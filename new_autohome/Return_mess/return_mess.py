#-*-coding:utf-8-*-
import json
def return_message(a=0,b=0,c='',d='',is_manager='',callback=''):
    return_data = { "success":"0", "error_code":"0", "message":""}
    return_more_data = { "success":"0", "error_code":"0", "message":"", "error_intr":""}
    mess = [return_data,return_more_data]

    if a != 0:
        return_data["success"] = a
        return_more_data["success"] = a

    if b != 0 :
        return_data["error_code"] = b
        return_more_data["error_code"] = b
        if d != '':
            return_more_data["error_intr"] = d

    if c != '':
        return_data["message"]=c
        return_more_data["message"]=c

    try:
        if callback != "":
            if is_manager == '':
                return callback+"("+json.dumps(mess[0])+")"
            else:
                return callback+"("+json.dumps(mess[1])+")"                    
        else:
            if is_manager == '':
                return json.dumps(mess[0])
            else:
                return json.dumps(mess[1])
    except:
        assert "wrong"

def Request_mess(Request):
    if len(str(Request)) == 1:
        Order_request = "0000000" + str(Request)
    elif len(str(Request)) == 2:
        Order_request = "000000" + str(Request)
    elif len(str(Request)) == 3:
        Order_request = "00000" + str(Request)
    elif len(str(Request)) == 4:
        Order_request = "0000" + str(Request)
    elif len(str(Request)) == 5:
        Order_request = "000" + str(Request)
    elif len(str(Request)) == 6:
        Order_request = "00" + str(Request)
    elif len(str(Request)) == 7:
        Order_request = "0" + str(Request)
    elif len(str(Request)) == 8:
        Order_request = str(Request)#生成指令结尾格式

    return Order_request

def return_message_datas(state,ip_message,port_message):
    try:
        news_data = { "state" : "", "ip_message" : "", "port_message" : ""}
        news_data["state"] = state
        news_data["ip_message"] = ip_message
        news_data["port_message"] = port_message
        return news_data

    except:
        assert "wrong"