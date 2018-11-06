#encoding=utf-8
import pymysql
db=pymysql.connect("127.0.0.1","root","yinxunjiang","test")

cur=db.cursor()
cur.execute("select * from test1;")
data=cur.fetchall()
print (data)
#1223456

