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
            mess_get = Return_mess.return_mess.return_message(a = 1,c = "hello world",callback = mycallback)

        except:
            mess_get = Return_mess.return_mess.return_message(b = 101,c = "hello world",d = "enter data is wrong",is_manager = is_manager,callback = mycallback)
 
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
            mess_get = Return_mess.return_mess.return_message(b = 101,d = "enter data is wrong",is_manager = is_manager,callback = mycallback)

        try:

            Mysql.userWork.Insert_log(user_id,info)
            Num4_message = Mysql.macWork.Product_isExist_inNum4(first_type,second_type,product_num,user_id)
            Num2_message = Mysql.macWork.Product_isExist_inNum2(first_type,second_type,product_num)#获取id，port，6,7

            if Num4_message != None:
                if Num2_message == None:
                    mess_get = Return_mess.return_mess.return_message(b = 105,d = "data not in form_2,so the send_order hava not ip and port",is_manager = is_manager,callback = mycallback)
                
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
                    logging_set.log_message.logging.warning('error_code:105_mac')
                    mess_get = Return_mess.return_mess.return_message(b = 109,d = "Num12_message have wrong",is_manager = is_manager,callback = mycallback)

                news_data = Return_mess.return_mess.return_message_datas(Order_send,Num2_message[5],json.dumps(Num2_message[6]))
                sock.sendto(json.dumps(news_data),(Host,int(Port)))

                try:
                    while timer_stop == "false":#方便后面暂停

                        Num12_message_for_life = Mysql.macWork.Product_isExist_inNum12(first_type,second_type,product_num)

                        if Num12_message_for_life == None:
                            logging_set.log_message.logging.warning('error_code:in12_life_have_no_data_mac')
                            timer_stop = "true"#停止定时器

                        else:                            
                            stop_value = int(Num12_message_for_life[3])
                            time.sleep(1)#1s定时器
                            Timer_message_inNum12 = Mysql.userWork.Get_message_inNum12(first_type,second_type,product_num,Num12_message_for_life[3])

                            try:
                                if Timer_message_inNum12 == None:
                                    logging_set.log_message.logging.warning('error_code:in12_have_no_data_mac')
                                    timer_stop = "true"#停止定时器

                                else:
                                    if str(Timer_message_inNum12[4]) == str(Timer_message_inNum12[5]):#请求值是否等于返回值
                                        Mysql.userWork.Delete_message_inNum12(first_type,second_type,product_num)
                                        mess_get = Return_mess.return_mess.return_message(a = 1,callback = mycallback)
                                        timer_stop = "true"#停止定时器

                                    else:
                                        if stop_value == 0:#生存值是否为0
                                            Mysql.userWork.Delete_message_inNum12(first_type,second_type,product_num)
                                            mess_get = Return_mess.return_mess.return_message(b = 103,d = "product_num"+"_"+str(product_num)+"_send failed"+" and life=0",is_manager = is_manager,callback = mycallback)
                                            timer_stop = "true"#停止定时器

                                        else:
                                            if stop_value % 2 == 1:
                                                pass

                                            else:
                                                Num12_message_for_request = Mysql.macWork.Product_isExist_inNum12(first_type,second_type,product_num)

                                                if Num12_message_for_request == None:
                                                    logging_set.log_message.logging.warning('error_code:in12_request_have_no_data_mac')
                                                    timer_stop = "true"#停止定时器 

                                                else:                       
                                                    if Num12_message_for_request[4] == Request:#判断当前请求值是否等于数据库的请求值
                                                        sock.sendto(json.dumps(news_data),(Host,int(Port)))

                                                    else:
                                                        timer_stop = "true"#停止定时器,因为有新的命令
                                                        mess_get = Return_mess.return_mess.return_message(b = 113,d = "there have new order_mac",is_manager = is_manager,callback = mycallback)

                            except:
                                logging_set.log_message.logging.warning('error_code:222_mac_12_timer')
                                mess_get = Return_mess.return_mess.return_message(b = 222,d = "timer_12_mac have wrong",is_manager = is_manager,callback = mycallback)
                              
                except:
                    logging_set.log_message.logging.warning('error_code:104_mac')
                    mess_get = Return_mess.return_mess.return_message(b = 104,d = "timer have wrong",is_manager = is_manager,callback = mycallback)

            else:
                logging_set.log_message.logging.warning('error_code:110_mac')
                mess_get = Return_mess.return_mess.return_message(b = 110,d = "data not in form_4",is_manager = is_manager,callback = mycallback)                

        except:
            logging_set.log_message.logging.warning('error_code:102_mac')
            mess_get = Return_mess.return_mess.return_message(b = 102,d = "code have wrong",is_manager = is_manager,callback = mycallback)

        finally:
            return mess_get

