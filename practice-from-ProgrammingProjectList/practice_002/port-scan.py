#! /usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
项目来源自https://github.com/jobbole/ProgrammingProjectList.git

题目: 端口扫描器

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

'''

import argparse
import asyncio
import socket
from concurrent.futures import ThreadPoolExecutor
import time

now = lambda : time.time()

def test_connect(address, port):
    r'''
    Corroutine func to test address:port can connect
    '''
    ret = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((address, port))
            ret = True
        except OSError as err:
            ret = False
    return (address, port, ret)



def scan_machine(address, start, end, concurrents=100):
    r'''
    scan machine
    '''
    with ThreadPoolExecutor(max_workers=concurrents) as executor:
        tasks = []
        loop = asyncio.get_event_loop()
        for port in range(start, end):
            future = loop.run_in_executor(executor, test_connect, address, port)
            task = asyncio.ensure_future(future)
            tasks.append(task)
        tasks_future = asyncio.wait(tasks)
        finished_futures, _ = loop.run_until_complete(tasks_future)
        loop.close()

    return sorted([future.result() for future in finished_futures])







if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="scan which ports listening")
    parser.add_argument("-a", "--address", type=str, help="address")
    parser.add_argument("-s", "--start-port", type=int, help="scan start port")
    parser.add_argument("-e", "--end-port", type=int, help="scan end port")

    params = parser.parse_args()
    address, start, end = params.address, params.start_port, params.end_port + 1

    start_time = now()
    results = scan_machine(address, start, end)
    use_time = now() - start_time

    for address, port, result in results:
        if result:
            print("{}:{} opend".format(address, port))

    print("use {}s".format(use_time))
