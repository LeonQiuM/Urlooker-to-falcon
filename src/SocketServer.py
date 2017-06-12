#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author : Leon

import socketserver
import sys,os,json
import re

BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BaseDir)
from conf.config import *


class UrlLookerTcpHandler(socketserver.BaseRequestHandler):

    def handle(self):
        '''
        handle
        :return: 
        '''
        li = []
        while True:
            try:
                self.data = self.request.recv(1024).strip()
            except Exception as text:
                print(text,"recv timeout")
            if not self.data:
                break
            li.append(self.data.decode())
            self.request.sendall("OK".encode())
        print(len(li))
        new_li = []
        for i in li:
            newli = re.sub("'","",i)
            new_li.append(json.loads(newli))
        with open("../db/db",'a') as f:
            for i in new_li:
                f.write(json.dumps(i)+"\n")


HOST, PORT = Server, Port
server = socketserver.ThreadingTCPServer((HOST, PORT), UrlLookerTcpHandler)
server.serve_forever()

