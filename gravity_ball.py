import pygame, sys, os

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

# Game constants
WIDTH = 1080
HEIGHT = 600


BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)


PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 1
PLATFORM_VER_GAP = 100
PLATFORM_HOR_GAP = 50
GAP = 50

BALL_RADIUS = 20
BALL_X_SPEED = 7
# JUMP_NUMBER = 0
# MAX_JUMP_NUMBER = 2 # giving the ball a double jump feature
J_COUNT = 7
MAX_J_COUNT = 7 # this is like the initial speed we are giving to the ball
MUL_FACTOR = 1/2
IS_JUMP = False

FPS = 60


PLATFORM_0 = pygame.Rect(0, HEIGHT -100 , WIDTH, PLATFORM_HEIGHT+20) # Ball initially on platform 0

PLATFORM_1 = pygame.Rect(PLATFORM_0.x , PLATFORM_0.y - PLATFORM_VER_GAP- PLATFORM_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT)

PLATFORM_2 = pygame.Rect(PLATFORM_1.x + PLATFORM_WIDTH + PLATFORM_HOR_GAP + GAP, PLATFORM_1.y - PLATFORM_VER_GAP- PLATFORM_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT)

PLATFORM_3 = pygame.Rect(PLATFORM_2.x + PLATFORM_WIDTH + PLATFORM_HOR_GAP + GAP, PLATFORM_2.y - PLATFORM_VER_GAP- PLATFORM_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT)

PLATFORM_4 = pygame.Rect(PLATFORM_3.x + PLATFORM_WIDTH + PLATFORM_HOR_GAP + GAP, PLATFORM_2.y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

PLATFORM_5 = pygame.Rect(PLATFORM_2.x, PLATFORM_3.y - PLATFORM_VER_GAP- PLATFORM_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT)

LIST_PLATFORMS = [PLATFORM_0 ,PLATFORM_1, PLATFORM_2, PLATFORM_3, PLATFORM_4, PLATFORM_5]


class Ball():
    def __init__(self):
        self.x = PLATFORM_0.x + BALL_RADIUS
        self.y = PLATFORM_0.y - BALL_RADIUS
        self.platform = PLATFORM_0

    def hor_movement(self, keys_pressed):
        global J_COUNT
        global IS_JUMP
        if keys_pressed[pygame.K_a] and self.x - BALL_RADIUS > 0:
            self.x -= BALL_X_SPEED
            if (self.x not in range(self.platform.x, self.platform.x + self.platform.width)) and not(IS_JUMP) and J_COUNT==MAX_J_COUNT:
                J_COUNT = 0
                IS_JUMP = True
        if keys_pressed[pygame.K_d] and self.x + BALL_RADIUS < WIDTH:
            self.x += BALL_X_SPEED
            if (self.x not in range(self.platform.x, self.platform.x + self.platform.width)) and not(IS_JUMP) and J_COUNT==MAX_J_COUNT:
                J_COUNT = 0
                IS_JUMP = True


    def ver_movement(self):
        global IS_JUMP
        global J_COUNT


        if (IS_JUMP == True):
            if J_COUNT >= -MAX_J_COUNT:
                neg = -1 # velocity is in the negative direction of y
                if(J_COUNT < 0):
                    neg = 1 # velocity is in the positive direction of y
                self.y += (J_COUNT ** 2) * MUL_FACTOR * neg
                J_COUNT -= 0.5 # we can change the gravity of the jump by changing the value we subtract here
                            # example if we change it like J_COUNT -= 0.5 gravity of the jump decreases
                            # example if we change it like J_COUNT -= 2 gravity of the jump increases
            else:
                self.y += (J_COUNT ** 2) * MUL_FACTOR # the last J_COUNT
        if self.ball_plat_collision(): # Till the ball collides with one of the platforms IS_JUMP is True
            # Once it hits any platform we are gonna reset the JUMP_NUMBER to 0 and J_COUNT to 10
            IS_JUMP = False
            J_COUNT = MAX_J_COUNT
            return 1


    def ball_plat_collision(self):
        ball_rect = pygame.Rect(self.x - BALL_RADIUS/2, self.y - BALL_RADIUS, BALL_RADIUS, BALL_RADIUS)
        # in ball_rect we are checking if the middle part of the ball is colliding with any platform
        for platform in LIST_PLATFORMS:
            
            if self.x in range(platform.x - BALL_RADIUS, platform.x + platform.width):
                if(ball_rect.colliderect(platform)): #collided into the platform
                    self.y = platform.y - BALL_RADIUS
                    self.platform = platform
                    return True
        return False


def draw_display(ball):
    gameDisplay.fill(BLACK)

    for platform in LIST_PLATFORMS:
        pygame.draw.rect(gameDisplay, WHITE, platform)

    pygame.draw.circle(gameDisplay, RED, (int(ball.x), int(ball.y)), BALL_RADIUS)

    pygame.display.update()


gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))


def main():
    global IS_JUMP

    running = True

    clock = pygame.time.Clock()

    ball = Ball()

    while running:

        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    IS_JUMP = True
        ball.hor_movement(keys_pressed)
        x = ball.ver_movement()
        if(x is not 1):
            draw_display(ball)
        
    pygame.quit()

if __name__ == '__main__':
    main()