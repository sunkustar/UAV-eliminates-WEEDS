import pygame
import math
import sys
import random
import threading
import time

pygame.init()

height=1000
width=1000

screen = pygame.display.set_mode((width,height))
Black = (0, 0, 0)

run=True

# Get the starting time
start_time = pygame.time.get_ticks()

charging_points = [10, 20, 25]


#font
FONT_SIZE = 17
TEXT_OFFSET = 3 
discharge_rate = [0.05, 0.055, 0.050, 0.068, 0.065, 0.052]

battery_power = [100, 100, 100, 100, 100, 100]

font = pygame.font.Font(None, FONT_SIZE)

def text(image,i, m, n):
    
    text = battery_power[i], discharge_rate[i]
    text = str(text)
    text_surface = font.render(text, True, Black)
    text_width, text_height = text_surface.get_width(), text_surface.get_height()
    image_width, image_height = 40, 40
    
    text_x =  m + (image_width - text_width) // 2  # Centered horizontally
    text_y = n + image_height - text_height + 9 
    screen.blit(text_surface, (text_x, text_y))






pygame.display.set_caption("Drone game")
icon = pygame.image.load("drone.png")
pygame.display.set_icon(icon)

drone1Img = pygame.image.load('drone.png')
drone2Img = pygame.image.load('drone.png')
drone3Img = pygame.image.load('drone.png')
drone4Img = pygame.image.load('drone.png')
drone5Img = pygame.image.load('drone.png')
drone6Img = pygame.image.load('drone.png')

over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))
    #pygame.time.delay(10000)


def drone(droneImg):
    droneImg = pygame.transform.scale(droneImg, (40, 40))  # Scale the image to the desired size
    return droneImg
    
drone1Img = drone(drone1Img)
drone2Img = drone(drone2Img)
drone3Img = drone(drone3Img)
drone4Img = drone(drone4Img)
drone5Img = drone(drone5Img)
drone6Img = drone(drone6Img)


def rectangle(a,b):
    rect_color = (139, 69, 19)  # Brown color in RGB
    rect_x, rect_y = a, b
    rect_width, rect_height = 50, 50
    pygame.draw.rect(screen, rect_color, (rect_x, rect_y, rect_width, rect_height))



def circle(a,b):
    circle_color = (34, 139, 34) # GREEN color in RGB
    circle_center = (a,b)
    circle_radius = 10
    pygame.draw.circle(screen, circle_color, circle_center, circle_radius)

weeds_pos = [[12,33],[122,90],[800,400],[873,345],[920,120],[122,872]]

def weeds(i,v,f):
    weeds_pos[i]= [v,f]
    circle(v,f)

def recharge_battery():
    battery_power[battery] +=  (charging_points[0]*delta_time)
    battery_power[battery] = min(battery_power[battery], 100)
    pygame.time.delay(int(delta_time * 1000))





image_rect_1 = drone1Img.get_rect()
image_rect_2 = drone2Img.get_rect()
image_rect_3 = drone3Img.get_rect()
image_rect_4 = drone4Img.get_rect()
image_rect_5 = drone5Img.get_rect()
image_rect_6 = drone6Img.get_rect()

image_rect_1.topleft = (0, 950)
image_rect_2.topleft = (0, 50)
image_rect_3.topleft = (500, 500)
image_rect_4.topleft = (500, 0)
image_rect_5.topleft = (500, 950)
image_rect_6.topleft = (950, 500)

image_pos = [image_rect_1, image_rect_2, image_rect_3, image_rect_4, image_rect_5, image_rect_6]


dragging = False
offset_x, offset_y = 0, 0

changed_battery = 0
discharging = 0
battery = 0
p =0
q = 0
w = 0
o = 0
dragged_image = None
running = True

clock = pygame.time.Clock()
delta_time = clock.tick(60) / 10000.0

weeds(0, random.randint(100, 900), random.randint(0, 1000) )
weeds(1, random.randint(100, 900), random.randint(0, 1000) )
weeds(2, random.randint(100, 900), random.randint(0, 1000) )
weeds(3, random.randint(100, 900), random.randint(0, 1000) )
weeds(4, random.randint(100, 900), random.randint(0, 1000) )
weeds(5, random.randint(100, 900), random.randint(0, 1000) )


