import xmlrpclib
import sys
import socket
proxy = xmlrpclib.ServerProxy("http://localhost:8888/")
print "parameter", sys.argv[1]
#socket.setdefaulttimeout(None)
print proxy.add_task(sys.argv[1])

