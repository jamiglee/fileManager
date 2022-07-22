#!/usr/bin/python
# -*- coding: UTF-8 -*-
# coding=utf-8

import os
import sys
import jutil
import logging
from configparser import ConfigParser

logger = logging.getLogger('fileManager')
formatter = logging.Formatter('%(asctime)s|%(processName)s|%(threadName)s|%(levelname)s|%(filename)s:%(lineno)d|%('
                              'funcName)s|%(message)s')
file_handler = logging.FileHandler("scan_main.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)



# 1. 扫描目录，将hash值和文件的路径保存到key value的map中{"hashstring": [路径list]}
# 2. 如果发现已经存在hashstring，代表有重复文件，单独记录到set中；
# 3. 遍历set输出路径；

duplicate_filehash_set = set()
hashfile_dict = {}
local_file_path_list = ""
file_total_num = 0



# read config file:
def read_cfg():
    config = ConfigParser()
    this_file_path = os.path.dirname(os.path.abspath(__file__))
    
    config_path = this_file_path + "%s..%sresources%sconfig.ini" % (os.sep, os.sep, os.sep)
    config_path = os.path.abspath(config_path)
    logger.debug("config path: %s" % config_path)
    config.read(config_path)

    # 定义扫描目录，区分linux/windows，如果不定义默认扫描全部目录；
    # 初始化文件例外的文件大小;
    # 初始化图片，音频，视频后缀
    global local_file_path_list
    global exclude_files
    if jutil.isLinux() == True:
        config_map = config["linux"]
        logger.info("OS is linux")
        scan_path = config_map["scan_path"]
        print("scan_path:" + scan_path)
        if(scan_path == None):
            logger.error("Please set scan path first!")
        local_file_path_list = scan_path.split(";")

        exclude_files_str = config_map["exclude_files"]
        exclude_files = exclude_files_str.split(";")

    elif jutil.isWindows() == True:
        logger.info("OS is windows")
        # print(config.sections())
        # print(config.items('windows'))
        config_map = config['windows']
        local_file_path_list = config_map['scan_path']
    else:
        logger.error("unknown OS")
        
    logger.debug(local_file_path_list)
    return

def visit_path_list(path_list):
    for path in path_list:
        logger.warning("scan path [%s] begin" % path)
        visit_path(path)
        logger.warning("scan path [%s] end" % path)
    return



def visit_path(root_path):
    try:
        li = os.listdir(root_path)
    except FileNotFoundError as e:
        logger.warning("No such file or directory : %s" % root_path)
        return

    for p in li:
        if p in exclude_files:
            logger.warning("exclude file/dir: %s" % p)
            continue
        path_name = os.path.join(root_path, p)
        if not os.path.isfile(path_name):  # 判断路径是否为文件，如果不是继续遍历
            visit_path(path_name)
        else:
            # file_name = p;
            process_one_file(path_name, get_file_md5(path_name))
            logger.debug(path_name + ":" + str(get_file_md5(path_name)))
    return


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

# init local db, 从本地实例化的文件中初始化，也可以从网络盘中初始化；用来和多个计算机上的文件作对比
# def initDb():
#   return;


# main function
# 1. 扫描目录，将hash值和文件的路径保存到key value的map中{"hashstring": [路径list]}
# 2. 如果发现已经存在hashstring，代表有重复文件，单独记录到set中；
# 3. 遍历set输出路径；
def process_one_file(path, file_md5):
    #    fileHash = "hash1"
    global file_total_num
    file_total_num += 1
    if hashfile_dict.get(file_md5) is not None:
        value = hashfile_dict.get(file_md5)
        value.append(path)
        hashfile_dict.update({file_md5: value})
        duplicate_filehash_set.add(file_md5)
    else:
        fileList = [path]
        hashfile_dict[file_md5] = fileList
        return


def get_print_duplicate_files():
    if len(duplicate_filehash_set) == 0:
        logger.warning("not found duplicated files")
        return
    logger.warning("found same files:")
    num = 1
    for hashValue in duplicate_filehash_set:
        logger.warning("============ %d:%s ============" % (num, hashValue))
        path_list = hashfile_dict.get(hashValue)
        for n in range(len(path_list)):
            logger.warning(path_list[n])
        logger.warning("============ %d:%s ============" % (num, hashValue))
        num = num + 1

def scan_duplicate_files():
    try:
        # 定义扫描目录
        logger.warning("init..begin")
        read_cfg()
        logger.warning("init..end")
        logger.warning("scan paths..begin")
        visit_path_list(local_file_path_list)
        logger.warning("scan paths..end")
        logger.warning("scan %d files" % file_total_num)
        logger.warning("print..begin")
        get_print_duplicate_files()
        logger.warning("print..end")
    except Exception as e:
        logger.exception(e)
    finally:
        return


def test():
    process_one_file("/proc", "hash1")
    process_one_file("/proc1", "hash12")
    process_one_file("/proc13", "hash12")
    process_one_file("/proc14", "hash12")

    process_one_file("/proc/cat", "hash432")
    process_one_file("/media/jamie", "hash432")
    print(hashfile_dict)
    print(duplicate_filehash_set)
    get_print_duplicate_files()

if __name__ == '__main__':
    scan_duplicate_files()
      # path = []
    # path.append("E:\\")
    # path.append("D:\\")
    # visit_path_list(path)
