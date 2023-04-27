import serializable
from yaml import load, dump, Loader
import logging

class JsonChecker(serializable.Checker):
    def serialize(self, arg):
        return dump(arg)

    def deserialize(self, string):
        return load(string, Loader)
    
def run_tests():
    return serializable.run_tests(JsonChecker())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(run_tests())