#!/usr/bin/python
# coding=utf-8

import datetime

import logging
import os
import sys
print(os.curdir)
sys.path.append(os.pardir)
from util import jutil
from util import logger

log = logger.Logger(loglevel=logging.INFO, loggername=__name__).getlog()
device_id = jutil.get_device_id()

''' device_id varchar(36),
    name varchar(255),
    path varchar(1000),
    type varchar(36),
    md5_value varchar(36),
    byte_size bigint,
    create_time datetime
'''

'''
返回路径下的所有文件
'''
def get_files_path(path):
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        # print("dirpath:%s" % dirpath)
        for filename in filenames:
            # print("filename:%s" % filename)
            files.append(os.path.join(dirpath, filename))
    return files

'''
返回单个文件的属性信息
'''
def get_file_info(path):
    file = {}
    if os.path.isfile(path):  # 判断路径是否为文件，如果不是继续遍历
        logging.debug("path: %s" % path)
        file['device_id'] = device_id
        file['name'] = os.path.basename(path)
        file['path'] = os.path.abspath(path)
        file['type'] = os.path.splitext(path)[1]
        file['byte_size'] = os.path.getsize(path)
        file['md5_value'] = get_file_md5(path)
        file['create_time'] = datetime.datetime.fromtimestamp(os.path.getctime(path))
        file['update_time'] = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        # print(datetime.datetime.fromtimestamp(os.path.getctime(path)))
        return file
    else:
        log.warning("path %s is not a file" % path)
    return None

def get_file_info_2(path):
    file = {}
    if os.path.isfile(path):  # 判断路径是否为文件，如果不是继续遍历
        logging.debug("path: %s" % path)
        file_stat = os.stat(path)
        file['device_id'] = jutil.get_device_id()
        file['name'] = os.path.basename(path)
        file['path'] = os.path.abspath(path)
        file['type'] = os.path.splitext(path)[1]
        file['byte_size'] = file_stat.st_size
        file['md5_value'] = get_file_md5(path)
        file['create_time'] = datetime.datetime.fromtimestamp(file_stat.st_ctime)
        file['update_time'] = datetime.datetime.fromtimestamp(file_stat.st_mtime)
        # print(datetime.datetime.fromtimestamp(os.path.getctime(path)))
        return file
    else:
        log.warning("path %s is not a file" % path)
    return None


def get_file_md5(pathname):
    return
    if os.path.isfile(pathname):
        if jutil.isLinux() == True:
            command = 'md5sum "' + pathname + '"'
            results = os.popen(command)
            result = results.read()
            for line in result.splitlines():
                # print(line)
                md5value = line.split(" ")[0]
                return md5value
            log.exception("calc error:", pathname)
        elif jutil.isWindows() == True:
            command = 'certutil -hashfile "' + pathname + '" MD5'
            results = os.popen(command)
            result = results.read()
            # for line in result.splitlines():
            #     print(line)
            #     # md5value = line.split(" ")[0]
            #     # return md5value
            log.debug("file " + pathname + " md5:" + result.splitlines()[1])
            return result.splitlines()[1]
            # for line in result.splitlines():
            #     print(line)
            #     # md5value = line.split(" ")[0]
            #     # return md5value
        else:
            return
    else:
        log.warning(pathname + ": not a file")
        return
    return

if __name__ == '__main__':
    # path = "E:\歌曲\金属\Rhapsody - Emerald Sword.mp3"
    # print(get_file_info(path))
    # path = "f:/github/fileManager/util/file.py"
    # print(get_file_info(path))
    # # print(get_files_path("f:/github/fileManager"))
    print(get_files_path("F:\\"))