weedh=[100,100,100,100,100,100]
sta=[1,1,1,1,1,1]

while running:
    z=0
   
    #TIME
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000
    text_time = f" Time: {elapsed_time} seconds"
    text_surface = font.render(text_time, True, Black)
    text_rect = text_surface.get_rect(center=(20, 990))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                y = 0
                for  image_rect in image_pos:
                    
                    if image_rect.collidepoint(event.pos):
                        discharging = discharge_rate[y]
                        battery = y
                        p = image_rect.left 
                        q = image_rect.top
                        dragging = True
                        dragged_image = image_rect
                        offset_x = event.pos[0] - image_rect.left
                        offset_y = event.pos[1] - image_rect.top
                        
                        


                    y = y + 1

        if event.type == pygame.MOUSEBUTTONUP :
            if event.button == 1 :  # Left mouse button
                dragging = False
                
                mouse_x, mouse_y = pygame.mouse.get_pos()
                w = dragged_image.left
                o = dragged_image.top
                u =  dragged_image.right
                s = dragged_image.bottom
                distance = math.sqrt(math.pow(w - p, 2) + math.pow(o - q, 2))
                battery_power[battery] = math.trunc(battery_power[battery] - (discharging * distance))
                dragged_image = None

                if battery_power[battery] <= 0:
                    game_over_text()
                    running=False

                
                
                ######BATTERY CHARGING NEEDS TO BE MODIFIED
                if u <= 50 and s >= 475 and o >= 475:
                    
                    delta_time = clock.tick(60) / 1000.0
                    while(battery_power[battery] < 100):    
                        battery_power[battery] +=  (charging_points[0]*delta_time)
                        battery_power[battery] = min(battery_power[battery], 100)
                        pygame.time.delay(int(delta_time * 1000))
                        
                        

        
        
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dragged_image.topleft = (mouse_x - offset_x, mouse_y - offset_y)
        
        
    
    
    screen.fill((0, 255, 0))
    
   
    print(weedh)
    for x in weeds_pos:
        a=x[0]
        b=x[1]
        print(a,b)
        circle(a,b)
        for image in image_pos:
            print(z)
            m=image[0]
            n=image[1]
            distance = math.sqrt(math.pow(a - m, 2) + (math.pow(b - n, 2)))
            if distance < 27:
                sta[z]=0
                if weedh[z]>0:
                 sta[z]=0
                 weedh[z]=weedh[z]-0.1
                 print("op")
                 
                if weedh[z]<0:
                    sta[z]=1
                    print("plus")
                    time.sleep(10)
                    image[z][0]=random.randint(100,900)
                    image[z][0]=random.randint(100,900)
                    battery_power[z]=battery_power[z]-5
            z=z+1    
             

    

    #CHARGING POINTS
    rectangle(0, 475)
    rectangle(950,950)
    rectangle(950,0)

    screen.blit(drone1Img, image_rect_1)
    screen.blit(drone2Img, image_rect_2)
    screen.blit(drone3Img, image_rect_3)
    screen.blit(drone4Img, image_rect_4)
    screen.blit(drone5Img, image_rect_5)
    screen.blit(drone6Img, image_rect_6)
    screen.blit(text_surface, text_rect)


    (a, b) = image_rect_1.topleft
    (c, d) = image_rect_2.topleft
    (e, f) = image_rect_3.topleft
    (g, h) = image_rect_4.topleft
    (i, j) = image_rect_5.topleft
    (k, l) = image_rect_6.topleft

    
    text(drone1Img,0, a, b)
    text(drone2Img,1, c, d)
    text(drone3Img,2, e, f)
    text(drone4Img,3, g, h)
    text(drone5Img,4, i, j)
    text(drone6Img,5, k, l)

    if battery_power[battery] <= 0:
            game_over_text()
            running=False

    

    pygame.display.update()

pygame.quit()
sys.exit()









