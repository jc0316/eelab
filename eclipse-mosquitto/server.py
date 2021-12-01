import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt

history = []

class Subscriber():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(host="localhost", port=1883)
        self.client.subscribe('log', 0)

    def on_message(self, client, obj, msg):
        print(f"TOPIC:{msg.topic}, VALUE:{msg.payload}")
        history.append(msg.payload)

    def run(self):
        print("subscribe log to localhost:1883")
        try:
            self.client.loop_forever()
        except KeyboardInterrupt as e:
            pass

    

class FibCalculatorLogServicer(log_pb2_grpc.FibCalculatorLogServicer):

    def __init__(self):
        pass

    def getHistory(self, request, context):
        response = log_pb2.LogResponse()
        response.value.extend(history)

        return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8088, type=int)
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = FibCalculatorLogServicer()
    log_pb2_grpc.add_FibCalculatorLogServicer_to_server(servicer, server)
    sub = Subscriber()
    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        print(f"Run gRPC Server at {args['ip']}:{args['port']}")
        sub.run()
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass
