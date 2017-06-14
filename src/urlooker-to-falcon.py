#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author : Leon

import pymysql
import time
from urllib.parse import urlparse
import requests,json
import socket

ServerAddress="192.168.30.130"
ServerPort=6699

PUSHHOME="http://127.0.0.1/v1/push"
HOST="127.0.0.1"
ZoneTag = ""
PORT=3306
USER='root'
PASSWD=""
DB='urlooker'

class MysqlDb(object):
    def __init__(self,HOST,PORT,USER,PASSWD,DB):
        self.HOST = HOST
        self.PORT = PORT
        self.USER = USER
        self.PASSWD = PASSWD
        self.DB = DB

    def connect(self,sql):
        connect = pymysql.connect(host=self.HOST, port=self.PORT, user=self.USER, passwd=self.PASSWD, db=self.DB)
        cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        raw = cursor.fetchall()
        connect.commit()
        cursor.close()
        connect.close()
        return raw

    def __del__(self):
        pass
    def __str__(self):
        return "Exception!"

def query_map():
    '''
    Query the raw data table, maintaining the sid and url corresponding relation, and write the map.conf file
    :return: None
    '''
    _mysql_conn_obj = MysqlDb(HOST,PORT,USER,PASSWD,DB)
    raw = _mysql_conn_obj.connect("select * from {TABLE_NAME}".format(TABLE_NAME="strategy"))
    BaseData = {}
    for item in raw:
        key = item["id"]
        value = item["url"]
        BaseData[key] = value
    with open("map.conf",'w+') as f:
        for i,j in BaseData.items():
            line = str(i) + "\t" + str(j) + "\n"
            f.write(line)


def query_data():
    '''
    From the database to retrieve data within ten minutes before the current point in time
    :return: 
    
    '''
    CurrentTime = int(time.time())
    TenMinTime = CurrentTime - 600  #ten minutes
    _mysql_conn_obj = MysqlDb(HOST, PORT, USER, PASSWD, DB)
    raw = _mysql_conn_obj.connect(
        "select * from item_status00 where push_time>%s and push_time<%s order by Sid"
        %(TenMinTime, CurrentTime)
    )
    return raw


def handle_data():
    '''
    The original data cleaning
    :param query_data_raw: 
    :return: 
    '''
    OriginalData = query_data()
    CleanData = {}
    for item in OriginalData:
        CleanData[item["sid"]] = {}
        CleanData[item["sid"]]["resp_time"] = []
        CleanData[item["sid"]]["result"] = []
    for item in OriginalData:
        if item["sid"] in CleanData.keys():
            CleanData[item["sid"]]["resp_time"].append(item["resp_time"])
            CleanData[item["sid"]]["result"].append(item["result"])
    PushBaseData = {}
    for i, j in CleanData.items():
        PushBaseData[i] = {}
    for i, j in CleanData.items():
        ResponseTimeTotal = 0
        for item in j["resp_time"]:
            ResponseTimeTotal += item
        ResponseTimeAverage = ResponseTimeTotal / len(j["resp_time"])
        PushBaseData[i]["ResponseTimeAverage"] = ResponseTimeAverage
        ErrorCount = NormalCount = 0
        for item in j["resp_code"]:
            if item == 0:
                NormalCount += 1
            else:
                ErrorCount += 1
        CurrentAvailableRate = NormalCount / float(NormalCount + ErrorCount)
        PushBaseData[i]["CurrentAvailableRate"] = CurrentAvailableRate

    return PushBaseData


def _read_map():
    '''
    :return: 
    '''
    #update local file
    query_map()
    MapDict = {}
    with open("map.conf", 'r') as f:
        for line in f:
            sid, url = line.split()
            url = urlparse(url)
            MapDict[sid] = url.netloc+url.path
    return MapDict



def _push_data():
    '''
    handle push to open-falcon data
    :return: 
    '''
    PushBaseData = handle_data()
    Mapdict = _read_map()
    PushList = []

    for item in PushBaseData:
        item = int(item)
        FinallyPushData = {}
        FinallyPushData["endpoint"] = Mapdict[str(item)]
        FinallyPushData["metric"] = "ResponseTimeAverage"
        FinallyPushData["timestamp"] = int(time.time())
        FinallyPushData["value"] = PushBaseData[item]["ResponseTimeAverage"]
        FinallyPushData["counterType"] = "GAUGE"
        FinallyPushData["tags"] = "Zone={ZoneTag}".format(ZoneTag=ZoneTag)
        FinallyPushData["step"] = 300
        PushList.append(FinallyPushData)
        FinallyPushData = {}
        FinallyPushData["endpoint"] = Mapdict[str(item)]
        FinallyPushData["metric"] = "CurrentAvailableRate"
        FinallyPushData["timestamp"] = int(time.time())
        FinallyPushData["value"] = PushBaseData[item]["CurrentAvailableRate"]
        FinallyPushData["counterType"] = "GAUGE"
        FinallyPushData["tags"] = "Zone={ZoneTag}".format(ZoneTag=ZoneTag)
        FinallyPushData["step"] = 300
        PushList.append(FinallyPushData)
    return PushList


if __name__ == '__main__':
    PushDataList = _push_data()
    response = requests.post(PUSHHOME,data=json.dumps(PushDataList))
    print(response.text)

    client = socket.socket()
    client.connect((ServerAddress, ServerPort))

    while True:
        for i in PushDataList:
            client.sendall(json.dumps(i).encode())
            print(len(PushDataList))
            recv = client.recv(1024)
            print("recv status", recv.decode())
        break

    client.close()





