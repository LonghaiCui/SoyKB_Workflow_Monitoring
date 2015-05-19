************************** SoyKB WorkFlow Monitoring System*****************************

Pegasus Workflow Management System and NaradaMetrics Monitoring System Integration script for Soybean Knowledge Base

This is an independent module of NaradaMetrics specifically written for SoyKB workflow monitoring. This module can be considered as specific user defined custom metrics and communicates with NaradaMetrics CIS (central information system) in an active way by sending the measurement data to CIS without affecting its internal task scheduler. The Pegasus workflow is processed in the worker nodes in the TACC super computer center, monitoring system (workflow.isi.edu) is only responsible for receiving and sending the monitoring information. 

For the details of software defined application monitoring platform NaradaMetrics, please see http://www.naradametrics.com/

For the details of workflow management system Pegasus, please see http://pegasus.isi.edu/

For the details of soybean knowledge base SoyKB, please see http://soykb.org/

————————————————————————————————————————————————————————————

Make sure all the files are put in the same directory including results.py, utils.py, auth.py and dateutil folder. These are essential files to communicate with NaradaMetrics CIS. 

For the convenience of soyKB users, we decouple the pegasus workflow generating module and monitoring module. The monitor server runs on a specific screen terminal named monitor_server, the soyKB users only need to call the monitor client with the workflow directory automatically created by pegasus generator as parameter. Multiple threading is used for continuously receive the workflow monitoring requests and return the terminal operatability to the users.  

————————————————————————————————————————————————————————————
1. Login to the pegasus workflow management server.(Contact Dr.Trupti to ask for the access permission joshitr@missouri.edu)

ssh username@workflow.isi.edu

2. Ensure the following packages are installed: python screen 

sudo yum install python screen

3. Start a screen session for soykb workflow monitoring server. 

screen -S monitor_server; python monitor_server.py; screen -d monitor_server;

4. Generate the pegasus workflow for soykb, this command will create a folder where all the workflow is processed. 

./workflow-generator --exec-env tacc-stampede

5. Run the pegasus workflow with the folder directory as the parameter. 

python client.py /local-scratch/longhai/soykb/20141103-203914/wf-20141103-203914

6. Run the monitor client whenever you want to start getting the periodic measurement data.

python client.py /local-scratch/longhai/soykb/20141103-203914/wf-20141103-203914
python client.py /local-scratch/longhai/soykb/20141103-230637/wf-20141103-230637
