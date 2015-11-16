import subprocess
import re
import time
from results import results
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
import multiprocessing
pegasus_path = ""

#This is a subclass of multiprocessing.Process. The main process does not wait until the subprocess to finish its task
# since the monitoring may take up to several days to finish.  Instead, it continues to listens on the port 8888 to get
# task requests and create multiple threads to handle the monitoring of single workflow.
class startMonitoring(multiprocessing.Process):
    def run(self):
        flag = True
        result = {}
        while flag:
            print pegasus_path
            if pegasus_path !="":
                #Use subprocess to call pegasus-status command
                p = subprocess.Popen([r'pegasus-status', pegasus_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = p.communicate()
                #Output type is a list, the bandwidth information is in the first position of the list
                # the type is a string
                s = (output[0].split("%DONE\n")[1]).split("Summary")[0]
                #Parsing the result of pegasus-status
                vs = re.findall(r'\d+', s)
                # Order of the parsed results
                # READY   PRE  IN_Q  POST  DONE  FAIL %DONE STATE DAGNAME
                result['unready'] = int(vs[0])
                result['ready'] = int(vs[1])
                result['pre'] = int(vs[2])
                result['in_queue'] = int(vs[3])
                result['post'] = int(vs[4])
                result['done'] = int(vs[5])
                result['fail'] = int(vs[6])
                result['percent_done'] = float(vs[7])
                print result
                #Send the result to the NaradaMetrics CIS
                results(result)

            time.sleep(5)
            print pegasus_path
            if result['percent_done'] == 100.0:
                flag = False
#thead list for different monitoring tasks.
threads = []
#Use xmlrpc protocol for server-client communication.
server = SimpleXMLRPCServer(("localhost", 8888))
print "Listening on port 8888..."
#Register the add_task function for adding different monitoring tasks.
server.register_function(add_task, "add_task")
#Run forever until the KeyboardInterrupt event. Press control+c to terminate.
server.serve_forever()

def add_task(path):
    global pegasus_path
    pegasus_path = path

    t = startMonitoring()
    t.start()
    # t = threading.Thread(target=start_monitoring())
    # t.setDaemon(True)
    # threads.append(t)
    # t.start()

    print path
    return "Client"



