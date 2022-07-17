#!/usr/bin/python
# -*- coding: UTF-8 -*-
# coding=utf-8

import os
import time
import jutil
import logging

# logging.basicConfig(format='%(asctime)s|%(processName)s|%(threadName)s|%(levelname)s|%(filename)s:%(lineno)d|%(funcName)s|%(message)s')

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s: %(message)s',level='INFO')



# 1. 扫描目录，将hash值和文件的路径保存到key value的map中{"hashstring": [路径list]}
# 2. 如果发现已经存在hashstring，代表有重复文件，单独记录到set中；
# 3. 遍历set输出路径；

duplicate_filehash_set = set()
hashfile_dict = {}
local_file_path = ""
file_num = 0


# read config file:
def read_cfg():
    # 定义扫描目录，区分linux/windows，如果不定义默认扫描全部目录；
    # 初始化文件例外的文件大小;
    # 初始化图片，音频，视频后缀
    global local_file_path
    # _local_file_path_ = "/media/jamie/Document/GatewayFiles/photo"
    if jutil.isLinux() == True:
        logging.info("OS is linux")
        local_file_path = "/media/jamie/Document"
    elif jutil.isWindows() == True:
        logging.info("OS is windows")
        local_file_path = "E:\\djgo\\testdir"
    else:
        logging.error("unknown OS")
        
    logging.debug(local_file_path)
    return


def visit_path(root_path):
    try:
        li = os.listdir(root_path)
    except FileNotFoundError as e:
        logging.warning("No such file or directory : %s" % root_path)
        return

    for p in li:
        path_name = os.path.join(root_path, p)
        if not os.path.isfile(path_name):  # 判断路径是否为文件，如果不是继续遍历
            visit_path(path_name)
        else:
            # file_name = p;
            process_one_file(path_name, get_file_md5(path_name))
            logging.debug(path_name + ":" + str(get_file_md5(path_name)))
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
            logging.exception("calc error:", pathname)
        elif jutil.isWindows() == True:
            command = 'certutil -hashfile "' + pathname + '" MD5'
            results = os.popen(command)
            result = results.read()
            # for line in result.splitlines():
            #     print(line)
            #     # md5value = line.split(" ")[0]
            #     # return md5value
            logging.debug("file " + pathname + " md5:" + result.splitlines()[1])
            return result.splitlines()[1]
            # for line in result.splitlines():
            #     print(line)
            #     # md5value = line.split(" ")[0]
            #     # return md5value
        else:
            return
    else:
        logging.warning(pathname + ": not a file")
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
    global file_num
    file_num += 1
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
        print("not found duplicated files")
        return
    print("found same files:")
    num = 1
    for hashValue in duplicate_filehash_set:
        print("============ %d:%s ============" % (num, hashValue))
        path_list = hashfile_dict.get(hashValue)
        for n in range(len(path_list)):
            print(path_list[n])
        print("============ %d:%s ============" % (num, hashValue))
        num = num + 1


def print_with_time(log):
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ":" + log)


def scan_duplicate_files():
    try:
        # 定义扫描目录
        logging.warning("init..begin")
        read_cfg()
        logging.warning("init..end")
        logging.warning("scan path begin: " + local_file_path)
        visit_path(local_file_path)
        logging.warning("scan path..end")

        logging.warning("scan %d files" % file_num)

        logging.warning("print..begin")
        get_print_duplicate_files()
        logging.warning("print..end")
    except Exception as e:
        logging.exception(e)
    finally:
        return



# get_file_md5("/media/jamie/Document/GatewayFiles/photo/惠州/IMG_0014 (1).JPG")

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

scan_duplicate_files()