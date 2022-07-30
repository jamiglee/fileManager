#!/usr/bin/python
# coding=utf-8
import sqlite3
import logging

from util import file
from util import logger

log = logger.Logger(loglevel=logging.INFO, loggername=__name__).getlog()

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

    log.info("create table file_infos success!")


    path = "f:/github/fileManager/util/file.py"
    file_info = file.get_file_info(path)
    print("file_info %s" % file_info)
    sql_text_2 = "INSERT INTO file_infos VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (file_info['device_id'], file_info['name'], file_info['path'],file_info['type'],file_info['path'],file_info['byte_size'],file_info['create_time'])
    print(sql_text_2)
    cur.execute(sql_text_2)

    conn.commit()
    log.info("insert table file_infos success!")


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
    log.info("create table file_infos success!")
    return


def insert_info(conn, cur, file_info):
    sql_text_2 = "INSERT INTO file_infos VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (file_info['device_id'], file_info['name'], file_info['path'], file_info['type'], file_info['md5_value'], file_info['byte_size'], file_info['create_time'])
    cur.execute(sql_text_2)
    conn.commit()


def query_file_infos(conn, cur, limit=100):
    query_sql = "select name, count(1) from file_infos where count(1) > 1 group by md5_value"
    cur.execute(query_sql)
    result = cur.fetchall()
    log.debug(result.__len__)
    log.info(result)
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
