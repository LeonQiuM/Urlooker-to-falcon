#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author : Leon

import paramiko

class SSHTcpClient(object):
    def __init__(self,host,port,username,pkey):
        self.host = host
        self.port = port
        self.username = username
        self.pkey = pkey

    def connecting(self,cmd):
        private_key = paramiko.RSAKey.from_private_key_file(self.pkey)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host,
                    port=self.port,
                    username=self.username,
                    pkey=private_key
                    )
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        print(result.decode())
        ssh.close()