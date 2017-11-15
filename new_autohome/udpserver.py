#-*-coding:utf-8-*-
import SocketServer,socket,json,demjson
import threading,traceback,time,thread
import Mysql.mysql
import Mysql.macWork
import Mysql.userWork
import logging_set.log_message
import Return_mess.return_mess
import handle_work
reload(sys) 
sys.setdefaultencoding('utf8')
HOST = "localhost"
PORT = 12000


def cut_online_value():
    thread.start_new_thread(Mysql.macWork.Mac_is_not_in,())
    timer = threading.Timer(150,cut_online_value)
    timer.start()
timer = threading.Timer(150,cut_online_value)
timer.start()


class MyUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        thread.start_new_thread(handle_message, (data, self.client_address, socket ))  


def handle_message(data, addr, socket):
    if "state" in data and "ip_message" in data and "port_message" in data:
        try:
            datas = demjson.decode(data)
            state = datas["state"]
            ip_message = datas["ip_message"]
            port_message = datas["port_message"]

            try:
                socket.sendto(state,(ip_message,int(port_message)))

            except:
                logging_set.log_message.logging.warning('error_code:104_udp_first_control_send')
 
        except:
            logging_set.log_message.logging.warning('error_code:102_udp_first')

      
    if "first_type" in data and "second_type" in data and "device_number" in data and "current_status" in data and "request" in data :
        try:
            datas = demjson.decode(data)
            First_type = datas["first_type"]
            Second_type = datas["second_type"]
            Device_nums = datas["device_number"]
            Current_status = datas["current_status"]
            Request = datas["request"]

            Mysql.userWork.Insert_log_drive(First_type,Second_type,Device_nums,Current_status,Request)
            Num1_message = Mysql.macWork.Product_isExist_inNum1(First_type,Second_type,Device_nums)
            Num2_message = Mysql.macWork.Product_isExist_inNum2(First_type,Second_type,Device_nums)
            Num12_message = Mysql.macWork.Product_isExist_inNum12(First_type,Second_type,Device_nums)       
            if Num1_message != None:
                if Num2_message == None:
                    Mysql.macWork.Register_mac(First_type,Second_type,Device_nums,Current_status,addr[0],addr[1])

                else:
                    Mysql.macWork.Update_mac(First_type,Second_type,Device_nums,Current_status,addr[0],addr[1])
                    if Num12_message != None:
                        if Num12_message[5] == Request: 
                            pass

                        else:
                            Mysql.macWork.Update_Return_value(First_type,Second_type,Device_nums,int(Request))

                    else:
                        pass

            else:
                logging_set.log_message.logging.warning('error_code:not in form_1_udp_second')
                pass

        except:
            logging_set.log_message.logging.warning('error_code:103_udp_second')


    if "first_type" in data and "second_type" in data and "product_num" in data and "state" in data :

        try:
            datas = demjson.decode(data)
            first_type = datas["first_type"]
            second_type = datas["second_type"]
            product_num = datas["product_num"]
            State = datas["state"]
            info = State["current_status"]
            Mysql.userWork.Insert_log_switch(first_type,second_type,product_num,info)

        except:
            logging_set.log_message.logging.warning('error_code:103_udp_third')


        if info == "online":
            pass

        else:    
            try:
                handle_work.for_handle(first_type,second_type,product_num,State,info)

            except:
                logging_set.log_message.logging.warning('error_code:102_udp_third')


def startservice():#启动udp
    server = SocketServer.UDPServer((HOST, int(PORT)), MyUDPHandler)
    server.serve_forever()
if __name__ == "__main__":
    startservice()
