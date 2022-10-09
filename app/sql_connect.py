# -*- coding: utf-8 -*-

import pandas as pd 
import sqlalchemy 
from sqlalchemy import create_engine
import pymysql
import re 

def table_exists(table_name):
    connect = pymysql.connect(host="127.0.0.1",
                              user="root",
                              password="1234",
                              port=3306,                   
                              db ="yt_apple_bigdata",
                              charset = 'utf8')   
    con = connect.cursor()    
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    if table_name in table_list:
        return 1
    else:
        return 0

def find_add_data(table_name, seg_table_name):
    DB_USER = "root"
    DB_PASS = 1234"
    DB_HOST =  "127.0.0.1"
    DB_PORT = "3306"
    DATABASE = "yt_apple_bigdata"
    connect_info = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".for
