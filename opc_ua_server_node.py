"""
    Code for the node of the server in OPCUA for studying the closed loop latency

"""

import asyncio
import logging
import random
import sys

from asyncua import Server


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
    plc_node = await server.nodes.objects.add_object(idx, "PLC")
    #Log message
    _logger.info("myobj is {}".format(plc_node))
    #We add one variable to the node
    temperature = await plc_node.add_variable(idx, "Temp", 25)
    #Log message
    _logger.info("myvar is {}".format(temperature))
    # Set MyVariable to be writable by clients
    await temperature.set_writable()


    _logger.info("Starting server!")
    async with server:
        try:
            while True:
                sleep_seconds = random.randint(1, 3)
                await asyncio.sleep(sleep_seconds)
                #We read the variable value
                current_value = await temperature.read_value()
                #We use .info() beacuse a logger doesnt support a print
                _logger.info("Set value of %s to %d", temperature, current_value)
                #We write the variable value
                #await temperature.write_value(current_value)

        #We finish the server if there is an exception (keyboard)        
        except (KeyboardInterrupt, SystemExit):
            server.stop()
            sys.exit()

if __name__ == "__main__":
    #If we set level = logging.DEBUG there is a lot of information
    #If we set level = logging.INFO we get less info
    logging.basicConfig(format="%(asctime)-15s %(message)s",
                        level=logging.INFO)
    #Main run() of the server
    asyncio.run(main(), debug=True)
