#-*-coding:utf-8-*-
import web
import traceback
import json
import Mysql.mysql
import Mysql.userWork
import Mysql.macWork
import MySQLdb
import socket
import time
import logging_set.log_message
import Return_mess.return_mess
import handle_work
import sys
sys.path.append("..")
Host = "localhost"
Port = 12000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class Online:
    def GET(self):
        data = web.input(
            callback = '',
            is_manager = '',
            )
        mess_get = ''

        try:
            mycallback = data.callback
            is_manager = data.is_manager
            mess_get = Return_mess.return_mess.return_message(
                a = 1,
                c = "hello world",
                callback = mycallback)

        except:
            mess_get = Return_mess.return_mess.return_message(
                b = 101,
                c = "hello world",
                d = "enter data is wrong",
                is_manager = is_manager,
                callback = mycallback)
 
        finally:
            return mess_get


class Control_mac:#设备控制
    def GET(self):
        data = web.input(
            callback = '',
            is_manager = '',
            )
        mess_get = ''
        news_data = ''
        timer_stop = "false"

        try:
            mycallback = data.callback
            is_manager = data.is_manager
            user_id = data.user_id          #用户id
            first_type = data.first_type    #一级类型
            second_type = data.second_type        #二级类型
            product_num = data.product_num    #设备编号
            state = data.state        #状态
            info = data.info

        except:
            mess_get = Return_mess.return_mess.return_message(
                b = 101,
                d = "enter data is wrong",
                is_manager = is_manager,
                callback = mycallback)

        try:

            Mysql.userWork.Insert_log(user_id,info)
            Num4_message = Mysql.macWork.Product_isExist_inNum4(first_type,second_type,product_num,user_id)
            Num2_message = Mysql.macWork.Product_isExist_inNum2(first_type,second_type,product_num)#获取id，port，6,7

            if Num4_message != None:
                if Num2_message == None:
                    mess_get = Return_mess.return_mess.return_message(
                        b = 105,
                        d = "data not in form_2,so the send_order hava not ip and port",
                        is_manager = is_manager,
                        callback = mycallback)
                
                else:
                    pass  

                Num12_message = Mysql.macWork.Product_isExist_inNum12(first_type,second_type,product_num)       
                Request = Mysql.userWork.Get_last_value() #当前的请求值
                Order_request = Return_mess.return_mess.Request_mess(Request)
                Order_send = "#" + state + "$" + Order_request + "@"
                
                try:
                    if Num12_message != None :#存在的话更新
                        Mysql.userWork.Update_Num12(first_type,second_type,product_num,Request,state)

                    else:
                        Mysql.userWork.Insert_Num12(first_type,second_type,product_num,Request,state)

                except:
                    mess_get = Return_mess.return_mess.return_message(
                        b = 109,
                        d = "Num12_message have wrong",
                        is_manager = is_manager,
                        callback = mycallback)

                news_data = Return_mess.return_mess.return_message_datas(Order_send,Num2_message[5],json.dumps(Num2_message[6]))
                sock.sendto(json.dumps(news_data),(Host,int(Port)))

                try:
                    while timer_stop == "false":#方便后面暂停

                        Num12_message_for_life = Mysql.macWork.Product_isExist_inNum12(first_type,second_type,product_num)

                        if Num12_message_for_life == None:
                            mess_get = Return_mess.return_mess.return_message(
                                b = 139,
                                d = 'error_code:in12_life_have_no_data_mac',
                                is_manager = is_manager,
                                callback = mycallback)       
                            timer_stop = "true"#停止定时器

                        else:                            
                            stop_value = int(Num12_message_for_life[3])
                            time.sleep(1)#1s定时器
                            Timer_message_inNum12 = Mysql.userWork.Get_message_inNum12(first_type,second_type,product_num,Num12_message_for_life[3])

                            try:
                                if Timer_message_inNum12 == None:
                                    mess_get = Return_mess.return_mess.return_message(
                                        b = 129,
                                        d = 'error_code:in12_have_no_data_mac',
                                        is_manager = is_manager,
                                        callback = mycallback)
                                    timer_stop = "true"#停止定时器

                                else:
                                    if str(Timer_message_inNum12[4]) == str(Timer_message_inNum12[5]):#请求值是否等于返回值
                                        Mysql.userWork.Delete_message_inNum12(first_type,second_type,product_num)
                                        mess_get = Return_mess.return_mess.return_message(
                                            a = 1,
                                            callback = mycallback)
                                        timer_stop = "true"#停止定时器

                                    else:
                                        if stop_value == 0:#生存值是否为0
                                            Mysql.userWork.Delete_message_inNum12(first_type,second_type,product_num)
                                            mess_get = Return_mess.return_mess.return_message(
                                                b = 103,
                                                d = "product_num"+"_"+str(product_num)+"_send failed"+" and life=0",
                                                is_manager = is_manager,
                                                callback = mycallback)
                                            timer_stop = "true"#停止定时器

                                        else:
                                            if stop_value % 2 == 1:
                                                pass

                                            else:
                                                Num12_message_for_request = Mysql.macWork.Product_isExist_inNum12(first_type,second_type,product_num)

                                                if Num12_message_for_request == None:
                                                    mess_get = Return_mess.return_mess.return_message(
                                                        b = 119,
                                                        d = 'error_code:in12_request_have_no_data_mac',
                                                        is_manager = is_manager,
                                                        callback = mycallback)
                                                    timer_stop = "true"#停止定时器 

                                                else:                       
                                                    if Num12_message_for_request[4] == Request:#判断当前请求值是否等于数据库的请求值
                                                        sock.sendto(json.dumps(news_data),(Host,int(Port)))

                                                    else:
                                                        timer_stop = "true"#停止定时器,因为有新的命令
                                                        mess_get = Return_mess.return_mess.return_message(
                                                            b = 113,
                                                            d = "there have new order_mac",
                                                            is_manager = is_manager,
                                                            callback = mycallback)

                            except:
                                mess_get = Return_mess.return_mess.return_message(
                                    b = 222,
                                    d = "timer_12_mac have wrong",
                                    is_manager = is_manager,
                                    callback = mycallback)
                              
                except:
                    mess_get = Return_mess.return_mess.return_message(
                        b = 104,
                        d = "timer have wrong",
                        is_manager = is_manager,
                        callback = mycallback)

            else:
                mess_get = Return_mess.return_mess.return_message(
                    b = 110,
                    d = "data not in form_4",
                    is_manager = is_manager,
                    callback = mycallback)                

        except:
            mess_get = Return_mess.return_mess.return_message(
                b = 102,
                d = "code have wrong",
                is_manager = is_manager,
                callback = mycallback)

        finally:
            return mess_get


class Control_switch:#设备开关
    def GET(self):
        data=web.input(
            callback='',
            is_manager='',
            )

        mess_get = ''
        news_data = ''

        try:
            mycallback = data.callback
            is_manager = data.is_manager
            first_type = data.first_type    #开关一级类型
            second_type = data.second_type        #开关二级类型
            product_num = data.product_num    #开关编号
            state = data.state        #状态
            info = data.info
            Mysql.userWork.Insert_log_switch(first_type,second_type,product_num,info)

        except:
            mess_get = Return_mess.return_mess.return_message(
                b = 101,
                d = "enter data is wrong",
                is_manager = is_manager,
                callback = mycallback)

        try:
            mess_get = handle_work.for_handle(first_type,second_type,product_num,state,info,status = 1,mess_get,news_data,is_manager,mycallback)

        except:
            mess_get = Return_mess.return_mess.return_message(
                b = 107,
                d = "code have wrong",
                is_manager = is_manager,
                callback = mycallback)

        finally:
            return mess_get