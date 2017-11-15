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
import logging
from logging.handlers import RotatingFileHandler
Rthandler = RotatingFileHandler('log.txt', maxBytes=10*1024*1024,backupCount=5)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)
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
 