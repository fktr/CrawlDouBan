#coding=utf-8

import mysql.connector

class DBHelper(object):

    def __init__(self,db):
        self.conn=mysql.connector.Connect(host="127.0.0.1",port=3306,db=db,user="fu",password="hitsucks")

    def close(self):
        self.conn.close()

    def create_table(self,table):
        cursor=self.conn.cursor()
        sql="create table %s(" \
            "title varchar(60)," \
            "author varchar(30)," \
            "country varchar(20)," \
            "isbn varchar(20)," \
            "page_num int unsigned," \
            "price float(6,2) unsigned," \
            "score float(2,1) unsigned," \
            "reader_num int unsigned," \
            "publisher varchar(30)," \
            "publish_date date," \
            "image varchar(20)," \
            "book_info varchar(2048)," \
            "author_info varchar(1024));" % (table)
        try:
            cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def save_book(self,book):
        cursor=self.conn.cursor()
        sql = "insert into %s (title,author,country,isbn,page_num,price,score,reader_num,publisher,publish_date,image,book_info,author_info)" \
              "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" %(
              book['tag'], book['title'], book['author'], book['country'],book['isbn'], book['page_num'], book['price'], book['score'],
              book['reader_num'],book['publisher'], book['publish_date'],book['image'], book['book_info'], book['author_info'])
        try:
            cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            return False
        finally:
            cursor.close()
