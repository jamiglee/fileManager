#!/usr/bin/python
# -*- coding: UTF-8 -*-
# coding=utf-8
import time
import os

result = os.popen("md5sum README.md")
print("1")
res = result.read()
for line in res.splitlines():
    md5value = line.split(" ")[0]
    print(md5value)
datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print(datetime)

