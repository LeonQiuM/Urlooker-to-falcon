#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author : Leon

import os,sys,time
import json
import requests

BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BaseDir)

from conf.config  import *
from conf.agent import *

from ParamikoClient import SSHTcpClient


def push(PushDataList):
    response = requests.post(PUSHHOME, data=json.dumps(PushDataList))
    print(response.text)


def analyse(AllUrlDict):
    PushDataList = []
    for key in AllUrlDict:
        Timedata = {}
        RateData = {}
        Timedata["endpoint"] = key
        RateData["endpoint"] = key
        ResponseTimeTotal = ResponseTimeCount = CurrentAvailableRateTotal = CurrentAvailableRateCount = 0
        for ValueDict in AllUrlDict[key]:

            if ValueDict.get("metric") == "ResponseTimeAverage":
                ResponseTimeTotal += ValueDict["value"]
                ResponseTimeCount += 1
            elif ValueDict.get("metric") == "CurrentAvailableRate":
                CurrentAvailableRateTotal += ValueDict["value"]
                CurrentAvailableRateCount += 1
        Timedata["metric"] = "ResponseTimeAverage"
        Timedata["value"] = ResponseTimeTotal/ResponseTimeCount
        Timedata["step"] = STEP
        Timedata["tags"] = "zone=all"
        Timedata["timestamp"] = int(time.time())
        Timedata["counterType"] = 'GAUGE'
        PushDataList.append(Timedata)
        RateData["metric"] = "CurrentAvailableRate"
        RateData["value"] = CurrentAvailableRateTotal / CurrentAvailableRateCount
        RateData["step"] = STEP
        RateData["tags"] = "zone=all"
        RateData["timestamp"] = int(time.time())
        RateData["counterType"] = 'GAUGE'
        PushDataList.append(RateData)
    return PushDataList



def grouping():
    '''
    :return: 
    '''
    AllUrlDict = {}
    with open("../db/db", 'r', encoding="utf-8") as f:
        for line in f:
            line = json.loads(line)
            if line["endpoint"] not in AllUrlDict.keys():
                AllUrlDict[line["endpoint"]] = []
                AllUrlDict[line["endpoint"]].append(line)
            else:
                AllUrlDict[line["endpoint"]].append(line)
    return AllUrlDict


while True:
    # loading data
    for agent in agent_list:
        print(agent)
        try:
            SSHClient = SSHTcpClient(agent["host"],agent["port"],agent["username"],private_key)
            SSHClient.connecting(AGENTCMD)
        except Exception as text:
            print(text)
            continue

    AllUrlDict = grouping()
    PushDataList = analyse(AllUrlDict)
    print(PushDataList)
    push(PushDataList)
    t = time.localtime()
    FileTag = "{year}-{mon}-{day}:{hour}:{min}:{sec}".format(year=t.tm_year,
                                                        mon=t.tm_mon,
                                                        day=t.tm_mday,
                                                        hour=t.tm_hour,
                                                        min=t.tm_min,
                                                        sec=t.tm_sec)
    os.rename("../db/db","../db/db.{date}".format(date=FileTag))
    time.sleep(STEP)

