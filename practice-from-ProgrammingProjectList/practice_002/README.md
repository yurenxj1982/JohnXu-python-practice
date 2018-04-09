# 练习2: 端口扫描器

输入某个ip地址和端口区间，程序会逐个尝试区间内的端口，如果能成功连接的话就将该端口标记为open。

## 使用方法：

``` shell
$ python3 port-scan.py -h
usage: port-scan.py [-h] [-a ADDRESS] [-s START_PORT] [-e END_PORT]

scan which ports listening

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        address
  -s START_PORT, --start-port START_PORT
                        scan start port
  -e END_PORT, --end-port END_PORT
                        scan end port

```

## 分析
1. socket 连接操作判断对方端口是否处在监听状态
2. 使用asyncio.eventloop进行并发操作

## 练习目标
1. 熟悉socket connect
1. 熟悉asyncio eventloop


## 实现
参见[port-scan.py](./port-scan.py)

