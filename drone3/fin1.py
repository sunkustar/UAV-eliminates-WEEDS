import numpy as np 
import matplotlib.pyplot as plt
import gymnasium as gym
from gymnasium import spaces
import random
import pygame
import math

playerImg = pygame.image.load('drone.png')

class Drone(gym.Env):
    def __init__(self,config=None):
        super(Drone, self).__init__()
        self.action_space = spaces.Discrete(8)
        num_dimensions = 13

    # Set the identical lower and upper bounds for all dimensions
        lower_bound = np.full(num_dimensions, 0)
        upper_bound = np.full(num_dimensions, 1.0)

    # Create a 13D Box space
        self.observation_space = spaces.Box(lower_bound, upper_bound, dtype=np.float64)

        
    
    def reset(self,seed=None):
         
        self.weeds={1:[300,230],2:[450,230],3:[310,210],4:[320,230],5:[300,420]}
        self.observation=np.array([300/600,300/600,np.random.randint(100, 500)/600,np.random.randint(100, 500)/600,np.random.randint(100, 500)/600,np.random.randint(100, 500)/600,np.random.randint(100, 500)/600,np.random.randint(100, 500)/600,np.random.randint(100, 500)/600,np.random.randint(100, 500)/600,np.random.randint(100, 500)/600,np.random.randint(100, 500)/600,100/100])
        self.charge = 100
        self.old=[300,300]
        self.run=1
        self.rewards=0
        self.charger=[300,300]
        self.score=0
        pygame.init()
        pygame.display.set_caption("CATCH THE WEEDS")
        icon = pygame.image.load("drone.png")
        pygame.display.set_icon(icon)
        self.display = pygame.display.set_mode((600,600))
        self.clock = pygame.time.Clock()

        


        return self.observation,{}
    
    def step(self,action):
        terminated=False

        a= self.observation[0]*600
        b= self.observation[1]*600
        self.old=[a,b]
        if action==0  and self.run==1:
            a=a-10
        if action ==1  and self.run==1:
            a=a+10
        if action==2  and self.run==1:
            b=b-10
        if action ==3  and self.run==1:
            b=b+10
        if action ==4 and self.run==1:
            b=b+10    
            a=a+10
        if action ==5 and self.run==1:
            b=b-10    
            a=a+10    
        if action ==6 and self.run==1:
            b=b+10    
            a=a-10    
        if action ==7 and self.run==1:
            b=b-10    
            a=a-10    

        if a> 590 or b>590 or a<10 or b<10   :
           terminated=True

        if self.run==1:
         self.charge -= 0.055

        if self.charge<0 :
            terminated=True
            self.rewards -= 1000
        
        distanceo = math.sqrt(math.pow(a - self.old[0], 2) + (math.pow(b - self.old[1], 2)))
        if distanceo==0:
           self.rewards -=1

            
       
        def isCollision(a, b, bul_x, bul_y):
           distance = math.sqrt(math.pow(a - bul_x, 2) + (math.pow(b - bul_y, 2)))
           if distance < 50:
              return True
           else:
              return False
        def isCollisionw(a, b, bul_x, bul_y):
           distance = math.sqrt(math.pow(a - bul_x, 2) + (math.pow(b - bul_y, 2)))
           if distance < 50:
              return True
           else:
              return False
        for weed in self.weeds:
            p=self.weeds[weed][0]
            q=self.weeds[weed][1]

            if isCollision(a,b,p,q):
                self.rewards += 100
                self.charge -= 5
                self.weeds[weed][0]=np.random.randint(100,500)
                self.weeds[weed][1]=np.random.randint(100,500)
                self.score+=1

            distance = math.sqrt(math.pow(a - p, 2) + (math.pow(b - q, 2)))
            distancec = math.sqrt(math.pow(self.old[0] - p, 2) + (math.pow(self.old[1] - q, 2)))
            
            if distance <distancec and self.charge>30 and distance<100:
               self.rewards+=3
            else:
               self.rewards-=0.5 

        if self.charge<40 :
           distance1 = math.sqrt(math.pow(a - self.charger[0], 2) + (math.pow(b - self.charger[1], 2)))
           distance2 = math.sqrt(math.pow(self.old[0] - self.charger[0], 2) + (math.pow(self.old[1] - self.charger[1], 2)))
           if distance1 < distance2:
              self.rewards+=5
              print("char")
               
        if isCollisionw(a,b,self.charger[0],self.charger[1]) and self.run==1:
            self.run=0
            
            if self.charge<20:
               self.rewards+=300
               a=a+100
               b=b+100
            if self.charge>80:
               self.rewards-=50
               self.run=1
               a=a+100
               b=b+100
            self.charge = 100
            self.run=1
                
        
        reward=self.rewards
        truncated=False
        
        
        
        print(reward)
        print(self.charge)

        self.observation=np.array([a/600,b/600,self.weeds[1][0]/600,self.weeds[1][1]/600,self.weeds[2][0]/600,self.weeds[2][1]/600,self.weeds[3][0]/600,self.weeds[3][1]/600,self.weeds[4][0]/600,self.weeds[4][1]/600,self.weeds[5][0]/600,self.weeds[5][1]/600,self.charge/100])
        self.render()
        return self.observation, reward, terminated, truncated, {}
    
    def render(self):
        a= self.observation[0]*600
        b= self.observation[1]*600
        

        pygame.display.set_caption("Drone game")
        icon = pygame.image.load("drone.png")
        pygame.display.set_icon(icon)

        screen = pygame.display.set_mode((600,600))
        screen=self.display
        screen.fill((0, 255, 0))

      
        def circle(a,b):
         circle_color = (34, 139, 34) # GREEN color in RGB
         circle_radius = 20
         pygame.draw.circle(screen, circle_color, (int(a),int(b)), circle_radius)
        
        def weeds(i):
         v=self.weeds[i][0]
         f=self.weeds[i][1]

         circle(v,f)
         
        weeds(1)
        weeds(2)
        weeds(3)
        weeds(4)
        weeds(5)
        
        circle_color = (255, 0, 0) # GREEN color in RGB
        circle_radius = 50
        pygame.draw.circle(screen, circle_color, (int(a),int(b)), circle_radius)
        charge_wall1 = pygame.Rect(275, 275, 50, 50)
        screen.blit(playerImg,(a-25,b-25))
        pygame.draw.rect(screen, (0,0,0), charge_wall1)

        pygame.display.update()
        self.clock.tick(10)
        

    def close(self):
        pygame.quit()    
 
  
