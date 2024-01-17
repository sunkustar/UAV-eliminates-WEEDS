import functools
import random
from copy import copy
import pygame
import math

import numpy as np
from gymnasium.spaces import  *

from pettingzoo import ParallelEnv

height=500
width=500

screen = pygame.display.set_mode((width,height))
Black = (0, 0, 0)

class Drone(ParallelEnv):
    """The metadata holds environment constants.

    The "name" metadata allows the environment to be pretty printed.
    """

    metadata = {
        "name": "custom_environment_v0",
    }

    def __init__(self, config=None):
        self.possible_agents=["drone1","drone2","drone3"]
        self.agents=["drone1","drone2","drone3"]
        
        self.dic={"drone1":1,"drone2":2,"drone3":3}

        
        self.observation_spaces=dict(zip(self.agents,[MultiDiscrete([500]*16)]*3))
        self.action_spaces=dict(zip(self.agents, [Discrete(4)] * 3))


       
      
    
    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
   
    def reset(self , seed=None, options=None):
        
        self.weeds={1:[np.random.randint(100,300),np.random.randint(100,300)],2:[np.random.randint(100,300),np.random.randint(100,300)],3:[np.random.randint(100,300),np.random.randint(100,300)],4:[np.random.randint(100,300),np.random.randint(100,300)],5:[np.random.randint(100,300),np.random.randint(100,300)]}
        self.weedh = {1:100,2:100,3:100,4:100,5:100}
        self.dis = {1:0.05,2:0.006,3:0.01}
        self.pos={1:[np.random.randint(100,300),np.random.randint(100,300)],2:[np.random.randint(100,300),np.random.randint(100,300)],3:[np.random.randint(100,300),np.random.randint(100,300)]}
        self.possible_agents=["drone1","drone2","drone3"]
        self.agents=["drone1","drone2","drone3"]
        
        self.chargepoints=[25,275,475,275]
        self.charge = {1:100,2:100,3:100}
        self.run={1:0,2:0,3:0,4:0,5:0}
        self.timestep = 0
        self.score=0


        self.rewards={1:0,2:0,3:0}
        self.terminations={1:False,2:False,3:False}

        observations = {
            a: np.array((self.pos[1][0],self.pos[1][1],self.pos[2][0],self.pos[2][1],self.pos[3][0],self.pos[3][1],self.weeds[1][0],self.weeds[1][1],self.weeds[2][0],self.weeds[2][1],self.weeds[3][0],self.weeds[3][1],self.weeds[4][0],self.weeds[4][1],self.weeds[5][0],self.weeds[5][1]
            ))
            for a in self.agents
        }

        # Get dummy infos. Necessary for proper parallel_to_aec conversion
        infos = {a: {} for a in self.agents}

        pygame.init()
        pygame.display.set_caption("ESCAPE THE BULLET")
        self.display = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()
        
        return observations, infos

    def step(self, actions):
        terminations = {a: False for a in self.agents}
        p=self.chargepoints[0]
        q=self.chargepoints[1]
        r=self.chargepoints[2]
        s=self.chargepoints[3]
        
        print(self.charge)
        
        def isCollision(a, b, bul_x, bul_y):
           distance = math.sqrt(math.pow(a - bul_x, 2) + math.pow(b - bul_y, 2))
           if distance < 27:
              return True
           else:
              return False
        for agent in self.agents:
         kar=agent
         agent=self.dic[agent]
         # Execute actions
         agent_action = actions[kar]
         if isCollision(p,q,self.pos[agent][0],self.pos[agent][1]) and self.run[agent]==0 and self.charge[agent]<30:
            self.rewards[agent] += 50
         if isCollision(p,q,self.pos[agent][0],self.pos[agent][1]) and self.charge[agent]<100:
            self.run[agent]=2
            self.charge[agent] += 1*0.02
            if self.charge[agent]>100:
               self.run[agent]=0
         if isCollision(r,s,self.pos[agent][0],self.pos[agent][1]) and self.run[agent]==0 and self.charge[agent]<30:
            self.rewards[agent] += 50
         if isCollision(r,s,self.pos[agent][0],self.pos[agent][1]) and self.charge[agent]<100:
            self.run[agent]=2
            self.charge[agent] += 1*0.02
            if self.charge[agent]>100:
               self.run[agent]=0
         if self.run[agent]==0:
          
          if self.charge[agent]>0:
           self.charge[agent] -= self.dis[agent]*0.1
          if self.charge[agent]<0:
             
             self.rewards[agent]=-200
             terminations={a: True  for a in self.agents}
             print(1)


          if agent_action == 0 and self.pos[agent][0] > 0:
            self.pos[agent][0] -= 1
          elif agent_action == 1 and self.pos[agent][0] < 499:
            self.pos[agent][0] += 1
          elif agent_action == 2 and self.pos[agent][1] > 0:
            self.pos[agent][1] -= 1
          elif agent_action == 3 and self.pos[agent][1] < 499:
            self.pos[agent][1] += 1
        
         x=self.pos[agent][0]
         y=self.pos[agent][1]

         print(x,y)

         for key in self.weeds:
            a = self.weeds[key][0]
            b = self.weeds[key][1]
            if isCollision(x,y,a,b) and self.run[agent]==0:
               self.rewards[agent] += 100
            
            if isCollision(x,y,a,b) :
                self.run[agent]=1
                if self.weedh[key]>0:
                 self.weedh[key] -=10
                if self.weedh[key]<=0:
                 self.charge[agent] -=10
                 self.weeds[key][0]=np.random.randint(0,500)
                 self.weeds[key][1]=np.random.randint(0,500)
                
                 self.score += 1
                 self.run[agent]=0
         

        
        def dis(a, b, bul_x, bul_y):
           distance = math.sqrt(math.pow(a - bul_x, 2) + math.pow(b - bul_y, 2))
           return distance
        
        
        if dis(self.pos[1][0],self.pos[1][1],self.pos[2][0],self.pos[2][1]) < 5:
           self.rewards[1] -= 300
           self.rewards[2] -= 300
           self.rewards[3] -= 300
           self.terminations={a: True  for a in self.agents}
           print(2)
        if dis(self.pos[1][0],self.pos[1][1],self.pos[3][0],self.pos[3][1]) < 5:
           self.rewards[1] -= 300
           self.rewards[2] -= 300
           self.rewards[3] -= 300
           self.terminations={a: True  for a in self.agents}
           print(3)
        if dis(self.pos[3][0],self.pos[3][1],self.pos[2][0],self.pos[2][1]) < 5:
           self.rewards[1] -= 300
           self.rewards[2] -= 300
           self.rewards[3] -= 300
           self.terminations={a: True  for a in self.agents}
           print(3)

        
        

        # Check truncation conditions (overwrites termination conditions)
        truncations = {a: False for a in self.agents}
         
        

        
        if any(terminations.values()) or all(truncations.values()):
            self.agents = []
        # Get observations
        observations = {
            a: np.array((self.pos[1][0],self.pos[1][1],self.pos[2][0],self.pos[2][1],self.pos[3][0],self.pos[3][1],self.weeds[1][0],self.weeds[1][1],self.weeds[2][0],self.weeds[2][1],self.weeds[3][0],self.weeds[3][1],self.weeds[4][0],self.weeds[4][1],self.weeds[5][0],self.weeds[5][1]
                
            ))
            for a in self.agents
        }

        # Get dummy infos (not used in this example)
        infos = {a: {} for a in self.agents}

       
        rewards={"drone1":self.rewards[1],"drone2":self.rewards[2],"drone3":self.rewards[3]}
        self.render()
        print(observations,actions,rewards)
        return observations, rewards, terminations, truncations, infos

    def render(self):
        

        def circle(a,b):
         circle_color = (34, 139, 34) # GREEN color in RGB
         circle_radius = 10
         pygame.draw.circle(screen, circle_color, (int(a),int(b)), circle_radius)

        height=500
        width=500
        playerImg = pygame.image.load('1.png')
       

        def weeds(i):
         v=self.weeds[i][0]
         f=self.weeds[i][1]
         
         circle(v,f)
        
        charge_wall1 = pygame.Rect(0, 250, 50, 50)
        charge_wall2 = pygame.Rect(450, 250, 50, 50)
        wall_color=(0,0,0)
        screen.fill((0, 255, 0))

        screen.blit(playerImg,(self.pos[1][0],self.pos[1][1]))
        screen.blit(playerImg,(self.pos[2][0],self.pos[2][1]))
        screen.blit(playerImg,(self.pos[3][0],self.pos[3][1]))

        weeds(1)
        weeds(2)
        weeds(3)
        weeds(4)
        weeds(5)

        pygame.draw.rect(screen, wall_color, charge_wall1)
        pygame.draw.rect(screen, wall_color, charge_wall2)

        pygame.display.update()

    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    
    def close(self):
        pygame.quit() 