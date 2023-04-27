from abc import ABC, abstractmethod
import timeit
import random


def equal(d1, d2): # Returns the max floating number difference between d1 and d2, or >=1 if they are not equal at all
    if type(d1) != type(d2):
        return 1
    mx = 0
    if type(d1) == dict:
        if set(d1.keys()) != set(d2.keys()):
            return 1
        for key in d1:
            mx = max(mx, equal(d1[key], d2[key]))
        return mx

    elif type(d1) == list:
        if len(d1) != len(d2):
            return 1
        for i in range(len(d1)):
            mx = max(mx, equal(d1[i], d2[i]))
        return mx

    elif type(d1) == float:
        return abs(d1 - d2)
    else:
        return int(d1 != d2)


class Checker(ABC):
    @abstractmethod
    def serialize(self, arg):
        pass

    @abstractmethod
    def deserialize(self, string):
        pass

    def check(self, arg):
        deserialized = self.deserialize(self.serialize(arg))
        return equal(arg, deserialized)
    
    def time_serialize(self, arg):
        return timeit.timeit(lambda: self.serialize(arg), number=1000)

    def time_deserialize(self, arg):
        serialized = self.serialize(arg)
        return timeit.timeit(lambda: self.deserialize(serialized), number=1000)
    
    def size_serialized(self, arg):
        return len(self.serialize(arg))


class StressFormat:
    def __init__(self):
        self.__dict = dict()
        self.__dict["contacts"] = dict()
        self.__dict["friends"] = []

    def set_name(self, name):
        self.__dict["name"] = name

    def set_age(self, age):
        self.__dict["age"] = age

    def add_friend(self, friend):
        self.__dict["friends"].append(friend)

    def set_phone(self, phone):
        self.__dict["contacts"]["phone"] = phone

    def set_email(self, email):
        self.__dict["contacts"]["email"] = email

    def set_ape_index(self, apeIndex):
        self.__dict["apeIndex"] = apeIndex;

    def get_dict(self):
        return self.__dict


def random_string(length):
    alphabet = "qwertyuiopasdfghjklzxcvbnm1234567890"
    return ''.join(random.choices(alphabet, k=length))

def stress_tests(some_checker, stress_size=100, seed=1543):
    stress_size=1
    result = ""
    random.seed(seed)
    sertime = 0 # This is calculated in milliseconds
    desertime = 0
    correct = 0
    sersize = 0
    for testnum in range(stress_size):
        data = StressFormat()
        data.set_name(random_string(10))
        data.set_age(random.randint(1, 128))
        data.set_phone(random.randint(2**20, 2**31-1)) # This is pretty much what a phone number looks like, no?
        data.set_email(random_string(10))
        data.set_ape_index(random.normalvariate(1.024, 0.027)) # https://www.reddit.com/r/climbharder/comments/v5j0k6/does_anyone_have_data_on_the_percentile/
        for _ in range(10):
            data.add_friend(random_string(10))

        if some_checker.check(data.get_dict()) < 1e-6: # For floating-point support
            correct += 1
            sertime += some_checker.time_serialize(data.get_dict())
            desertime += some_checker.time_deserialize(data.get_dict())
            sersize += some_checker.size_serialized(data.get_dict())
        else:
            print(some_checker.check(data.get_dict()))
            print(data.get_dict())
            print(some_checker.deserialize(some_checker.serialize(data.get_dict())))

    result += f"Correct: {correct}/{stress_size}\n"
    result += f"Average time spent on serialization: {round(sertime * 10**3 / correct, 3)}μs\n"
    result += f"Average time spent on deserialization: {round(desertime * 10**3 / correct, 3)}μs\n"
    result += f"Average size of serialized format: {round(sersize / correct)} bytes\n"
    return result


def run_tests(some_checker, stress_size=100, stress_seed=1543):
    return stress_tests(some_checker, stress_size, stress_seed)