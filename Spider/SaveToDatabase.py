# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 14:51:43 2018

@author: 11796
"""
import pymysql

class NewsDataBase:
    def __init__(self): 
        self.host = 'localhost'#服务器名
        self.user = 'root'#用户名
        self.pwd = '123456'#密码 
        self.db = 'news'#数据库名
    def Create(self):
        print("Create A TABLE SAVE NEWS PAGE")
        # 打开数据库连接 
        db = pymysql.connect(self.host, self.user, self.pwd, self.db )
        # 使用 cursor() 方法创建一个游标对象 cursor 
        cursor = db.cursor()
        # 使用预处理语句创建表 
        sql = """CREATE TABLE IF NOT EXISTS NEWS 
        ( 
        FILENAME CHAR(80) NOT NULL,
        PATH CHAR(100) NOT NULL, 
        WEBSITE CHAR(20) NOT NULL,
        TITLE CHAR(80) NOT NULL, 
        TIME1 CHAR(12) NOT NULL, 
        TIME2 CHAR(10) NOT NULL,
        TYPE CHAR(20)
        )""" 
        cursor.execute(sql) 
        # 关闭数据库连接 
        db.close()
    def Drop(self):
        print("Drop This Table")
        # 打开数据库连接 
        db = pymysql.connect(self.host, self.user, self.pwd, self.db ) 
        # 使用 cursor() 方法创建一个游标对象 cursor 
        cursor = db.cursor() 
        # 使用 execute() 方法执行 SQL，如果表存在则删除 
        cursor.execute("DROP TABLE IF EXISTS NEWS") 
        # 关闭数据库连接 
        db.close()
    def Insert(self, params):
        #try: 
            # 打开数据库连接 
            db = pymysql.connect(self.host, self.user, self.pwd, self.db, charset="utf8") 
            # 使用cursor()方法获取操作游标 
            cursor = db.cursor() 
            # SQL 插入语句 
            sql = """INSERT INTO NEWS
                    (FILENAME, PATH, WEBSITE, TITLE, TIME1, TIME2, TYPE) 
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(params[0], params[1], params[2], params[3], params[4], params[5], params[6])
           
            # 执行sql语句 
            cursor.execute(sql) 
            # 提交到数据库执行 
            db.commit()    
        #except: 
            #print('INSERT ERROR')
            # 如果发生错误则回滚 
            #db.rollback() 
            # 关闭数据库连接 
            #db.close()
    def Select(self, sql):
        print("Select")
        # 打开数据库连接 
        db = pymysql.connect(self.host, self.user, self.pwd, self.db, charset="utf8") 
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor() 
        # SQL 查询语句 
        #sql = "SELECT * FROM EMPLOYEE WHERE INCOME > '%d'" % (1000) 
        try: 
            # 执行SQL语句 
            cursor.execute(sql) 
            # 获取所有记录列表 
            results = cursor.fetchall() 
            params = []
            for row in results: 
                p = {'filename':row[0], 'path': row[1]
                , 'website':row[2], 'title':row[3]
                , 'time1':row[4], 'time2':row[5]
                , 'type':row[6]}
                params.append(p)
                # 打印结果 
            return params
        except: 
            print ("Error: unable to fetch data") 
            # 关闭数据库连接 
            db.close()
            return None
nd = NewsDataBase()
info = nd.Select('select * from news')
count = 0
with open('newsTitle.txt', 'a', encoding = 'utf-8') as n:  
    for p in info:
        count = count + 1
        n.write(p['title'])
        print(p)
print(count)

    