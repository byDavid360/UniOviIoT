import logging
from asyncua import Client, ua, Node
import asyncio
import random
import time

"""
    Code of OPC-UA PubSub SUBSCRIBER used to study localhost

"""

#OPCUA Namespace
namespace = "OPC-UA_Server"
#Period PUBSUB (ms)
period_ms = 1



logging.basicConfig(level=logging.WARNING)

class SubHandler:

    #Function initialization (constructor)
    def __init__(self, aux_value: Node):
        self.aux_value = aux_value


    #Function that tells us about the change in data
    async def datachange_notification(self, node, val, attr):
        global packet_dict
    
        print("New data change event:")
        print("Node: ", node)
        print("Value: ", val)


   

#We separate WRITE of SUBS in 2 functions because that way the async waits for the last to complete
# so its a concurrent/parallel scenario
# |----------------------- WRITE ENDS                         | From here both finished but we wait for the last to complete
# |--------------------------------------------- SUBS ENDS    |



#Function for the SUBSCRIPTION
async def subscription(client: Client, variable:Node):

    #We create a SUBSCRIPTION 
    sub = await client.create_subscription(period_ms, SubHandler(variable))
    #We subscribe to the value change of the variable temperature
    handle_var = await sub.subscribe_data_change(variable)

    await change_value(variable)

    await sub.unsubscribe(handle_var)
    await sub.delete()


async def change_value(node: Node):
      for i in range(0,100):
        # Get the variable node for read / write
        # we have to write the same node (PLC) and variable name of this node (Temp) as in the server
        #??WE THINK THAT THE get_child() METHOD BUILDS THE REQUEST
        #We write the new value after we know the prior one
        await node.write_value(i)
        await asyncio.sleep(0.25)



            

async def main():
    #We connect to the OPC-UA server
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")
    try:
        await client.connect()
    
        #We get the namespace of the node
        namespaceidx = await client.get_namespace_index(namespace)
        #We get the childs (nodes) of the namespace
        var_wrist =  await client.nodes.root.get_child(
                        ["0:Objects", f"{namespaceidx}:Arm", f"{namespaceidx}:Wrist"])
        #We get the elbow variable
        var_elbow =  await client.nodes.root.get_child(
                        ["0:Objects", f"{namespaceidx}:Arm", f"{namespaceidx}:Elbow"])
   

        
    
        #We SUBSCRIBE
        await subscription(client,var_wrist)
        await subscription(client,var_elbow)

      
        
    finally:
        await client.disconnect()

    
if __name__ == "__main__":
    asyncio.run(main())
