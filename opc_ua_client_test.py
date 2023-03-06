"""
    OPC-UA client implementation in python
    Computer side
"""









#We import the OPCUA client
from opcua import Client
import random
import time

#URL of the server
url = "opc.tcp://172.26.19.38:4840"
#Client instance
client = Client(url)

try:
    client.connect()
    print("Client has connected to server in {}".format(url))
    start_time = time.time()

except:
    print("Error")

"""
#We get the values from the server
while True:
    #We access to the part of the node containing the Wrist twist variable
    Wrist_twist = client.get_node("ns=2;i=2")
    Wrist_twist_value = Wrist_twist.get_value()
    #We access to the part of the node containing the Elbow twist variable
    Elbow_twist = client.get_node("ns=2;i=3")
    Elbow_twist_value = Elbow_twist.get_value()
    print("Wrist twist value: ", Wrist_twist_value)
    print("Elbow twist value: ", Elbow_twist_value)
"""

#Updating values 1000 times
#We write values in wrist and elbow twist
for i in range(0,5):
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



"""
#Code for only updating values once

Wrist_twist = client.get_node("ns=2;i=2")
Elbow_twist = client.get_node("ns=2;i=3")
#We get the current values of both variables
Wrist_current = Wrist_twist.get_value()
Elbow_current = Elbow_twist.get_value()
print("Current wrist twist value: ", Wrist_current)
print("Current elbow twist value: ", Elbow_current)

#We ask for new values for both variables
wrist_value = input("New wrist value: ")
Wrist_twist.set_value(wrist_value)
elbow_value = input("New elbow value: ")
Elbow_twist.set_value(elbow_value)

client.disconnect()
"""