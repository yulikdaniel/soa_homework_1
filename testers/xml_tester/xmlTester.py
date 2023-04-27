import serializable
from xmltodict import parse, unparse
import logging

def convert(d):
    if type(d) == str:
        try:
            return int(d)
        except:
            try:
                return float(d)
            except:
                return d
    if type(d) == dict:
        for key in d:
            d[key] = convert(d[key])
    if type(d) == list:
        for i in range(len(d)):
            d[i] = convert(d[i])
    return d

class JsonChecker(serializable.Checker):
    def serialize(self, arg):
        return unparse({"obj": arg})

    def deserialize(self, string):
        return convert(parse(string)["obj"])
    
def run_tests():
    return serializable.run_tests(JsonChecker())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(run_tests())