import serializable
from xmltodict import parse, unparse
import logging

class JsonChecker(serializable.Checker):
    def serialize(self, arg):
        return unparse({"obj": arg})

    def deserialize(self, string):
        return parse(string)["obj"]
    
def run_tests(verbose=0):
    return serializable.run_tests(JsonChecker(), verbose)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(run_tests())