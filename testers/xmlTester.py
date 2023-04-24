import serializable
from xmltodict import parse, unparse

class JsonChecker(serializable.Checker):
    def serialize(self, arg):
        return unparse({"obj": arg})

    def deserialize(self, string):
        return parse(string)["obj"]
    
def run_tests(verbose=0):
    serializable.run_tests(JsonChecker(), verbose)

if __name__ == "__main__":
    serializable.run_tests(JsonChecker(), unit_suites=["string"])