import pettingzoo
from pettingzoo import AECEnv
import ray
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
from ray.tune.registry import register_env
from ray.rllib.env import PettingZooEnv

from drone import Drone

class MultiAgentPettingZooEnv(PettingZooEnv):
    def __init__(self, env_config):
        super(MultiAgentPettingZooEnv, self).__init__(env_config)


def create_env(env_name):
    env = Drone
    return env


if __name__ == "__main__":
    ray.init()

    # Define your petting zoo environment name
    env_name = "123"

    # Register the custom environment with RLlib
    register_env(env_name, create_env)

    # Define RLlib configuration
    config = {
        "env": env_name,
        "num_workers": 2,  # Number of parallel workers
        "num_cpus_per_worker": 0.5,
        "framework": "torch",  # or "tf" for TensorFlow
        "model": {"fcnet_hiddens": [256, 256]},  # Customize the neural network architecture
        "batch_mode": "complete_episodes",
        "gamma": 0.99,  # Discount factor
        "lambda": 0.95,
        "kl_coeff": 0.2,
        "num_sgd_iter": 20,
        "lr": 5e-5,
        "clip_param": 0.3,
    }

    # Train the PPO agent
    trainer = PPOTrainer(config=config, env=env_name)

    # Train for 1000 iterations
    for i in range(1000):
        result = trainer.train()
        print("Iteration {}: {}".format(i, result))

    # Save the trained model
    checkpoint = trainer.save()
    print("Model saved at", checkpoint)

    ray.shutdown()
