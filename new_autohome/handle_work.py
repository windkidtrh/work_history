#-*-coding:utf-8-*-
import web
import traceback
import json,demjson
import Mysql.mysql
import Mysql.userWork
import Mysql.macWork
import MySQLdb
import socket
import threading,traceback,time,thread
import logging_set.log_message
import Return_mess.return_mess
reload(sys) 
sys.setdefaultencoding('utf8')
Host = "localhost"
Port = 12000


def error_handle_1(B = '',D = '',Is_manager = '',Callback = '',Error_messsage = '',Status = 0):
    if status == 0 :
        logging_set.log_message.logging.warning(Error_messsage)
        return "None"

    else:
        return  Return_mess.return_mess.return_message(b = B,d = D,is_manager = Is_manager,callback = Callback)


def error_handle_2(Error_messsage1 = '',Error_messsage2 = '',status = 0):
    if status == 0 :
        logging_set.log_message.logging.warning(Error_messsage1)

    else:
        logging_set.log_message.logging.warning(Error_messsage2)



def for_handle(first_type,second_type,product_num,state,info,status = 0,mess_get = '',news_data = '',is_manager = '',mycallback = ''):
    timer_stop = "false"
    try:
        Num11_message = Mysql.macWork.Product_isExist_inNum11(first_type,second_type,product_num)
        if Num11_message == None :#判断是否在表11
            mess_get = error_handle_1(
            	B=106,
            	D="data not in form_11",
            	is_manager,
            	mycallback,
            	Error_message='error_code:106_udp_third_not_in_11',
            	Status=status)

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
                                Mysql.userWork.Update_Num12(target_message[3],target_message[4],target_message[5],Request,json.dumps(State))

                            else :
                                Mysql.userWork.Insert_Num12(target_message[3],target_message[4],target_message[5],Request,json.dumps(State))

                        except:
                            mess_get = error_handle_1(
                            	B=108,
                            	D="check form_12 hava wrong",
                            	is_manager,
                            	mycallback,
                            	Error_message='error_code:108_udp_third',
                            	Status=status)

                except:
                    mess_get = error_handle_1(
                    	B=107,
                    	D="check form_2 hava wrong",
                    	is_manager,
                    	mycallback,
                    	Error_message='error_code:107_udp_third',
                    	Status=status)

            Order_request = Return_mess.return_mess.Request_mess(Request)

            Order_send = ''
            if status == 0:
                Order_send = "#" + str(state["current_status"]) + "$" + Order_request + "@"#生成指令，格式如：00_00_00_00000001                    

            else:
                Order_send = "#" + state + "$" + Order_request + "@"#生成指令，格式如：#00_00_00$00000001@                    

            if len(Ip_list) == 0:
                mess_get = error_handle_1(
                	B=105,
                	D="data not in form_2,so the send_order hava not ip and port",
                	is_manager,
                	mycallback,
                	Error_message='error_code:105_udp_third_not_in_2',
                	Status=status)
                pass

            else:                
                i = 0
                while i < len(Ip_list):
                    if status == 0: 
                        socket.sendto(Order_send,(Ip_list[i],Port_list[i]))
                        i = i + 1

                    else:
                    	news_data = Return_mess.return_mess.return_message_datas(Order_send,Ip_list[i],json.dumps(Port_list[i]))
                        sock.sendto(json.dumps(news_data),(Host,int(Port)))
                        i = i + 1
                try:   
                    while timer_stop == "false":#方便后面暂停
                        def remove_list(num_list):
                            Ip_list.remove(Ip_list[num_list])
                            Port_list.remove(Port_list[num_list])
                            First_type_list.remove(First_type_list[num_list])
                            Second_type_list.remove(Second_type_list[num_list])
                            Product_num_list.remove(Product_num_list[num_list])  

                        Num12_message_for_life = Mysql.macWork.Product_isExist_inNum12(First_type_list[0],Second_type_list[0],Product_num_list[0])
                        if Num12_message_for_life == None:
                            error_handle_2(
                            	Error_messsage1 = 'error_code:in12_life_have_no_data_udp',
                            	Error_messsage2 = 'error_code:in12_life_have_no_data_switch',
                            	status = status) 
                            timer_stop = "true"#停止定时器

                        else:
                            stop_value = Num12_message_for_life[3]
                            time.sleep(1)#1s定时器
                            Device_num = 0

                            while Device_num < len(Ip_list):
                                Timer_message_inNum12 = Mysql.userWork.Get_message_inNum12(First_type_list[int(Device_num)],Second_type_list[int(Device_num)],Product_num_list[int(Device_num)],Num12_message_for_life[3])

                                try:
                                    if Timer_message_inNum12 == None:
                                        error_handle_2(
                                        	Error_messsage1 = 'error_code:in12_have_no_data_udp',
                                        	Error_messsage2 = 'error_code:in12_have_no_data_switch',
                                        	status = status)
                                        timer_stop = "true"#停止定时器

                                    else:
                                        def Delete_12(Device_num):
                                            Mysql.userWork.Delete_message_inNum12(First_type_list[int(Device_num)],Second_type_list[int(Device_num)],Product_num_list[int(Device_num)])

                                        if str(Timer_message_inNum12[4]) == str(Timer_message_inNum12[5]):#请求值是否等于返回值
                                            if len(Ip_list) == 1:
                                                Delete_12(Device_num)
                                                Device_num = int(Device_num) + 1 
                                                if status != 0:
                                                    mess_get = Return_mess.return_mess.return_message(
                                                    	a = 1,
                                                    	callback = mycallback)
                                                    
                                                timer_stop = "true"#停止定时器

                                            else:
                                                Delete_12(Device_num)
                                                remove_list(Device_num)

                                        else:
                                            if stop_value == 0:#生存值是否为0
                                                if len(Ip_list) == 1:
                                                    Delete_12(Device_num)
                                                    remove_list(Device_num)
                                                    error_handle_2(
                                                    	Error_messsage1 = 'error_code:109_udp_third_life==0,delete,Ip_list=1',
                                                    	Error_messsage2 = 'error_code:109_switch_life==0,delete,Ip_list=1',
                                                    	status = status)
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
                                                        error_handle_2(
                                                        	Error_messsage1 = 'error_code:in12_request_have_no_data_udp',
                                                        	Error_messsage2 = 'error_code:in12_request_have_no_data_switch',
                                                        	status = status)                                                            
                                                        timer_stop = "true"#停止定时器

                                                    else: 
                                                        if Num12_message_for_request[4] == Request:#判断当前请求值是否等于数据库的请求值
                                                            if status == 0:
                                                                socket.sendto(Order_send,(Ip_list[int(Device_num)],Port_list[int(Device_num)]))
                                                            
                                                            else:
                                                                news_data = Return_mess.return_mess.return_message_datas(Order_send,Ip_list[int(Device_num)],json.dumps(Port_list[int(Device_num)]))
                                                                sock.sendto(json.dumps(news_data),(Host,int(Port)))
                                                                
                                                            Device_num = int(Device_num) + 1  

                                                        else:
                                                            if len(Ip_list) == 1:
                                                                Device_num = int(Device_num) + 1 
                                                                timer_stop = "true"#停止定时器,因为有新的命令
                                                                mess_get = error_handle_1(
                                                                	B=111,
                                                                	D="there have new order_switch,Ip_list=1",
                                                                	is_manager,
                                                                	mycallback,
                                                                	Status=status)

                                                            else:

                                                                Device_num = int(Device_num) + 1
                                                                if Device_num == len(Ip_list):
                                                                    timer_stop = "true"#停止定时器,因为有新的命令
                                                                    mess_get = error_handle_1(
                                                                    	B=112,
                                                                    	D="there have new order_switch",
                                                                    	is_manager,
                                                                    	mycallback,
                                                                    	Status=status)


                                except:
                                    mess_get = error_handle_1(
                                    	B=223,
                                    	D="timer_12_switch have wrong",
                                    	is_manager,
                                    	mycallback,
                                    	Error_message='error_code:222_udp_third',
                                    	Status=status)
    
                except:
                    mess_get = error_handle_1(
                    	B=104,
                    	D="timer hava wrong",
                    	is_manager,
                    	mycallback,
                    	Error_message='error_code:104_udp_third',
                    	Status=status)

    except:
        mess_get = error_handle_1(
        	B=197,
        	D="handle_work_error_switch",
        	is_manager,
        	mycallback,
        	Error_message='handle_work_error_udp',
        	Status=status)


    finally:
        if status == 0:
            pass

        else:
        	return mess_get