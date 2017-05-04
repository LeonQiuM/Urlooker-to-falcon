#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author : Leon



#open-falcon API
PUSHHOME = "http://127.0.0.1/v1/push"

#agent需要执行的系统命令，请确保在每一个agent上都执行成功
AGENTCMD = "python3 /data/scripts/urlooker_to_falcon/src/urlooker-to-falcon.py"


#socket-server-config
Server = "0.0.0.0"
Port = 6699

#时间间隔，server会定时去执行agent上的脚本，也是falcon的step间隔
STEP = 300

