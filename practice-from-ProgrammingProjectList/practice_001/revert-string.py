#! /usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
项目来源自https://github.com/jobbole/ProgrammingProjectList.git

题目:逆转字符串

使用方法:
revert-string [-h|--help] string

'''

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Revert the string')
    parser.add_argument('string', metavar='string', type=str,
                        help='the string will be reverted')

    namespace = parser.parse_args()

    print(namespace.string[-1::-1])
