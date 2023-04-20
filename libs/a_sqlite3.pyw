import sqlite3,os
import  pandas  as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule
import inspect
cur_name = inspect.getfile(inspect.currentframe())#当前文件
cur_path = os.path.dirname(cur_name)#当前目录
conn = sqlite3.connect(f'{cur_path}\\data\\Test.sdb',check_same_thread = False)
#============================================================        
#sqlite3数据库
def s3db_u(sql): #插入、更新
     c=conn.cursor()#创建一个游标对象，调用其execute（）方法来执行SQL语句
     c.execute(sql)#执行SQL指令
     conn.commit()
     re=c.lastrowid#最后插入的自增字段号
     c.close()
     return str(re)
def s3db_pu(sql,datas): #批量插入
     c=conn.cursor()#创建一个游标对象，调用其execute（）方法来执行SQL语句
     c.executemany(sql,datas)#插入多条数据
     conn.commit()
     c.close()     
def s3db_q_list(sql): #查询
     c=conn.cursor()#创建一个游标对象，调用其execute（）方法来执行SQL语句
     c.execute(sql)#执行SQL指令
     resList = c.fetchall()
     c.close()
    # conn.close()  
     return resList
def s3db_q_dict(sql): #查询
     c=conn.cursor(as_dict=True)#创建一个游标对象，调用其execute（）方法来执行SQL语句
     c.execute(sql)#执行SQL指令
     resList = c.fetchall()
     c.close()
     #conn.close()  
     #conn.close()  
     return resList
def s3db_q_pd(sql): #查询
     resList =pd.read_sql(sql,conn)#,dtype='object')
    # conn.close()  
     return resList
def pdtos3tab(df,name): #pd生成表，增加
    df.to_sql(name=name, con=conn, if_exists='append', index=False)
def pd_retab(df,name): #pd生成表,覆盖
    df.to_sql(name=name, con=conn, if_exists='replace', index=False)

