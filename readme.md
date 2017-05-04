# 网站监控

## 前言

1. 感谢
+ [URLooker](https://github.com/URLooker "URLooker")
+ [open-falcon](https://github.com/open-falcon "open-falcon")


## 摘要

```text
1. 监控方式是在urlooker的基础上，将数据dump下来进行整理汇总，计算等操作后再push到open-falcon
2. agent与server端的数据传输，采用socket的方式
3. server端控制了agent的定时执行
4. agent上传数据的同时也会将自己的dump下来的数据push到open-falcon作为独立的数据监测站点,并以一个为zone的tag来作为相同地址监控的区分
```

> 1. 在URLooker的基础上将数据手机整理，重新计算后push到open-falcon
> 2. 由于URLooker的部署可以分布到不同的地点，所以在处理数据的时候，不但将每个点的数据都push到falcon，\
而且会将所有点的结果进行汇总计算后push到falcon，并以tag:`zone=all`来辨识 
> 3. push到falcon的数据的endpoint为你在URLooker中监控的url地址
> 4. metric有只有两个:
> + 响应平均时间`ResponseTimeAverage`
> + 平均可用率`CurrentAvailableRate` 


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
cd src;nohup python3 SocketServer.py &
cd src;nohup python3 main.py &
```
## 添加新的监控节点

1. 首先部署`urlooker`，从其他节点导出监控数据，这样避免了手动添加
2. 添加`open-falcon`主机对新agent的免密码登录
3. 添加`open-falcon`主机对新agent的ssh`22`端口防火墙访问权限
4. `open-falcon`外网防火墙添加agent对其`6699`端口的访问权限
5. 新节点上存在`/data/scripts/urlooker_to_falcon/src/urlooker-to-falcon.py`
6. Python3
7. 依赖：
    + pymysql
    + requests
    + urlparse
    + socket
8. 在`agent.py`中的`agent_list`列表添加一个字典，请注意包含以下三个字段：
```python
    {
        "host":"",  
        "port":22,
        "username":"root"
    },
```