#!/usr/bin/python
# coding=utf-8

import datetime
import logging
import os
from util import jutil

logger = logging.getLogger('fileManager')
# formatter = logging.Formatter('%(asctime)s|%(processName)s|%(threadName)s|%(levelname)s|%(filename)s:%(lineno)d|%('
#                               'funcName)s|%(message)s')
# formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s %(funcName)s %(lineno)d : %(message)s')
# file_handler = logging.FileHandler("scan_main.log")
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# stream_handler = logging.StreamHandler(sys.stdout)
# stream_handler.setLevel(logging.INFO)
# stream_handler.setFormatter(formatter)
# logger.addHandler(stream_handler)

# logger.setLevel(logging.DEBUG)


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
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files

    # for dirpath, dirnames, filenames in os.walk(path):
    #     for filename in filenames:
    #         print(os.path.join(dirpath, filename))

'''
返回单个文件的属性信息
'''
def get_file_info(path):
    file = {}
    if os.path.isfile(path):  # 判断路径是否为文件，如果不是继续遍历
        logging.warning("path: %s" % path)
        file['device_id'] = jutil.get_device_id()
        file['name'] = os.path.basename(path)
        file['path'] = os.path.abspath(path)
        file['type'] = os.path.splitext(path)[1]
        file['byte_size'] = os.path.getsize(path)
        file['md5_value'] = get_file_md5(path)
        file['create_time'] = datetime.datetime.fromtimestamp(os.path.getctime(path))
        print(datetime.datetime.fromtimestamp(os.path.getctime(path)))
        return file
    else:
        logging.warning("path %s is not a file" % path)
    return None


def get_file_md5(pathname):
    if os.path.isfile(pathname):
        if jutil.isLinux() == True:
            command = 'md5sum "' + pathname + '"'
            results = os.popen(command)
            result = results.read()
            for line in result.splitlines():
                # print(line)
                md5value = line.split(" ")[0]
                return md5value
            logger.exception("calc error:", pathname)
        elif jutil.isWindows() == True:
            command = 'certutil -hashfile "' + pathname + '" MD5'
            results = os.popen(command)
            result = results.read()
            # for line in result.splitlines():
            #     print(line)
            #     # md5value = line.split(" ")[0]
            #     # return md5value
            logger.debug("file " + pathname + " md5:" + result.splitlines()[1])
            return result.splitlines()[1]
            # for line in result.splitlines():
            #     print(line)
            #     # md5value = line.split(" ")[0]
            #     # return md5value
        else:
            return
    else:
        logger.warning(pathname + ": not a file")
        return
    return

if __name__ == '__main__':
    path = "E:\歌曲\金属\Rhapsody - Emerald Sword.mp3"
    print(get_file_info(path))
    path = "f:/github/fileManager/util/file.py"
    print(get_file_info(path))
    # print(get_files_path("f:/github/fileManager"))