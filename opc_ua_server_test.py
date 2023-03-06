"""
OPC-UA Server code in Python
Robotic arm side

"""
from opcua import Server
import time
#Server instance
server = Server()
#Server endpoint
url = "opc.tcp://172.26.19.38:4840"
server.set_endpoint(url)

server_name = "OPC_UA_TEST_SERVER"
addspace = server.register_namespace(server_name)

#A node is the way information is represented in OPC-UA
#It can be variables, Datatypes, methods...
node = server.get_objects_node()
#We represent the arm information as an object of the node
Arm_param = node.add_object(addspace, "Arm-params")
#We add variables of the arm
Wrist_twist = Arm_param.add_variable(addspace, "Wrist-Twist", 0)
Elbow_twist = Arm_param.add_variable(addspace, "Elbow-Twist", 0)

Wrist_twist.set_writable()
Elbow_twist.set_writable()


server.start()
print("Server is running at {}".format(url))

"""
while True:
    w_twist = input("Wrist twist value: ")
    Wrist_twist.set_value(w_twist)
    e_twist = input("Elbow twist value: ")
    Elbow_twist.set_value(e_twist)
    time.sleep(5)
"""