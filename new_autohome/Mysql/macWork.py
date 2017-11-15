#-*-coding:utf-8-*- 
import mysql
import MySQLdb

def Product_isExist_inNum2(First_type,Second_type,Product_num):
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="select * from product_current_state where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(First_type,Second_type,Product_num)
        cur.execute(sql1)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        return result

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Product_isExist_inNum12(First_type,Second_type,Product_num):
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="select * from manage_request where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(First_type,Second_type,Product_num)
        cur.execute(sql1)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        return result

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Product_isExist_inNum11(First_type,Second_type,Product_num):
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql="select * from switch_join_device where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(First_type,Second_type,Product_num)
        cur.execute(sql)
        result = cur.fetchone()
        conn.commit()
        cur.close()

        cur = conn.cursor()
        sql1="select * from switch_join_device where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(First_type,Second_type,Product_num)
        cur.execute(sql1)
        result1 = cur.fetchall()
        conn.commit()
        cur.close()
        if result==None:
            return result
        else:
            return result1

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Product_inNum8(First_type,Second_type):
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="select * from product_description where (first_type,second_type) in (('%s','%s'))"%(First_type,Second_type)
        cur.execute(sql1)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        return result

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Product_isExist_inNum4(First_type,Second_type,Product_num,User_id):
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="select * from product_belong_to where (first_type,second_type,product_num,user_id) in (('%s','%s','%s','%s'))"%(First_type,Second_type,Product_num,User_id)
        cur.execute(sql1)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        return result

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Product_isExist_inNum1(First_type,Second_type,Product_num):
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="select * from product where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(First_type,Second_type,Product_num)
        cur.execute(sql1)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        return result

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def Register_mac(First_type,Second_type,Product_num,Current_state,Ip_address,Net_port):
   # return "hah1"
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="insert into product_current_state(first_type,second_type,product_num,current_state,ip_address,net_port,online_value) values ('%s','%s','%s','%s','%s','%s','%s')"%(First_type,Second_type,Product_num,Current_state,Ip_address,Net_port,2)
        cur.execute(sql1)
        conn.commit()
        cur.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Update_mac(First_type,Second_type,Product_num,Current_state,Ip_address,Net_port):
   # return "hah1"
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="update product_current_state set current_state='%s',ip_address='%s',net_port='%s',online_value='%s' where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(Current_state,Ip_address,Net_port,2,First_type,Second_type,Product_num)
        cur.execute(sql1)
        conn.commit()
        cur.close()

        # cur = conn.cursor()
        # sql2="select belong_id from product_current_state where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(First_type,Second_type,Product_num)
        # cur.execute(sql2)
        # result = cur.fetchone()
        # conn.commit()
        # cur.close()

        # cur = conn.cursor()
        # sql3="select * from product_belong_to where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(First_type,Second_type,Product_num)
        # cur.execute(sql3)
        # result1 = cur.fetchone()
        # conn.commit()
        # cur.close()

        # if result1 != None:
        #     cur = conn.cursor()
        #     sql4="update product_belong_to set user_id='%s' where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(result[0],First_type,Second_type,Product_num)
        #     cur.execute(sql4)
        #     conn.commit()
        #     cur.close()
        # else:
        #     pass
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Update_Return_value(First_type,Second_type,Product_num,Request):
   # return "hah1"
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql1="update manage_request set return_value='%s' where (first_type,second_type,product_num) in (('%s','%s','%s'))"%(Request,First_type,Second_type,Product_num)
        cur.execute(sql1)
        conn.commit()
        cur.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def Mac_is_not_in():
   # return "hah1"
    try:
        conn=mysql.connect_mysql()
        cur = conn.cursor()
        sql="select * from product_current_state"
        cur.execute(sql)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        # return result
        cur = conn.cursor()
        sql1="select * from product_current_state"
        cur.execute(sql1)
        result1 = cur.fetchall()
        conn.commit()
        cur.close()
        # return result1
        if result == None:
            pass
        else:
            for i in result1:
                cur = conn.cursor()
                sql1="update product_current_state set online_value='%s' where belong_id='%s'"%(int(i[7])-1,i[8])
                cur.execute(sql1)
                conn.commit()
                cur.close()
            cur = conn.cursor()
            sql2="delete from product_current_state where online_value='%s'"%(0)
            cur.execute(sql2)
            conn.commit()
            cur.close()                

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])