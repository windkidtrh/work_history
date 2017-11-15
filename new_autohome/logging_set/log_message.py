#-*-coding:utf-8-*-
import logging
from logging.handlers import RotatingFileHandler
Rthandler = RotatingFileHandler('log.txt', maxBytes=10*1024*1024,backupCount=5)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)