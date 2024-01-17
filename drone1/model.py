import gymnasium as gym
from stable_baselines3 import A2C
import os
from fin import Drone


models_dir = "models/A2C"
logdir = "logs/A2C"
episode_dir= "episode/A2C"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

if not os.path.exists(episode_dir):
    os.makedirs(episode_dir)

env = Drone()


model = A2C('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 3000
iters = 0
model.learn(total_timesteps=TIMESTEPS)
model.save(f"{models_dir}")
