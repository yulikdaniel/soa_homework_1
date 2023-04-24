from abc import ABC, abstractmethod
from time import time
import random

infinite_list = []
infinite_list.append(infinite_list) # Try to deserialize this

data = {
    "simple": ["Hello world", 1, 15.43],
    "string": ["Hello\t\nworld!", "Привет, мир!", "\{\}\\\\\'\"", "\333"],
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


def unit_tests(some_checker, verbose=0, suites=data.keys()):
    failed_tests = []
    total_success, total = 0, 0
    for suite in suites:
        elements = data[suite]
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


class StressFormat:
    def __init__(self):
        self.__dict = dict()
        self.__dict["contacts"] = dict()
    
    def set_name(self, name):
        self.__dict["name"] = name
    
    def set_age(self, age):
        self.__dict["age"] = age
    
    def set_phone(self, phone):
        self.__dict["contacts"]["phone"] = phone
    
    def set_email(self, email):
        self.__dict["contacts"]["email"] = email
    
    def get_dict(self):
        return self.__dict


def random_string(length):
    alphabet = "qwertyuiopasdfghjklzxcvbnm1234567890"
    return ''.join(random.choices(alphabet, k=length))

def stress_tests(some_checker, verbose=0, stress_size=100, seed=1543):
    random.seed(seed)
    worktime = 0
    correct = 0
    for testnum in range(stress_size):
        data = StressFormat()
        data.set_name(random_string(10))
        data.set_age(random_string(10))
        data.set_phone(random_string(10))
        data.set_email(random_string(10))

        t0 = time()
        if some_checker.check(data.get_dict(), verbose):
            correct += 1
        worktime += time() - t0
    print(f"Correct: {correct}/{stress_size}")
    print(f"Average time spent: {round(worktime / stress_size * 10**6, 3)}μs")


def run_tests(some_checker, verbose=0, unit_suites=data.keys(), stress_size=100, stress_seed=1543):
    print("Unit tests:")
    unit_tests(some_checker, verbose, unit_suites)
    print("Stress tests:")
    stress_tests(some_checker, verbose, stress_size, stress_seed)