class Control_switch:#设备开关
    def GET(self):
        data=web.input(
            callback='',
            is_manager='',
            )
        timer_stop = "false"
        mess_get = ''
        news_data = ''

        try:
            mycallback = data.callback
            is_manager = data.is_manager
            first_type = data.first_type    #开关一级类型
            second_type = data.second_type        #开关二级类型
            product_num = data.product_num    #开关编号
            state = data.state        #状态

        except:
            mess_get = Return_mess.return_mess.return_message(b = 101,d = "enter data is wrong",is_manager = is_manager,callback = mycallback)

        try:
            Num11_message=Mysql.macWork.Product_isExist_inNum11(first_type,second_type,product_num)
            if Num11_message == None :#判断是否在表11
                mess_get = Return_mess.return_mess.return_message(b = 106,d = "data not in form_11",is_manager = is_manager,callback = mycallback)

            else:
                Request = Mysql.userWork.Get_last_value(2) #当前的请求值
                Ip_list = []
                Port_list = []
                First_type_list = []
                Second_type_list = []
                Product_num_list = []

                for target_message in Num11_message:
                    Num2_message = Mysql.macWork.Product_isExist_inNum2(target_message[3],target_message[4],target_message[5])#获取id，port，6,7
                    Num12_message = Mysql.macWork.Product_isExist_inNum12(target_message[3],target_message[4],target_message[5])

                    try:
                        if Num2_message == None:
                            pass

                        else:
                            Ip_list.append(Num2_message[5])
                            Port_list.append(Num2_message[6])
                            First_type_list.append(target_message[3])
                            Second_type_list.append(target_message[4])
                            Product_num_list.append(target_message[5])

                            try:
                                if Num12_message != None:
                                    Mysql.userWork.Update_Num12(target_message[3],target_message[4],target_message[5],Request,state)

                                else :
                                    Mysql.userWork.Insert_Num12(target_message[3],target_message[4],target_message[5],Request,state)

                            except:
                                logging_set.log_message.logging.warning('error_code:108_switch')
                                mess_get = Return_mess.return_mess.return_message(b = 108,d = "check form_12 hava wrong",is_manager = is_manager,callback = mycallback)

                    except:
                        logging_set.log_message.logging.warning('error_code:107_switch')
                        mess_get = Return_mess.return_mess.return_message(b = 107,d = "check form_2 hava wrong",is_manager = is_manager,callback = mycallback)

                Order_request = Return_mess.return_mess.Request_mess(Request)
                Order_send = "#" + state + "$" + Order_request + "@"#生成指令，格式如：#00_00_00$00000001@                    
    
                if len(Ip_list)==0:
                   mess_get = Return_mess.return_mess.return_message(b = 105,d = "data not in form_2,so the send_order hava not ip and port",is_manager = is_manager,callback = mycallback)
                   pass

                else:
                    i = 0
                    while i < len(Ip_list):
                        news_data = Return_mess.return_mess.return_message_datas(Order_send,Ip_list[i],json.dumps(Port_list[i]))
                        sock.sendto(json.dumps(news_data),(Host,int(Port)))
                        i = i + 1

                    try:    
                        while timer_stop=="false":#方便后面暂停
                            def remove_list(num_list):
                                Ip_list.remove(Ip_list[num_list])
                                Port_list.remove(Port_list[num_list])
                                First_type_list.remove(First_type_list[num_list])
                                Second_type_list.remove(Second_type_list[num_list])
                                Product_num_list.remove(Product_num_list[num_list])

                            Num12_message_for_life = Mysql.macWork.Product_isExist_inNum12(First_type_list[0],Second_type_list[0],Product_num_list[0])
                            if Num12_message_for_life == None:
                                logging_set.log_message.logging.warning('error_code:in12_life_have_no_data_switch')
                                timer_stop = "true"#停止定时器

                            else:                               
                                stop_value = Num12_message_for_life[3]
                                time.sleep(1)#1s定时器
                                Device_num = 0

                                while Device_num < len(Ip_list):
                                    Timer_message_inNum12 = Mysql.userWork.Get_message_inNum12(First_type_list[int(Device_num)],Second_type_list[int(Device_num)],Product_num_list[int(Device_num)],Num12_message_for_life[3])
                                    try:
                                        if Timer_message_inNum12 == None:
                                            logging_set.log_message.logging.warning('error_code:in12_have_no_data_switch')
                                            timer_stop = "true"#停止定时器
                                        
                                        else:
                                            def Delete_12(Device_num):
                                                Mysql.userWork.Delete_message_inNum12(First_type_list[int(Device_num)],Second_type_list[int(Device_num)],Product_num_list[int(Device_num)])        

                                            if str(Timer_message_inNum12[4]) == str(Timer_message_inNum12[5]):#请求值是否等于返回值
                                                if len(Ip_list) == 1:
                                                    Delete_12(Device_num)
                                                    Device_num = int(Device_num) + 1 
                                                    mess_get = Return_mess.return_mess.return_message(a = 1,callback = mycallback)
                                                    timer_stop = "true"#停止定时器

                                                else:
                                                    Delete_12(Device_num)
                                                    remove_list(Device_num)

                                            else:
                                                if stop_value == 0:#生存值是否为0
                                                    if len(Ip_list) == 1:
                                                        Delete_12(Device_num)
                                                        remove_list(Device_num)
                                                        mess_get = Return_mess.return_mess.return_message(b = 103,d="send failed and life = 0",is_manager = is_manager,callback = mycallback)
                                                        timer_stop = "true"#停止定时器


                                                    else:
                                                        Delete_12(Device_num)
                                                        remove_list(Device_num)

                                                else:
                                                    if stop_value % 2 == 1:
                                                        Device_num = int(Device_num) + 1
                                                        pass 

                                                    else:
                                                        Num12_message_for_request = Mysql.macWork.Product_isExist_inNum12(First_type_list[int(Device_num)],Second_type_list[int(Device_num)],Product_num_list[int(Device_num)])
                                                        if Num12_message_for_request == None:
                                                            logging_set.log_message.logging.warning('error_code:in12_request_have_no_data_switch')
                                                            timer_stop = "true"#停止定时器

                                                        else:
                                                            if Num12_message_for_request[4] == Request:#判断当前请求值是否等于数据库的请求值                                   
                                                                news_data = Return_mess.return_mess.return_message_datas(Order_send,Ip_list[int(Device_num)],json.dumps(Port_list[int(Device_num)]))
                                                                sock.sendto(json.dumps(news_data),(Host,int(Port)))
                                                                Device_num = int(Device_num) + 1  

                                                            else:
                                                                if len(Ip_list) == 1:
                                                                    Device_num = int(Device_num) + 1 
                                                                    timer_stop = "true"#停止定时器,因为有新的命令
                                                                    mess_get = Return_mess.return_mess.return_message(b = 111,d = "there have new order_switch,Ip_list=1",is_manager = is_manager,callback = mycallback)

                                                                else:
                                                                    Device_num = int(Device_num)+1
                                                                    if Device_num == len(Ip_list):
                                                                        timer_stop = "true"#停止定时器,因为有新的命令
                                                                        mess_get = Return_mess.return_mess.return_message(b = 112,d = "there have new order_switch",is_manager = is_manager,callback = mycallback)

                                    except:
                                        logging_set.log_message.logging.warning('error_code:223_switch_timer_12')
                                        mess_get = Return_mess.return_mess.return_message(b = 223,d = "timer_12_switch have wrong",is_manager = is_manager,callback = mycallback)
                
                    except:
                        logging_set.log_message.logging.warning('error_code:104_switch_timer')
                        mess_get = Return_mess.return_mess.return_message(b = 104,d = "timer have wrong",is_manager = is_manager,callback = mycallback)

        except:
            logging_set.log_message.logging.warning('error_code:102_switch')
            mess_get = Return_mess.return_mess.return_message(b = 107,d = "code have wrong",is_manager = is_manager,callback = mycallback)

        finally:
            return mess_get