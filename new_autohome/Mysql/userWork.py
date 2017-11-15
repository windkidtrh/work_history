#-*-coding:utf-8-*- 
import mysql
import MySQLdb
import time
TIMEFORMAT= "%Y.%m.%d.%H.%M.%S"
def Get_last_value():
   # return "hah1"
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="select last_value from save_tmp_value where id=1"
        cur.execute(sql1)
        result=cur.fetchone()
        conn.commit()
        cur.close()

        if result[0]==99999999:
            renew=1
            cur = conn.cursor()
            sql2="update save_tmp_value set last_value='%s' where id=1"%(renew)
            cur.execute(sql2)
            conn.commit()
            cur.close()        
            return renew
        else:
            cur = conn.cursor()
            sql3="update save_tmp_value set last_value='%s' where id=1"%(result[0]+1)
            cur.execute(sql3)
            conn.commit()
            cur.close()        
            return result[0]+1

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Get_last_value_switch():
   # return "hah1"
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="select last_value from save_tmp_value where id=2"
        cur.execute(sql1)
        result=cur.fetchone()
        conn.commit()
        cur.close()

        if result[0]==99999999:
            renew=1
            cur = conn.cursor()
            sql2="update save_tmp_value set last_value='%s' where id=2"%(renew)
            cur.execute(sql2)
            conn.commit()
            cur.close()        
            return renew
        else:
            cur = conn.cursor()
            sql3="update save_tmp_value set last_value='%s' where id=2"%(result[0]+1)
            cur.execute(sql3)
            conn.commit()
            cur.close()        
            return result[0]+1

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Get_message_inNum12(First_type,Second_type,Product_num,Life):
   # return "hah1"
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql="update manage_request set life='%s' where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(int(Life)-1,First_type,Second_type,Product_num)
        cur.execute(sql)
        conn.commit()
        cur.close()

        cur = conn.cursor()
        sql1="select * from manage_request where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(First_type,Second_type,Product_num)
        cur.execute(sql1)
        result=cur.fetchone()
        conn.commit()
        cur.close()
        return result

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Delete_message_inNum12(First_type,Second_type,Product_num):
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="delete from manage_request where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(First_type,Second_type,Product_num)
        cur.execute(sql1)
        result=cur.fetchone()
        conn.commit()
        cur.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])    

def Update_Num12(First_type,Second_type,Product_num,Request_value,State):
   # return "hah1"
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="update manage_request set life='%s',request_value='%s',state='%s' where(first_type,second_type,product_num) in (('%s','%s','%s'))"%(6,Request_value,State,First_type,Second_type,Product_num)
        cur.execute(sql1)
        conn.commit()
        cur.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Insert_Num12(First_type,Second_type,Product_num,Request_value,State):
   # return "hah1"
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="insert into manage_request(first_type,second_type,product_num,life,request_value,return_value,state) values ('%s','%s','%s','%s','%s','%s','%s')"%(First_type,Second_type,Product_num,6,int(Request_value),0,State)
        cur.execute(sql1)
        conn.commit()
        cur.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Insert_log(User_id,Info):
   # return "hah1"
    try:
        Current_time=time.strftime(TIMEFORMAT,time.localtime())
        # Current_time=time.ctime()
        # return Current_time
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="insert into log(user_id,the_time,info) values ('%s','%s','%s')"%(User_id,str(Current_time),Info)
        # return sql1
        cur.execute(sql1)
        conn.commit()
        cur.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Insert_log_switch(First_type,Second_type,Product_num,Info):
   # return "hah1"
    try:
        Current_time=time.strftime(TIMEFORMAT,time.localtime())
        # Current_time=time.ctime()
        # return Current_time
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="insert into log_switch(first_type,second_type,product_num,the_time,info) values ('%s','%s','%s','%s','%s')"%(First_type,Second_type,Product_num,str(Current_time),Info)
        # return sql1
        cur.execute(sql1)
        conn.commit()
        cur.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Insert_log_drive(First_type,Second_type,Device_nums,Current_status,Info):
   # return "hah1"
    try:
        Current_time=time.strftime(TIMEFORMAT,time.localtime())
        # Current_time=time.ctime()
        # return Current_time
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="insert into log_drive(first_type,second_type,device_nums,the_time,current_status,info) values ('%s','%s','%s','%s','%s','%s')"%(First_type,Second_type,Device_nums,str(Current_time),Current_status,Info)
        # return sql1
        cur.execute(sql1)
        conn.commit()
        cur.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])