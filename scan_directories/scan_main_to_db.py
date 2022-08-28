#!/usr/bin/python
# -*- coding: UTF-8 -*-
# coding=utf-8

import os
import sys
import logging
from configparser import ConfigParser

print(os.pardir)
sys.path.append(os.pardir)
from util import jutil
from util import file
from util import db
from util import logger

log = logger.Logger(loglevel=logging.INFO, loggername=__name__).getlog()

# 1. 扫描目录，将hash值和文件的路径保存到key value的map中{"hashstring": [路径list]}
# 2. 如果发现已经存在hashstring，代表有重复文件，单独记录到set中；
# 3. 遍历set输出路径；

local_file_path_list = []

file_total_num = 0


# read config file:
def read_cfg():
    config = ConfigParser()
    this_file_path = os.path.dirname(os.path.abspath(__file__))
    
    config_path = this_file_path + "%s..%sresources%sconfig.ini" % (os.sep, os.sep, os.sep)
    config_path = os.path.abspath(config_path)
    log.debug("config path: %s" % config_path)
    config.read(config_path, encoding='utf-8')

    # 定义扫描目录，区分linux/windows，如果不定义默认扫描全部目录；
    # 初始化文件例外的文件大小;
    # 初始化图片，音频，视频后缀
    global local_file_path_list
    global exclude_files
    global min_file_size

    ########
    if jutil.isLinux() == True:
        log.info("OS is linux")
        config_map = config["linux"]
    elif jutil.isWindows() == True:
        log.info("OS is windows")
        config_map = config['windows']
    else:
        log.error("unknown OS")

    ## init local_file_path
    scan_path = config_map["scan_path"]
    print("scan_path:" + scan_path)
    if(scan_path == None):
        log.error("Please set scan path first!")
    local_file_path_list = scan_path.split(";")

    exclude_files_str = config_map["exclude_files"] if config_map.__contains__("exclude_files") else ""
    exclude_files = exclude_files_str.split(";")
    ##

    ## init min_file_size
    min_file_size = int(config_map["min_file_size"]) if config_map.__contains__("min_file_size") else 0
    log.debug("min_file_size: %s bytes" % min_file_size)
    ##
        
    log.debug(local_file_path_list)
    return

def scan_path_list(path_list, conn, cur):
    for path in path_list:
        log.warning("start scan %s", path)
        files_list = file.get_files_path(path)
        # print(files_list)
        num = 0
        for file_path in files_list:
            if num != 0 and num%100 == 0:
                log.warning("find %d files in %s" % (num, path))
            file_info = file.get_file_info(file_path)
            db.insert_info(conn, cur, file_info)
            num = num + 1
        log.warning("find %d files in %s" % (num, path))
        log.warning("start scan %s", path)
    return


def visit_path_list(path_list, conn, cur):
    for path in path_list:
        log.warning("scan path [%s] begin" % path)
        visit_path(path, conn, cur)
        log.warning("scan path [%s] end" % path)
    return


def visit_path(root_path, conn, cur):
    try:
        li = os.listdir(root_path)
    except FileNotFoundError as e:
        log.warning("No such file or directory : %s" % root_path)
        return

    for p in li:
        if p in exclude_files:
            log.warning("exclude file/dir: %s" % p)
            continue
        path_name = os.path.join(root_path, p)
        if not os.path.isfile(path_name):  # 判断路径是否为文件，如果不是继续遍历
            log.warning("scan path: %s" % path_name)
            visit_path(path_name, conn, cur)
        else:
            if os.path.getsize(path_name) < min_file_size:
                return
            db.insert_info(conn, cur, file.get_file_info(path_name))
    return




# init local db, 从本地实例化的文件中初始化，也可以从网络盘中初始化；用来和多个计算机上的文件作对比
# def initDb():
#   return;


def get_print_files_info(cur):
    query_duplicate_sql = "select name, path, byte_size from file_infos"
    results = cur.execute(query_duplicate_sql).fetchall()
    log.warning("=============================start print file info=============================")
    num = 0
    
    for result in results:
        log.warning("No:%d, File Name: %s, File Path: %s, Size: %s" % (num + 1, result[0], result[1], result[2]))
        num = num + 1
    log.warning("=============================end print file num: %d============================" % num)
    return


def get_print_duplicate_files(cur):
    # query_duplicate_sql = "select * from file_infos"
    query_duplicate_sql = "select md5_value, name, path  from file_infos where md5_value = (select md5_value from file_infos group by md5_value having count(1) > 1) "
    # query_duplicate_sql = "select name, path, md5_value from file_infos"
    results = cur.execute(query_duplicate_sql).fetchall()
    print(results)
    if len(results) == 0:
        log.warning("not found duplicated files")
        return
    log.warning("Found same files:")
    log.warning(results)
    log.warning("=============================start print dupliate file=============================")
    num = 0
    
    for result in results:
        log.warning("No:%d, MD5Value: %s, File Name: %s, File Path: %s" % (num + 1, result[0], result[1], result[2]))
        num = num + 1
    log.warning("=============================end duplicate file num: %d============================" % num)

def init_files_info():
    try:
        # 定义扫描目录
        log.warning("init..begin")
        read_cfg()
        log.warning("init..end")
        conn = db.get_database_conn()
        cur = db.get_cur(conn)
        db.create_file_table(cur)
        log.warning("scan paths..begin")
        scan_path_list(local_file_path_list, conn, cur)
        log.warning("scan paths..end")
        log.warning("scan %d files" % file_total_num)
        log.warning("print..begin")
        # get_print_files_info(cur)
        db.close_cur(cur)
        db.close_conn(conn)
        log.warning("print..end")
    except Exception as e:
        log.exception(e)
    finally:
        return

def scan_duplicate_files():
    try:
        # 定义扫描目录
        log.warning("init..begin")
        read_cfg()
        log.warning("init..end")
        conn = db.get_memory_db_conn()
        cur = db.get_cur(conn)
        db.create_file_table(cur)
        log.warning("scan paths..begin")
        # visit_path_list(local_file_path_list, conn, cur)
        files_list = file.get_files_path()
        for file_path in files_list:
            file_info = file.get_file_info(file_path)
            db.insert_info(conn, cur, file_info)
        log.warning("scan paths..end")
        log.warning("scan %d files" % file_total_num)
        log.warning("print..begin")
        get_print_duplicate_files(cur)
        db.close_cur(cur)
        db.close_conn(conn)
        log.warning("print..end")
    except Exception as e:
        log.exception(e)
    finally:
        return


def test():
    get_print_duplicate_files()

if __name__ == '__main__':
    print(11213)
    init_files_info()
