#!/usr/bin/python
# coding=utf-8
import sqlite3
import logging
import sys
import file

logger = logging.getLogger('fileManager')
# formatter = logging.Formatter('%(asctime)s|%(processName)s|%(threadName)s|%(levelname)s|%(filename)s:%(lineno)d|%('
#                               'funcName)s|%(message)s')
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s %(funcName)s %(lineno)d : %(message)s')
# file_handler = logging.FileHandler("scan_main.log")
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logger.setLevel(logging.DEBUG)


def testthisfile():
    # conn = sqlite3.connect('test.db')
    conn = sqlite3.connect(':memory:')

    cur = conn.cursor()

    # 建表的sql语句
    sql_text_1 = '''create table fileInfos(
        device_id varchar(36),
        name varchar(255),
        path varchar(1000),
        type varchar(36),
        md5_value varchar(36),
        byte_size bigint,
        create_time datetime
    )'''
    # 执行sql语句
    cur.execute(sql_text_1)

    logger.info("create table fileInfos success!")


    path = "f:/github/fileManager/util/file.py"
    file_info = file.get_file_info(path)
    print("file_info %s" % file_info)
    sql_text_2 = "INSERT INTO fileInfos VALUES('windows', '%s', '%s', '%s', '%s', '%s', '%s')" % (file_info['name'], file_info['path'],file_info['type'],file_info['path'],file_info['byte_size'],file_info['create_time'])
    print(sql_text_2)
    cur.execute(sql_text_2)

    conn.commit()
    logger.info("insert table fileInfos success!")


    # 查询数学成绩大于90分的学生
    sql_text_3 = "SELECT * FROM fileInfos"
    cur.execute(sql_text_3)
    # 获取查询结果

    print("打印结果")
    print(cur.fetchall())
    cur.close()
    conn.close()

def get_memory_db_conn():
    return sqlite3.connect(':memory:')


def create_file_table():
    conn = get_memory_db_conn()
    cur = conn.cursor()
    # 建表的sql语句
    create_table_sql = '''create table if not exists fileInfos(
        device_id varchar(36),
        name varchar(255),
        path varchar(1000),
        type varchar(36),
        md5_value varchar(36),
        byte_size bigint,
        create_time datetime
    )'''
    # 执行sql语句
    cur.execute(create_table_sql)
    cur.close()
    conn.close()
    logger.info("create table fileInfos success!")
    return

if __name__ == '__main__':
    print(11213)

    testthisfile()
