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

# Host="47.92.49.44"
Host="172.26.55.190"
# Host="192.168.1.102"
# Host="localhost"
Port= 12000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
import logging
from logging.handlers import RotatingFileHandler
Rthandler = RotatingFileHandler('log.txt', maxBytes=10*1024*1024,backupCount=5)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)
class Online:
    def GET(self):
        data=web.input(
            callback='',
            is_manager='',
            )
        return_data ={ "success":"0", "error_code":"0","message":""}
        return_more_data={"success":"0", "error_code":"0","message":"","error_intr":""}
        try:
            mycallback = data.callback
            is_manager = data.is_manager
            return_data["success"]=1
            return_more_data["success"]=1
            return_data["message"]="hello world"
            return_more_data["message"]="hello world"
            
        except:
            return_data["error_code"]=101
            return_more_data["error_code"]=101
            return_more_data["error_intr"]="enter data is wrong"
            if is_manager=='':
                return json.dumps(return_data)
            else:
                return json.dumps(return_more_data) 

        finally:
            if mycallback !="":
                if is_manager=='':
                    return mycallback+"("+json.dumps(return_data)+")"
                else:
                    return mycallback+"("+json.dumps(return_more_data)+")"                    
            else:
                if is_manager=='':
                    return json.dumps(return_data)
                else:
                    return json.dumps(return_more_data)

