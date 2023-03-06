"""
    Code for the node of the client in OPCUA for studying the closed loop latency

"""

import asyncio
import logging
from asyncua import Client
from datetime import datetime
import time
import csv

url = "opc.tcp://localhost:4840/freeopcua/server/"
# namespace = "http://examples.freeopcua.github.io"
namespace = "OPC-UA_Server"


#Dict for before packet times
before_times = {}
for i in range(0,100):
    before_times[i] = datetime.now()

#Dict for after packet times
after_times = {}
for i in range(0,100):
    after_times[i] = datetime.now()

#Dict for elapsed  times
diff_times = {}
for i in range(0,100):
    diff_times[i] = -1.0

filename = "closed_loop_latency_opcua_client_server.csv"

async def main():
    _logger = logging.getLogger(__name__)
    _logger.info(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Find the namespace index (the nodes i and j indexes)
        namespaceidx = await client.get_namespace_index(namespace)
        _logger.info(f"Namespace Index for '{namespace}': {namespaceidx}")

        with open(filename, "w+", newline='') as file:
            writer = csv.writer(file)
            #We write the header
            writer.writerow(["TX Time", "RX Time", "Diff Time"])
            #50 times
            for j in range(0,5):
                #100 times
                for i in range(0,100):
                    # Get the variable node for read / write
                    # we have to write the same node (PLC) and variable name of this node (Temp) as in the server
                    #??WE THINK THAT THE get_child() METHOD BUILDS THE REQUEST
                    temperature = await client.nodes.root.get_child(
                        ["0:Objects", f"{namespaceidx}:PLC", f"{namespaceidx}:Temp"])
                    before_read_time = datetime.now()
                    before_times[i] = before_read_time
                    #We read the value of the temperature
                    read_temp = await temperature.read_value()
                    print("READ VALUE IS: ", read_temp)
                    #We write the new value after we know the prior one
                    temp_value = await temperature.write_value(read_temp+1)
                    #After reading, we stamp the time
                    after_write_time = datetime.now()
                    after_times[i] = after_write_time
                    _logger.info(f"Value of Temperature ({temperature}): {temp_value}")

                    diff_time = after_write_time-before_read_time
                    seconds = diff_time.seconds
                    microsec = diff_time.microseconds
                    #We compute in float the milliseconds
                    milliseconds = float(seconds)*1000 + float(microsec)/1000
                    diff_times[i] = milliseconds
                    #New row of the csv
                    row_data = [before_times[i], after_times[i], diff_times[i]]
                    #We store it in the CSV
                    writer.writerow(row_data)
                    print("Diff time is: ", milliseconds)
        await client.disconnect()



if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)-15s %(message)s",
                        level=logging.INFO)
    asyncio.run(main())
