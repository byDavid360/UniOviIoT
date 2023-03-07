"""
   OPC-UA Client script

   Here we deploy an OPC-UA Client that access to an OPC-UA server thought to be a robotic arm in which the client is able to set its elbow and wrist rotation angles
   
"""

#We import the OPCUA client
from opcua import Client
import random
import time

#URL of the server (opc.tcp://SERVER_IP:PORT)
url = "opc.tcp://172.26.19.38:4840"
#Client instance
client = Client(url)

try:
    client.connect()
    print("Client has connected to server in {}".format(url))
    start_time = time.time()

except:
    print("Error")


#We write values in wrist and elbow twist 
Wrist_twist = client.get_node("ns=2;i=2")
Elbow_twist = client.get_node("ns=2;i=3")
#We get the current values of both variables
Wrist_current = Wrist_twist.get_value()
Elbow_current = Elbow_twist.get_value()
print("Current wrist twist value: ", Wrist_current)
print("Current elbow twist value: ", Elbow_current)

#We ask for new values for both variables
wrist_value = random.randint(0,90)
elbow_value = random.randint(0,90)
Wrist_twist.set_value(wrist_value)
Elbow_twist.set_value(elbow_value)
time.sleep(0.1)

client.disconnect()
end_time = time.time()
print("Time elapsed: " + str(end_time-start_time) + "s")
