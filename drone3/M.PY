import gymnasium as gym
import ray
from ray.rllib.algorithms.ppo import PPOConfig

from fin import Drone


ray.init()

config = PPOConfig().environment(Drone, env_config={"corridor_length": 5})
algo = config.build()

for _ in range(3):
    print(algo.train())

algo.stop()