"""
    Code for a MQTT Publisher/Subscriber
    This code is thought to be the robot operator's app used to tell the robotic arm how to move its elbow and wrist (we publish to it)
    After it, we receive an status message from the robot (we subscribe to it)
"""

#Libraries
from paho.mqtt import client as mqtt_client
from threading import Thread
import time

#Broker Address
broker_address = "192.168.8.126"
#Broker port
broker_port = 1883
#Message to publish
msg_pub = ""
#Publishing topic
topics_pub = ["arm/elbow", "arm/wrist"]
#Subscribing topic
topic_sub = "arm/status"
#QoS level
qos_level = 0

"""
IMPORTANT
IF WE WANT TO ENSURE AUTHENTICATION, WE HAVE TO MAKE A CUSTOM mosquitto.conf FILE
IN THAT CASE, WE HAVE TO SPECIFY THOSE PARAMETERS

#MQTT credentials
username = "USERNAME"
passwd = "PASSWORD"
"""


#Function for connecting the broker
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Robot operator has connected to MQTT Broker!\n")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    #Uncomment when using authenticated communications
    #client.username_pw_set(username, passwd)
    client.on_connect = on_connect
    client.connect(broker_address, broker_port)
    return client


#PUBLISH function
def publish(client: mqtt_client.Client, topic_pub, msg):
    global qos_level
    #We publish the message
    result = client.publish(topic_pub,msg, qos=qos_level)
    #State code
    #Most common codes:
    # rc = 0 -> Connection succesful
    # rc = 1 -> Connection refused (incorrect protocol version)
    # rc = 2 -> Connection refused (invalid client identifier)
    # rc = 3 -> Connection refused (server unavailable)
    # rc = 4 -> Connection refused (bad username or passwd)
    # rc = 5 -> Connection refused (not authorised)
    status = result[0]
    if status == 0:
        print("---------------------------------")
        print("Published message: " + msg)
        print("Topic: " + topic_pub)
        print("---------------------------------")

    else:
        print(f"Failed to send message to topic {topic_pub}")

    time.sleep(0.01)


#SUBSCRIBER function
def subscribe(client: mqtt_client.Client):
    global qos_level
    def on_message(client, userdata, msg):
        #Message received
        rx_msg = msg.payload.decode()
        rx_topic = msg.topic
        print("---------------------------------")
        print("Received message " + rx_msg)
        print("Topic: " + rx_topic)
        print("---------------------------------")


    client.subscribe(topic_sub, qos=qos_level)
    print("Subscribed to topic: " + topic_sub)
    client.on_message = on_message

#We create this function so we can use a thread for subscribing (otherwise the loop_forever() dont let us continue)
def subscriber(client):
    subscribe(client)
    client.loop_forever()


#Main function
def run():
    global msg_pub, qos_level
    #We connect
    client = connect_mqtt()
    #Whe create a thread for subscribing, arguments -> client
    thread1 = Thread(target=subscriber, args = (client,))
    thread1.start()
    #If we dont put this sleep, the first packet can be lost due to the sync of the thread and publish
    time.sleep(1)
    
    while True:
        #We ask for the QoS level
        qos_level = int(input("QoS level {0,1,2}: "))
        #We ask for a message to publish
        msg_pub = input("Message: ")
        #We ask for a topic to publish
        topic = input("Topic: \n1) arm/elbow\n2) arm/wrist\n: ")
        #Case -> elbow topic
        if topic == "1":
            topic = topics_pub[0]
            publish(client, topic, msg_pub)
        #Case -> wrist topic
        elif topic == "2":
            topic = topics_pub[1]
            publish(client, topic, msg_pub)
        #The topic doesnt exist
        else:
            print("That topic is not avaliable, try again")
        #We sleep 5 seconds because we should wait for all the packets to be finished
 
if __name__ == '__main__':
    run()
