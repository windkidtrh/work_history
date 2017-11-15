#-*-coding:utf-8-*-
import MySQLdb
import socket


HOSTNAME = socket.gethostname()
PASSWD = ''

if HOSTNAME == 'iZ94zoeilgyZ':
    PASSWD = '4c1fadc64b' #4c1fadc64b
elif HOSTNAME == 'iZ28quomnknZ':
    PASSWD = 'aa123123'
elif HOSTNAME == 'iZ8vb8il84z4pt60dloexiZ':
    PASSWD = 'YJSshy2017'

sql_socket = "/run/mysqld/mysqld.sock"   #"/tmp/mysql.sock"

def connect_mysql():
    
    try:
        conn = MySQLdb.connect(
             host = 'localhost',
             port = 3306,
             user = 'root',
             passwd = PASSWD,
             charset = "utf8",
             unix_socket = sql_socket
             )
        conn.select_db("cloudhome")
        return conn
    
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


if __name__ == '__main__':
    con = connect_mysql()
    print con
