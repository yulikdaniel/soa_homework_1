from abc import ABC, abstractmethod

infinite_list = []
infinite_list.append(infinite_list) # Try to deserialize this

data = {
    "simple": ["Hello world", 1, 15.43],
    "string": ["Hello\t\nworld!", "Привет, мир!", "", "\{\}\\\\\'\"", "\333"],
    "float": [3.14159265359, float("+inf"), float("-inf"), float("nan")],
    "list": [[1, 2, 3], [1, "hi"], [], [[1, 2, 3], [[[[[]]]]]]],
    "tricky": infinite_list
}

class Checker(ABC):
    @abstractmethod
    def serialize(self, arg):
        pass

    @abstractmethod
    def deserialize(self, string):
        pass

    def check(self, arg, verbose = 0):
        try:
            deserialized = self.deserialize(self.serialize(arg))
            if arg == deserialized:
                return True
            if verbose == 2:
                print(f"Expected {arg}, got {deserialized}")
            return False
        except Exception as e:
            if verbose == 2:
                print(f"Got exception {e} while serializing/deserializing {arg}")
            return False


def run_tests(some_checker, verbose=0):
    failed_tests = []
    total_success, total = 0, 0
    for suite, elements in data.items():
        success = 0
        for element in elements:
            if some_checker.check(element, verbose):
                success += 1

        if verbose:
            print(f"Suite {suite}: successfully completed {success}/{len(elements)}")

        total_success += success
        total += len(elements)

        if success != len(elements):
            failed_tests.append(suite)
    
    print(f"Total success rate {total_success}/{total}")
    if failed_tests:
        print(f"Suites failed {len(failed_tests)}/{len(data)}, failed suites: {', '.join(failed_tests)}")
    else:
        print("All ok!")
