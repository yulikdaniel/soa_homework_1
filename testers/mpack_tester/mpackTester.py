import serializable
import msgpack
import logging

class JsonChecker(serializable.Checker):
    def serialize(self, arg):
        return msgpack.packb(arg)

    def deserialize(self, string):
        return msgpack.unpackb(string, raw=False)
    
def run_tests(verbose=0):
    return serializable.run_tests(JsonChecker(), verbose)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(run_tests())