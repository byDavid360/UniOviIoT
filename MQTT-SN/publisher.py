import sys, os
import logging
from pathlib import Path
import threading
import time


sys.path.append(os.path.join(Path(__file__).parents[0], "mqttsnclient"))
# sys.path.append(os.path.join(sys.path[0], "mqttsnclient"))

from mqttsnclient.MQTTSNclient import Callback
from mqttsnclient.MQTTSNclient import Client
from mqttsnclient.MQTTSNclient import publish
import mqttsnclient.MQTTSN as MQTTSN

FORMAT = '%(asctime)s, %(levelname)s, %(filename)s:%(lineno)d, %(funcName)s(), %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

myLogger = logging.getLogger()

print(sys.version_info)


# message_q = queue.Queue()

#Broker address
host = "172.26.23.13"
#Port for RSMB
port = 1884
#Topic for publishing
topic_pub = "n1"
#Topic for subscribing
topic_sub = "n2"
#Client
client_name = "node1"


class MyCallback(Callback):

    def on_message(self, client, TopicId, Topicname, payload, qos, retained,
                   msgid):
        m= "Arrived" +" topic  " +str(TopicId)+ "message " +\
           str(payload) +"  qos= " +str(qos) +" ret= " +str(retained)\
           +"  msgid= " + str(msgid)
        
        print("------------------------------")
        print("MSG RX: ", payload)
        print("Topic: ", Topicname.decode('utf8'))
        print("------------------------------\n")

        #myLogger.info(m)
        #myLogger.info("got the message {}".format(payload))
        # message_q.put(payload)
        return True
    

#We ask the user for the number of packets, the QoS and how loaded is the network
n_packets = int(input("Number of packets: "))
qos = int(input("QoS {0,1]: "))

#Function for subscribing
def subscription():
    try:
        client.subscribe(topic_sub, qos=qos)
        client.loop_start()
        while True:
            time.sleep(10)

    except BaseException as e:
        client.loop_stop()
        client.disconnect()
        raise e


#We start the client
client = Client(client_name)
client.message_arrived_flag = False
client.registerCallback(MyCallback())
myLogger.info("threads {}".format(threading.active_count()))
myLogger.info("connecting {}".format(host))
client.connected_flag = False

#We connect to the RSMB
client.connect(host, port)
#We look for CONNACK msg
client.lookfor(MQTTSN.CONNACK)

try:
    if client.waitfor(MQTTSN.CONNACK) == None:
        myLogger.info("connection failed")
        raise SystemExit("no Connection quitting")
except Exception as e:
    logging.exception(e)
    myLogger.info("connection failed")
    raise SystemExit("no Connection quitting")


try:
    #We publish the messages
    for i in range(0, n_packets):
    
        msg = "PACKET_NUMBER_"+str(i)
        client.publish(topic_pub, msg, qos=qos)
        print("------------------------------")
        print("MSG PUBLISHED: ", msg)
        print("Topic: ", topic_pub)
        print("------------------------------\n")
        time.sleep(0.1)

except BaseException as e:
    client.loop_stop()
    client.disconnect()
    raise e