class Control_mac:#设备控制
    def GET(self):
        data=web.input(
            callback='',
            is_manager='',
            )
        return_data ={ "success":"0", "error_code":"0"}
        return_more_data={"success":"0", "error_code":"0","error_intr":""}
        news_data={"state":"","ip_message":"","port_message":""}
        timer_stop="false"
        try:
            mycallback = data.callback
            is_manager = data.is_manager
            user_id=data.user_id          #用户id
            first_type=data.first_type    #一级类型
            second_type=data.second_type        #二级类型
            product_num=data.product_num    #设备编号
            state=data.state        #状态
            info=data.info

        except:
            return_data["error_code"]=101
            return_more_data["error_code"]=101
            return_more_data["error_intr"]="enter data is wrong"
            if is_manager=='':
                return json.dumps(return_data)
            else:
                return json.dumps(return_more_data)

        try:
            Mysql.userWork.Insert_log(user_id,info)
            Num4_message=Mysql.macWork.Product_isExist_inNum4(first_type,second_type,product_num,user_id)
            Num2_message=Mysql.macWork.Product_isExist_inNum2(first_type,second_type,product_num)#获取id，port，6,7
            if Num4_message!=None:
                if Num2_message==None:
                    return_data["error_code"]=105
                    return_more_data["error_code"]=105
                    return_more_data["error_intr"]="data not in form_2,so the send_order hava not ip and port"
                    if is_manager=='':
                        return json.dumps(return_data)
                    else:
                        return json.dumps(return_more_data)
                else:
                    pass                
                Num12_message=Mysql.macWork.Product_isExist_inNum12(first_type,second_type,product_num)       
                Request=Mysql.userWork.Get_last_value() #当前的请求值
                if len(str(Request))==1:
                    Order_request="0000000"+str(Request)
                elif len(str(Request))==2:
                    Order_request="000000"+str(Request)
                elif len(str(Request))==3:
                    Order_request="00000"+str(Request)
                elif len(str(Request))==4:
                    Order_request="0000"+str(Request)
                elif len(str(Request))==5:
                    Order_request="000"+str(Request)
                elif len(str(Request))==6:
                    Order_request="00"+str(Request)
                elif len(str(Request))==7:
                    Order_request="0"+str(Request)
                elif len(str(Request))==8:
                    Order_request=str(Request)#生成指令结尾格式
                Order_send="#"+state+"$"+Order_request+"@"#生成指令，格式如：00_00_00_00000001
                try:
                    if Num12_message != None :#存在的话更新
                        Mysql.userWork.Update_Num12(first_type,second_type,product_num,Request,state)
                    else:
                        Mysql.userWork.Insert_Num12(first_type,second_type,product_num,Request,state)
                except:
                    logging.warning('error_code:105_mac')
                    return_data["error_code"] = 105
                    return_more_data["error_code"]=105
                    return_more_data["error_intr"]="Num12_message have wrong"
                news_data["state"]=Order_send
                news_data["ip_message"]=Num2_message[5]
                news_data["port_message"]=json.dumps(Num2_message[6])
                sock.sendto(json.dumps(news_data),(Host,int(Port)))

                try:
                    while timer_stop=="false":#方便后面暂停
                        Num12_message_for_life=Mysql.macWork.Product_isExist_inNum12(first_type,second_type,product_num)
                        if Num12_message_for_life == None:
                            logging.warning('error_code:in12_life_have_no_data_mac')
                            timer_stop="true"#停止定时器

                        else:                            
                            stop_value=int(Num12_message_for_life[3])
                            time.sleep(1)#1s定时器
                            Timer_message_inNum12=Mysql.userWork.Get_message_inNum12(first_type,second_type,product_num,Num12_message_for_life[3])
                            try:
                                if Timer_message_inNum12 == None:
                                    logging.warning('error_code:in12_have_no_data_mac')
                                    timer_stop="true"#停止定时器
                                else:
                                    if str(Timer_message_inNum12[4])==str(Timer_message_inNum12[5]):#请求值是否等于返回值
                                        Mysql.userWork.Delete_message_inNum12(first_type,second_type,product_num)
                                        return_data["success"]=1
                                        return_more_data["success"]=1
                                        timer_stop="true"#停止定时器

                                    else:
                                        if stop_value==0:#生存值是否为0
                                            Mysql.userWork.Delete_message_inNum12(first_type,second_type,product_num)
                                            return_data["error_code"]=103
                                            return_more_data["error_code"]=103
                                            return_more_data["error_intr"]="_"+return_more_data["error_intr"]+"_product_num"+"_"+str(product_num)+"_send failed"+" and life=0"
                                            timer_stop="true"#停止定时器

                                        else:
                                            if stop_value%2==1:
                                                pass
                                            else:
                                                Num12_message_for_request=Mysql.macWork.Product_isExist_inNum12(first_type,second_type,product_num)
                                                if Num12_message_for_request== None:
                                                    logging.warning('error_code:in12_request_have_no_data_mac')
                                                    timer_stop="true"#停止定时器 
                                                else:                       
                                                    if Num12_message_for_request[4]== Request:#判断当前请求值是否等于数据库的请求值
                                                        sock.sendto(json.dumps(news_data),(Host,int(Port)))
                                                    else:
                                                        timer_stop="true"#停止定时器,因为有新的命令
                                                        return_data["error_code"] = 113
                                                        return_more_data["error_code"]=113
                                                        return_more_data["error_intr"]="there have new order_mac"
                                                        # print "there have new order"
                            except:
                                logging.warning('error_code:222_mac_12_timer')
                                return_data["error_code"] = 222
                                return_more_data["error_code"]=222
                                return_more_data["error_intr"]="timer_12_mac have wrong"                                                      
                except:
                    logging.warning('error_code:104_mac')
                    return_data["error_code"] = 104
                    return_more_data["error_code"]=104
                    return_more_data["error_intr"]="timer have wrong"

            else:
                return_data["error_code"]=110
                return_more_data["error_code"]=110
                return_more_data["error_intr"]="data not in form_4"
                if is_manager=='':
                    return json.dumps(return_data)
                else:
                    return json.dumps(return_more_data)
        except:
            logging.warning('error_code:102_mac')
            return_data["error_code"] = 102
            return_more_data["error_code"]=102
            return_more_data["error_intr"]=" code have wrong"

        finally:
            if mycallback !="":
                if is_manager=='':
                    return mycallback+"("+json.dumps(return_data)+")"
                else:
                    return mycallback+"("+json.dumps(return_more_data)+")"                    
            else:
                if is_manager=='':
                    return json.dumps(return_data)
                else:
                    return json.dumps(return_more_data)

