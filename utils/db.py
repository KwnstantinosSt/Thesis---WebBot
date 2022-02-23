import mysql.connector
from configparser import ConfigParser
from mysql.connector.errors import Error
from mysql.connector import errorcode
import sys


def connectDb():
    try:
        config = ConfigParser()
        config.read("../env.ini")
        host = config['CONNECTION_STRING']['Connection']
        user = config['MYSQL_CREDENTIALS']['User']
        password = config['MYSQL_CREDENTIALS']['Pass']
        db_name = config['MYSQL_DATABASE_NAME']['DbName']
        # print("Configuration file read successfully.")
        print(host, user, password, db_name)
        try:
            _db = mysql.connector.connect(
                host=host, user=user, password=password)
            # print("Connected to database successfully.")
            cursor = _db.cursor()
            cursor.execute("SHOW DATABASES")
            dbList = []
            for x in cursor:
                for i in x:
                    dbList.append(i)
            if db_name in dbList:
                _db.connect(database=db_name)
                _db.cursor(prepared=True)
            else:
                cursor.execute(f"CREATE DATABASE {db_name}")
                _db.connect(database=db_name)
                cursor.execute("CREATE TABLE bots(run_id integer auto_increment,start_url varchar(255),start_url_title varchar(255),bot_method varchar(255),bot_depth integer,page_size real,bot_status varchar(255),access_time varchar(255),modification_time varchar(255),primary key(run_id))")
                cursor.execute("CREATE TABLE urls(url_id integer auto_increment,bot_id integer,url varchar(255),url_title varchar(255),url_page_size varchar(255),parent_url varchar(255),width real,height real,color varchar(255),x real,y real,font_size real,font_name varchar(255),font_attrs varchar(255),found_deapth integer,visited bool default false,url_access_time varchar(255),url_modification_time varchar(255),primary key(url_id),foreign key(bot_id) references bots(run_id) on delete cascade on update cascade)")
                _db.cursor(prepared=True)
            return cursor
        except mysql.connector.Error as err:
            print(f"MysqlError: {err}")
            print("Exiting...")
            exit(1)
    except Exception as e:
        print(f"Error: {e}")
        print("Exiting...")
        exit(1)


def connectDb2():
    try:
        try:
            _db = mysql.connector.connect(
                host='localhost', user='root', password='')
            # print("Connected to database successfully.")
            cursor = _db.cursor()
            cursor.execute("SHOW DATABASES")
            dbList = []
            for x in cursor:
                for i in x:
                    dbList.append(i)
            if 'webbot2' in dbList:
                _db.connect(database='webbot3')
                _db.cursor(prepared=True)
            else:
                cursor.execute("CREATE DATABASE webbot3")
                _db.connect(database='webbot3')
                cursor.execute("CREATE TABLE bots(run_id integer auto_increment,bot_method varchar(255),bot_depth integer,bot_status varchar(255),bot_start_time varchar(255),bot_end_time varchar(255),primary key(run_id));")
                cursor.execute("CREATE TABLE urls(id integer auto_increment,run_id integer,url varchar(255) unique,url_title varchar(255),url_size real,url_access_time varchar(255),url_modification_time varchar(255),primary key(id),foreign key(run_id) references bots(run_id) on delete cascade on update cascade);")
                cursor.execute("CREATE TABLE links(id integer auto_increment,url_id integer,link varchar(255),link_title varchar(255),width real,height real,color varchar(255),x real,y real,font_size real,font_name varchar(255),font_attrs varchar(255),found_depth integer,visited bool default false,link_access_time varchar(255),link_modification_time varchar(255),primary key(id),foreign key(url_id) references urls(id) on delete cascade on update cascade);")
                _db.cursor(prepared=True)
            return _db
        except mysql.connector.Error as err:
            print(f"MysqlError: {err}")
            print("Exiting...")
            exit(1)
    except Exception as e:
        print(f"Error: {e}")
        print("Exiting...")
        exit(1)
