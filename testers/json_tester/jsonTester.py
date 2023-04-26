import serializable
from json import loads, dumps
import logging

class JsonChecker(serializable.Checker):
    def serialize(self, arg):
        return dumps(arg)

    def deserialize(self, string):
        return loads(string)
    
def run_tests(verbose=0):
    return serializable.run_tests(JsonChecker(), verbose)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(run_tests())