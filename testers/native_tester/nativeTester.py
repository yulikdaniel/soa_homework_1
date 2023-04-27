import serializable
import logging
from ast import literal_eval

class NativeChecker(serializable.Checker):
    def serialize(self, arg):
        return arg.__repr__()

    def deserialize(self, string):
        return literal_eval(string)
    
def run_tests():
    return serializable.run_tests(NativeChecker())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(run_tests())