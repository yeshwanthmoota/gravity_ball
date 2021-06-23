import pygame
import os
import time

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

WIDTH = 1000
HEIGHT = 600
BALL_RADIUS = 20
PLATFORM_HEIGHT = 1
PLATFORM_WIDTH = 200
PLATFORM_VER_GAP = 50
PLATFORM_HOR_GAP = 75
FPS = 100
GRAVITY = 2000
INITIAL_VER_VEL = -750
VER_VEL = 0
BALL_HOR_VEL = 2
MAX_HEIGHT = (INITIAL_VER_VEL**2) / (2*GRAVITY)


WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
ORANGE = (255, 165, 0)


gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))

PLATFORM_1 = pygame.Rect(0 + 20, HEIGHT - PLATFORM_HEIGHT - 200, PLATFORM_WIDTH, PLATFORM_HEIGHT)

PLATFORM_0 = pygame.Rect(0 , PLATFORM_1.y + MAX_HEIGHT, WIDTH, PLATFORM_HEIGHT)

PLATFORM_2 = pygame.Rect(PLATFORM_1.x + PLATFORM_WIDTH + PLATFORM_HOR_GAP, PLATFORM_1.y - MAX_HEIGHT + PLATFORM_HEIGHT + PLATFORM_VER_GAP, PLATFORM_WIDTH, PLATFORM_HEIGHT)

PLATFORM_3 = pygame.Rect(PLATFORM_2.x + PLATFORM_WIDTH + PLATFORM_HOR_GAP, PLATFORM_2.y - MAX_HEIGHT + PLATFORM_HEIGHT + PLATFORM_VER_GAP, PLATFORM_WIDTH, PLATFORM_HEIGHT)

PLATFORM_4 = pygame.Rect(PLATFORM_3.x + PLATFORM_WIDTH + PLATFORM_HOR_GAP, PLATFORM_2.y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

PLATFORM_5 = pygame.Rect(PLATFORM_2.x, PLATFORM_3.y - MAX_HEIGHT + PLATFORM_HEIGHT + PLATFORM_VER_GAP, PLATFORM_WIDTH, PLATFORM_HEIGHT)

LIST_PLATFORM = [PLATFORM_0 ,PLATFORM_1, PLATFORM_2, PLATFORM_3, PLATFORM_4, PLATFORM_5]





#----------------------code for working on terminal----------
final_path = os.getcwd()
path_list = final_path.split("\\")
# print(final_path)
final_path = final_path + "\\"
if path_list[-1] == "gravity_ball" or  path_list[-1] == "gravity_ball-master":
    pass
#----------------------code for working on terminal----------

#----------------------code for working on vs code----------
else:
    final_path = os.path.dirname(__file__) + "\\"
    # print(final_path)
#----------------------code for working on vs code----------




file1 = open(final_path + "log_vel_x_y.txt", "w")
file1.write("")
file1.close()
file1 = open(final_path + "log_vel_x_y.txt", "a")



class Ball():
    def __init__(self):
        self.x = 0 + 20 + BALL_RADIUS # initial position
        self.y = PLATFORM_1.y - BALL_RADIUS# initial position  # Will be placed on platform 1
        self.initial_y = PLATFORM_1.y -BALL_RADIUS
        self.ver_vel = 0
        self.on_platform = PLATFORM_1
        self.time = 0


    def ball_hor_movement(self, keys_pressed): # Horizontal movement
        if keys_pressed[pygame.K_a] and ((self.x -BALL_RADIUS) > 0):
                self.x -= BALL_HOR_VEL
        if keys_pressed[pygame.K_d] and (self.x + BALL_RADIUS < WIDTH):
                self.x += BALL_HOR_VEL
        
        if self.ver_vel == 0:
            if not(self.on_platform.x < self.x < self.on_platform.x + self.on_platform.width):
                # Then should add a y-component to the speed and it should start falling down
                time_count = time.time()
                self.ball_ver_movement(time_count, 2) # fall down


    def ball_ver_movement(self, time_count, num = 0): # Vertical movement
        global VER_VEL

        if(num == 1): # provide the ball with a jump from the platform
            self.ver_vel = INITIAL_VER_VEL
            self.time = time_count # Initial time recording
            VER_VEL = INITIAL_VER_VEL
            file1.write(f"\n\n\n\nTHIS IS A JUMP-----vertical velocity = {self.ver_vel}\n\n\n\n")

        elif(num == 2): # provide the ball with a fall from the platform
            self.ver_vel = 1
            self.time =time_count
            VER_VEL = 1
            file1.write(f"\n\n\n\nTHIS IS A FALL-----vertical velocity = {self.ver_vel}\n\n\n\n")

        else:
            list_check = self.ball_plat_collision(LIST_PLATFORM)
            if list_check[0]: # if the ball hits the platform
                self.y = list_check[1].y -BALL_RADIUS
                self.initial_y = list_check[1].y -BALL_RADIUS # Initial y on new platform
                self.on_platform = list_check[1]
                self.ver_vel = 0
                file1.write("\n\n\n\nHITS THE PLATFORM\n\n\n\n")
            else: # '<=' case
                t = time_count - self.time
                self.y = self.initial_y + (VER_VEL * t) + (1/2)*GRAVITY*(t**2) # s = (u*t) + (1/2)*(a)*(t**2)
                self.ver_vel = VER_VEL + (GRAVITY * t) # v = u + a*t
                # print(f"self.ver_vel = {self.ver_vel}, self.y ={self.y}")
                file1.write(f"self.ver_vel = {self.ver_vel}, self.x ={self.x}, self.y ={self.y}\n\n")

    
    def ball_plat_collision(self, list_platform):
        i = len(list_platform) - 1
        while i >= 0:
            if (list_platform[i].x) < (self.x) < (list_platform[i].x + list_platform[i].width):
                if((list_platform[i].y)< (self.y + BALL_RADIUS) < (list_platform[i].y + PLATFORM_HEIGHT + BALL_RADIUS)):
                    return [True, list_platform[i]]
            i -= 1
        return [False, 0]



def draw_display(gameDisplay, ball, list_platform):
    gameDisplay.fill(BLACK)
    for platform in list_platform: # draw all the platforms
        pygame.draw.rect(gameDisplay, WHITE, platform)
    pygame.draw.circle(gameDisplay, RED, (int(ball.x), int(ball.y)), BALL_RADIUS) # draw the ball
    pygame.display.update()

def main():
    running = True
    ball = Ball()

    clock = pygame.time.Clock()

    while running:

        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE) and (round(ball.y,2) == ball.initial_y):
                    time_count = time.time()
                    ball.ball_ver_movement(time_count, 1)
        
        if(ball.ver_vel != 0):
            time_count = time.time()
            ball.ball_ver_movement(time_count)
        ball.ball_hor_movement(keys_pressed)
        draw_display(gameDisplay, ball, LIST_PLATFORM)
    file1.close() 
    pygame.quit()

if __name__ == '__main__':
    main()