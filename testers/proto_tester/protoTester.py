import serializable
from stressformat_pb2 import TPerson
from google.protobuf.json_format import ParseDict, MessageToDict, MessageToJson
import logging
import timeit

class ProtoChecker(serializable.Checker):
    def __init__(self, format):
        self.format = format

    def serialize(self, arg):
        return ParseDict(arg, self.format()).SerializeToString()

    def deserialize(self, string):
        message = self.format()
        message.ParseFromString(string)
        return MessageToDict(message)
    
    def time_serialize(self, arg):
        protobuf = ParseDict(arg, self.format())
        return timeit.timeit(lambda: protobuf.SerializeToString(), number=1000)
    
    def time_deserialize(self, arg):
        string = ParseDict(arg, self.format()).SerializeToString()
        message = self.format()
        return timeit.timeit(lambda: message.ParseFromString(string), number=1000)
    
def run_tests():
    return serializable.run_tests(ProtoChecker(TPerson))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(run_tests())