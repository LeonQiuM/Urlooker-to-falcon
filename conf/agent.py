#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author : Leon


#paramiko相关配置，采用私钥公钥对的方式进行登录agent,请提前进行授权
private_key = "../conf/id_rsa"


#各个地域的agent配置，这是一个列表，列表中的每一个agent为一个字典，添加请确保关键字段完整
#并要求登录的用户对agent的脚本有执行的权限

agent_list = [
    {
        "host":"192.168.30.130",  # ssh ip
        "port":22,  #ssh port
        "username":"root",  # ssh user
    },
]