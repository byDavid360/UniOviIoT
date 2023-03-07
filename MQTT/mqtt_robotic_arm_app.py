"""
    Code for a MQTT Publisher/Subscriber
    This code is thought to be the robotic arm app in which we receive messages from the robot operator telling how to move the elbow and wrist
    After it, we send an status message 
"""

#Libraries
from paho.mqtt import client as mqtt_client

#Broker address
broker_address = "192.168.8.126"
#Broker port
broker_port = 1883
#Publishing topic
topic_pub = "arm/status"
#Subscribing topics
topics_sub = ["arm/elbow", "arm/wrist"]
#QoS for subscribing
qos_level = -1
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
            print("Robotic arm has connected to MQTT Broker!\n")
        else:
            print("Failed to connect, return code %d\n", rc)
    
    client = mqtt_client.Client()  
    #Uncomment when using authenticated communications
    #client.username_pw_set(username, passwd)
    client.on_connect = on_connect
    client.connect(broker_address, broker_port)
    return client


#PUBLISH function (we specify the type of client as a MQTT client)
def publish(client: mqtt_client.Client,tx_msg):
    result = client.publish(topic_pub,tx_msg,qos=qos_level)
    #Status
    status = result[0]
    if status == 0:
        print("---------------------------------")
        print("Published message: " + tx_msg)
        print("Topic: " + topic_pub)
        print("---------------------------------")

    else:
        print(f"Failed to send message to topic {topic_pub}")
    print("\n") 


#SUBSCRIBE function
def subscribe(client: mqtt_client.Client):
    def on_message(client, userdata, msg):

        #What we receive
        rx_msg = msg.payload.decode()
        rx_topic = msg.topic
        #We study in which topic the msg is received so we build an status msg
        if rx_topic == "arm/elbow":
            tx_msg = "elbow_OK"
        elif rx_topic == "arm/wrist":
            tx_msg = "wrist_OK"
        print("---------------------------------")
        print("Received message: " + rx_msg)
        print("Topic: " + msg.topic)
        print("---------------------------------")
        #We publish the status message
        publish(client,tx_msg)
        
            
    for topic in topics_sub:
        client.subscribe(topic, qos=qos_level)
        print("Subscribed to topic: " + topic)
    client.on_message = on_message

def run():
    global qos_level
    #We specify the qos_level for the subscribing link
    qos_level = int(input("QoS level {0,1,2}: "))
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
