import serializable
from json import loads, dumps

class JsonChecker(serializable.Checker):
    def serialize(self, arg):
        return dumps(arg)

    def deserialize(self, string):
        return loads(string)
    
def run_tests(verbose=0):
    serializable.run_tests(JsonChecker(), verbose)

if __name__ == "__main__":
    run_tests()