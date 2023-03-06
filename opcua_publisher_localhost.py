import asyncio
import logging
import random
import sys

from asyncua import Server

"""
    Code of OPC-UA PubSub PUBLISHER used in localhost
"""


async def main():
    _logger = logging.getLogger(__name__)
    # set up our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # set up our own namespace, not really necessary but should as spec
    # uri = "http://examples.freeopcua.github.io"
    uri = "OPC-UA_Server"
    idx = await server.register_namespace(uri)
    #Log messages
    _logger.info("idx is {}".format(idx))

    # server.nodes, contains, links to very common nodes like objects and root
    #We creatre a Node inside the namespace of this server
    arm_node = await server.nodes.objects.add_object(idx, "Arm")
    #Log message
    _logger.info("myobj is {}".format(arm_node))
    #We add one variable to the node
    var_wrist = await arm_node.add_variable(idx, "Wrist", 0)
    #Log message
    _logger.info("myvar is {}".format(var_wrist))
    # Set Temperaturee to be writable by clients
    await var_wrist.set_writable()

    #We add one variable to the node
    var_elbow = await arm_node.add_variable(idx, "Elbow", 0)
    #Log message
    _logger.info("myvar is {}".format(var_elbow))
    # Set Temperaturee to be writable by clients
    await var_elbow.set_writable()
    _logger.info("Starting server!")

    async with server:
        print("Before sleep")
        await asyncio.sleep(7)
        print("After sleep")
        try:
        
       

            #We finish sending our packets so we sleep forever    
            while True:
                val_wrist = await var_wrist.read_value()
                val_elbow = await var_elbow.read_value()
                print("VALUE OF WRIST: ", val_wrist)
                print("VALUE OF ELBOW: ", var_elbow)
                await asyncio.sleep(2)

                
        

        #We finish the server if there is an exception (keyboard)        
        except (KeyboardInterrupt, SystemExit):
            await server.stop()
            sys.exit()

if __name__ == "__main__":
    #If we set level = logging.DEBUG there is a lot of information
    #If we set level = logging.INFO we get less info
    logging.basicConfig(format="%(asctime)-15s %(message)s",
                        level=logging.INFO)
    #Main run() of the server
    asyncio.run(main(), debug=True)
