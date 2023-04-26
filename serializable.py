from abc import ABC, abstractmethod
import timeit
import random

class Checker(ABC):
    @abstractmethod
    def serialize(self, arg):
        pass

    @abstractmethod
    def deserialize(self, string):
        pass

    def check(self, arg, verbose = 0):
        deserialized = self.deserialize(self.serialize(arg))
        return arg == deserialized
    
    def time_serialize(self, arg):
        return timeit.timeit(lambda: self.serialize(arg), number=1000)

    def time_deserialize(self, arg):
        serialized = self.serialize(arg)
        return timeit.timeit(lambda: self.deserialize(serialized), number=1000)


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
    result = ""
    random.seed(seed)
    sertime = 0 # This is calculated in milliseconds
    desertime = 0
    correct = 0
    for testnum in range(stress_size):
        data = StressFormat()
        data.set_name(random_string(10))
        data.set_age(random_string(10))
        data.set_phone(random_string(10))
        data.set_email(random_string(10))

        if some_checker.check(data.get_dict(), verbose):
            correct += 1
            sertime += some_checker.time_serialize(data.get_dict())
            desertime += some_checker.time_deserialize(data.get_dict())

    result += f"Correct: {correct}/{stress_size}\n"
    result += f"Average time spent on serialization: {round(sertime * 10**3 / correct, 3)}μs\n"
    result += f"Average time spent on deserialization: {round(desertime * 10**3 / correct, 3)}μs\n"
    return result


def run_tests(some_checker, verbose=0, stress_size=100, stress_seed=1543):
    return stress_tests(some_checker, verbose, stress_size, stress_seed)