from drone import Drone

from pettingzoo.test import parallel_api_test

if __name__ == "__main__":
    env = Drone()
    parallel_api_test(env, num_cycles=10000000)
