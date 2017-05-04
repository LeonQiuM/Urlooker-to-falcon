# 网站监控

## 摘要

```text
1. 监控方式是在urlooker的基础上，将数据dump下来进行整理汇总，计算均值等操作后再push到open-falcon
2. agent与server端的数据传输，采用socket的方式
3. server端控制了agent的定时执行
4. agent上传数据的同时也会将自己的dump下来的数据push到open-falcon作为独立的数据监测站点,并以一个为zone的tag来作为相同地址监控的区分
```

## 环境支持
+ Python3

## 部署

+ python环境

+ 依赖
```bash
pip install -r requirement.txt
```
+ server端配置
    1. 防火墙请打开对应端口限制，以便于agent上报的数据正常接收
    2. 监听端口默认为`6699`，server修改请注意修改agent与之对应
    3. 私钥请将内容添加至conf目录下的id_rsa文件中

+ agent相关配置
    1. 公钥私钥对登录配置
    2. 外网访问
  
+ 启动server

```bash
sh bin/setup.sh
```