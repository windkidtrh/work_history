#-*-coding:utf-8-*-
import web
import time
import datetime
import Mysql.mysql
import Webs.customer
import Mysql.userWork
import Mysql.macWork
import SocketServer
import socket
import threading
import traceback
import SimpleHTTPServer
import udpserver
import sys
sys.path.append("..")
import logging_set.log_message


urls=(
      '/Control_mac','Webs.customer.Control_mac',
      '/Control_switch','Webs.customer.Control_switch',
      '/Online','Webs.customer.Online',
)


if __name__ == "__main__":
  try:
    threading.Thread(target=udpserver.startservice).start()   
  except:
    logging.warning('fail to create threads')
  app=web.application(urls,globals())
  app.run()
 