class Control_switch:#设备开关
    def GET(self):
        data=web.input(
            callback='',
            is_manager='',
            )
        return_data ={ "success":"0", "error_code":"0"}
        return_more_data={"success":"0", "error_code":"0","error_intr":""}
        news_data={"state":"","ip_message":"","port_message":""}
        timer_stop="false"
        try:
            mycallback = data.callback
            is_manager = data.is_manager
            first_type=data.first_type    #开关一级类型
            second_type=data.second_type        #开关二级类型
            product_num=data.product_num    #开关编号
            state=data.state        #状态

        except:
            return_data["error_code"]=101
            return_more_data["error_code"]=101
            return_more_data["error_intr"]="enter data is wrong"
            if is_manager=='':
                return json.dumps(return_data)
            else:
                return json.dumps(return_more_data)

        try:
            Num11_message=Mysql.macWork.Product_isExist_inNum11(first_type,second_type,product_num)
            if Num11_message == None :#判断是否在表11
                return_data["error_code"]=106
                return_more_data["error_code"]=106
                return_more_data["error_intr"]="data not in form_11"
            else:
                Request=Mysql.userWork.Get_last_value_switch() #当前的请求值
                Ip_list=[]
                Port_list=[]
                First_type_list=[]
                Second_type_list=[]
                Product_num_list=[]
                for target_message in Num11_message:
                    Num2_message=Mysql.macWork.Product_isExist_inNum2(target_message[3],target_message[4],target_message[5])#获取id，port，6,7
                    Num12_message=Mysql.macWork.Product_isExist_inNum12(target_message[3],target_message[4],target_message[5])

                    try:
                        if Num2_message==None:
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
                                logging.warning('error_code:108_switch')
                                return_data["error_code"] = 108
                                return_more_data["error_code"]=108
                                return_more_data["error_intr"]="check form_12 hava wrong"
                    except:
                        logging.warning('error_code:107_switch')
                        return_data["error_code"] = 107
                        return_more_data["error_code"]=107
                        return_more_data["error_intr"]="check form_2 hava wrong"
                if len(str(Request))==1:
                    Order_request="0000000"+str(Request)
                elif len(str(Request))==2:
                    Order_request="000000"+str(Request)
                elif len(str(Request))==3:
                    Order_request="00000"+str(Request)
                elif len(str(Request))==4:
                    Order_request="0000"+str(Request)
                elif len(str(Request))==5:
                    Order_request="000"+str(Request)
                elif len(str(Request))==6:
                    Order_request="00"+str(Request)
                elif len(str(Request))==7:
                    Order_request="0"+str(Request)
                elif len(str(Request))==8:
                    Order_request=str(Request)#生成指令结尾格式
                Order_send="#"+state+"$"+Order_request+"@"#生成指令，格式如：#00_00_00$00000001@                 
                if len(Ip_list)==0:
                    return_data["error_code"]=105
                    return_more_data["error_code"]=105
                    return_more_data["error_intr"]="data not in form_2,so the send_order hava not ip and port"
                    pass
                else:
                    i=0
                    while i <len(Ip_list):
                        news_data["state"]=Order_send
                        news_data["ip_message"]=Ip_list[i]
                        news_data["port_message"]=json.dumps(Port_list[i])
                        sock.sendto(json.dumps(news_data),(Host,int(Port)))
                        i=i+1

                    try:    
                        while timer_stop=="false":#方便后面暂停
                            Num12_message_for_life=Mysql.macWork.Product_isExist_inNum12(First_type_list[0],Second_type_list[0],Product_num_list[0])
                            if Num12_message_for_life==None:
                                logging.warning('error_code:in12_life_have_no_data_switch')
                                timer_stop="true"#停止定时器
                            else:                               
                                stop_value=Num12_message_for_life[3]
                                time.sleep(1)#1s定时器
                                Device_num=0
                                while Device_num<len(Ip_list):
                                    Timer_message_inNum12=Mysql.userWork.Get_message_inNum12(First_type_list[int(Device_num)],Second_type_list[int(Device_num)],Product_num_list[int(Device_num)],Num12_message_for_life[3])
                                    try:
                                        if Timer_message_inNum12 ==None:
                                            logging.warning('error_code:in12_have_no_data_switch')
                                            timer_stop="true"#停止定时器
                                        else:
                                            if str(Timer_message_inNum12[4])==str(Timer_message_inNum12[5]):#请求值是否等于返回值
                                                if len(Ip_list)==1:
                                                    Mysql.userWork.Delete_message_inNum12(First_type_list[int(Device_num)],Second_type_list[int(Device_num)],Product_num_list[int(Device_num)])
                                                    Device_num=int(Device_num)+1 
                                                    return_data["success"]=1
                                                    return_more_data["success"]=1
                                                    timer_stop="true"#停止定时器

                                                else:
                                                    Mysql.userWork.Delete_message_inNum12(First_type_list[int(Device_num)],Second_type_list[int(Device_num)],Product_num_list[int(Device_num)]) 
                                                    Ip_list.remove(Ip_list[Device_num])
                                                    Port_list.remove(Port_list[Device_num])
                                                    First_type_list.remove(First_type_list[Device_num])
                                                    Second_type_list.remove(Second_type_list[Device_num])
                                                    Product_num_list.remove(Product_num_list[Device_num])

                                            else:
                                                if stop_value==0:#生存值是否为0
                                                    if len(Ip_list)==1:
                                                        return_more_data["error_intr"]="_"+return_more_data["error_intr"]+"_product_num"+"_"+str(Product_num_list[Device_num])+"_send failed"+" and life=0"
                                                        Mysql.userWork.Delete_message_inNum12(First_type_list[int(Device_num)],Second_type_list[int(Device_num)],Product_num_list[int(Device_num)])
                                                        Ip_list.remove(Ip_list[Device_num])
                                                        Port_list.remove(Port_list[Device_num])
                                                        First_type_list.remove(First_type_list[Device_num])
                                                        Second_type_list.remove(Second_type_list[Device_num])
                                                        Product_num_list.remove(Product_num_list[Device_num])
                                                        return_data["error_code"]=103
                                                        return_more_data["error_code"]=103
                                                        timer_stop="true"#停止定时器

                                                    else:
                                                        return_more_data["error_intr"]="_"+return_more_data["error_intr"]+"_product_num"+"_"+str(Product_num_list[Device_num])+"_send failed "
                                                        Mysql.userWork.Delete_message_inNum12(First_type_list[int(Device_num)],Second_type_list[int(Device_num)],Product_num_list[int(Device_num)])
                                                        Ip_list.remove(Ip_list[Device_num])
                                                        Port_list.remove(Port_list[Device_num])
                                                        First_type_list.remove(First_type_list[Device_num])
                                                        Second_type_list.remove(Second_type_list[Device_num])
                                                        Product_num_list.remove(Product_num_list[Device_num])

                                                else:
                                                    if stop_value%2==1:
                                                        Device_num=int(Device_num)+1
                                                        pass 
                                                    else:
                                                        Num12_message_for_request=Mysql.macWork.Product_isExist_inNum12(First_type_list[int(Device_num)],Second_type_list[int(Device_num)],Product_num_list[int(Device_num)])
                                                        if Num12_message_for_request == None:
                                                            logging.warning('error_code:in12_request_have_no_data_switch')
                                                            timer_stop="true"#停止定时器
                                                        else:
                                                            if Num12_message_for_request[4]== Request:#判断当前请求值是否等于数据库的请求值                                   
                                                                # news_data="{"+""" " """+"state"+""" " """+":"+""" " """+Order_send+""" " """+","+""" " """+"ip_message"+""" " """+":"+""" " """+Ip_list[int(Device_num)]+""" " """+","+""" " """+"port_message"+""" " """+":"+json.dumps(Port_list[int(Device_num)])+"}"                 
                                                                # j=0
                                                                # while j<len(Ip_list):
                                                                #     news_data["state"]=Order_send
                                                                #     news_data["ip_message"]=Ip_list[j]
                                                                #     news_data["port_message"]=json.dumps(Port_list[j])
                                                                #     sock.sendto(json.dumps(news_data),(Host,int(Port)))
                                                                #     j=j+1
                                                                news_data["state"]=Order_send
                                                                news_data["ip_message"]=Ip_list[int(Device_num)]
                                                                news_data["port_message"]=json.dumps(Port_list[int(Device_num)])
                                                                sock.sendto(json.dumps(news_data),(Host,int(Port)))
                                                                Device_num=int(Device_num)+1  

                                                            else:
                                                                if len(Ip_list)==1:
                                                                    Device_num=int(Device_num)+1 
                                                                    timer_stop="true"#停止定时器,因为有新的命令
                                                                    return_data["error_code"] = 111
                                                                    return_more_data["error_code"]=111
                                                                    return_more_data["error_intr"]="there have new order_switch,Ip_list=1"

                                                                else:
                                                                    Device_num=int(Device_num)+1
                                                                    if Device_num==len(Ip_list):
                                                                        timer_stop="true"#停止定时器,因为有新的命令
                                                                        return_data["error_code"] = 112
                                                                        return_more_data["error_code"]=112
                                                                        return_more_data["error_intr"]="there have new order_switch"

                                    except:
                                        logging.warning('error_code:223_switch_timer_12')
                                        return_data["error_code"] = 223
                                        return_more_data["error_code"]=223
                                        return_more_data["error_intr"]="timer_12_switch have wrong"                     
                    except:
                        logging.warning('error_code:104_switch_timer')
                        return_data["error_code"] = 104
                        return_more_data["error_code"]=104
                        return_more_data["error_intr"]="timer have wrong"

        except:
            logging.warning('error_code:102_switch')
            return_data["error_code"] = 102
            return_more_data["error_code"]=102
            return_more_data["error_intr"]=" code have wrong"

        finally:
            if mycallback !="":
                if is_manager=='':
                    return mycallback+"("+json.dumps(return_data)+")"
                else:
                    return mycallback+"("+json.dumps(return_more_data)+")"                    
            else:
                if is_manager=='':
                    return json.dumps(return_data)
                else:
                    return json.dumps(return_more_data)
