#!/usr/bin/python
# coding=utf-8
import sqlite3
import logging
import sys
from util import file

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


def get_cur(conn):
    return conn.cursor()
    
def close_cur(cur):
    cur.close()
    return


def close_conn(conn):
    conn.close()
    return


def commit(conn):
    conn.commit()
    return


def testthisfile():
    # conn = sqlite3.connect('test.db')
    conn = sqlite3.connect(':memory:')

    cur = conn.cursor()

    # 建表的sql语句
    sql_text_1 = '''create table file_infos(
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

    logger.info("create table file_infos success!")


    path = "f:/github/fileManager/util/file.py"
    file_info = file.get_file_info(path)
    print("file_info %s" % file_info)
    sql_text_2 = "INSERT INTO file_infos VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (file_info['device_id'], file_info['name'], file_info['path'],file_info['type'],file_info['path'],file_info['byte_size'],file_info['create_time'])
    print(sql_text_2)
    cur.execute(sql_text_2)

    conn.commit()
    logger.info("insert table file_infos success!")


    # 查询数学成绩大于90分的学生
    sql_text_3 = "SELECT * FROM file_infos"
    cur.execute(sql_text_3)
    # 获取查询结果

    print("打印结果")
    print(cur.fetchall())
    cur.close()
    conn.close()

def get_memory_db_conn():
    return sqlite3.connect(':memory:')


def create_file_table(cur):
    # 建表的sql语句
    create_table_sql = '''create table if not exists file_infos(
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
    logger.info("create table file_infos success!")
    return


def insert_info(conn, cur, file_info):
    sql_text_2 = "INSERT INTO file_infos VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (file_info['device_id'], file_info['name'], file_info['path'], file_info['type'], file_info['md5_value'], file_info['byte_size'], file_info['create_time'])
    cur.execute(sql_text_2)
    conn.commit()


def query_file_infos(conn, cur, limit=100):
    query_sql = "select name, count(1) from file_infos where count(1) > 1 group by md5_value"
    cur.execute(query_sql)
    result = cur.fetchall()
    logger.debug(result.__len__)
    logger.info(result)
    return
    

if __name__ == '__main__':
    conn = get_memory_db_conn()
    cur = conn.cursor()
    create_file_table(cur)
    path = "f:/github/fileManager/util/file.py"
    file_info = file.get_file_info(path)
    for i in range(1, 10):
        insert_info(conn, cur, file_info)
    query_file_infos(conn, cur, 2)
    cur.close()
    conn.close()
