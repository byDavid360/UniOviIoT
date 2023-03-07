"""
OPC-UA Server code in Python
 Here we deploy an OPC-UA Server made up of a Node called Arm-params in which 2 main variables are studied:
    1) Wrist-Twist: rotation of the wrist in degrees
    2) Elbow-Twist: rotation of the elbow in degrees

"""

from opcua import Server
#Server instance
server = Server()
#Server endpoint
url = "opc.tcp://0.0.0.0:4840"
server.set_endpoint(url)

#Namespace of the server
server_name = "OPC_UA_TEST_SERVER"
addspace = server.register_namespace(server_name)

#A node is the way information is represented in OPC-UA
#It can be variables, Datatypes, methods...
node = server.get_objects_node()
#We represent the arm information as an object of the node
Arm_param = node.add_object(addspace, "Arm-params")
#We add variables of the arm (we set them to 0)
Wrist_twist = Arm_param.add_variable(addspace, "Wrist-Twist", 0)
Elbow_twist = Arm_param.add_variable(addspace, "Elbow-Twist", 0)

#We let them to be writable
Wrist_twist.set_writable()
Elbow_twist.set_writable()


server.start()
print("Server is running at {}".format(url))
