# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 14:51:43 2018

@author: 11796
"""
import pymysql
from Model import News


class NewsDataBase:
    def __init__(self):
        self.host = 'localhost'  # 服务器名
        self.user = 'root'  # 用户名
        self.pwd = '123456'  # 密码
        self.db = 'news'  # 数据库名

    def Create(self):
        print("Create A TABLE SAVE NEWS PAGE")
        # 打开数据库连接
        db = pymysql.connect(self.host, self.user, self.pwd, self.db)
        # 使用 cursor() 方法创建一个游标对象 cursor 
        cursor = db.cursor()
        # 使用预处理语句创建表 
        sql = """CREATE TABLE IF NOT EXISTS NEWS ( 
        ID INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        FILENAME CHAR(80) NOT NULL,
        PATH CHAR(100) NOT NULL, 
        WEBSITE CHAR(20) NOT NULL,
        TITLE CHAR(80) NOT NULL, 
        TIME1 CHAR(12) NOT NULL, 
        TIME2 CHAR(10) NOT NULL,
        TYPE CHAR(20) NOT NULL
        )"""
        cursor.execute(sql)
        # 关闭数据库连接
        db.close()

    def Drop(self):
        print("Drop This Table")
        # 打开数据库连接 
        db = pymysql.connect(self.host, self.user, self.pwd, self.db)
        # 使用 cursor() 方法创建一个游标对象 cursor 
        cursor = db.cursor()
        # 使用 execute() 方法执行 SQL，如果表存在则删除 
        cursor.execute("DROP TABLE IF EXISTS NEWS")
        # 关闭数据库连接 
        db.close()

    def Insert(self, news):
        try:
            # 打开数据库连接
            db = pymysql.connect(self.host, self.user, self.pwd, self.db, charset="utf8")
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            # SQL 插入语句
            sql = """INSERT INTO NEWS
                        (FILENAME, PATH, WEBSITE, TITLE, TIME1, TIME2, TYPE) 
                        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(news.filename, news.path, news.website,
                                                                                    news.title, news.time1, news.time2,
                                                                                    news.type)
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            db.close()
        except:
            print('INSERT ERROR')
            # 如果发生错误则回滚
            db.rollback()
            # 关闭数据库连接
            db.close()

    def Select(self, sql):
        print("Select")
        # 打开数据库连接
        db = pymysql.connect(self.host, self.user, self.pwd, self.db, charset="utf8")
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # SQL 查询语句 
        # sql = "SELECT * FROM EMPLOYEE WHERE INCOME > '%d'" % (1000)
        try:
            # 执行SQL语句 
            cursor.execute(sql)
            # 获取所有记录列表 
            results = cursor.fetchall()
            params = []
            for row in results:
                news = News.News()
                news.id = row[0]
                news.filename = row[1]
                news.path = row[2]
                news.website = row[3]
                news.title = row[4]
                news.time1 = row[5]
                news.time2 = row[6]
                news.type = row[7]
                params.append(news)
                # 打印结果
            db.close()
            return params
        except:
            print("Error: unable to fetch data")
            # 关闭数据库连接
            db.close()
            return None

    def SelectAndGetRows(self, sql):
        print("Select")
        # 打开数据库连接
        db = pymysql.connect(self.host, self.user, self.pwd, self.db, charset="utf8")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 查询语句
        # sql = "SELECT * FROM EMPLOYEE WHERE INCOME > '%d'" % (1000)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            params = []
            for row in results:
                news = News.News()
                news.id = row[0]
                news.filename = row[1]
                news.path = row[2]
                news.website = row[3]
                news.title = row[4]
                news.time1 = row[5]
                news.time2 = row[6]
                news.type = row[7]
                params.append(news)
                # 打印结果
            cursor.execute('SELECT FOUND_ROWS()')
            count = cursor.fetchall()[0][0]
            db.close()
            return params, count
        except:
            print("Error: unable to fetch data")
            # 关闭数据库连接
            db.close()
            return None