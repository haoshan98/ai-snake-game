import pygame
import random
import os
import time
import neat
import math
pygame.font.init()  # init font

WIN_WIDTH = 600
WIN_HEIGHT = 700

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Snake Game")

SIZE = 25
STAT_FONT = pygame.font.SysFont("comicsans", 50)
DASHBOARD = 150
gen = 0

START = True
YELLOW = (255,255,0) 
GREEN = (0,255,0) 
BLUE = (0,0,255) 
WHITE = (255,255,255) 
RED = (255,0,0)
BLACK = (0,0,0)

class Snake():

    LENGTH = 7
    VEL = SIZE
    DIRECTION = 3 
    snake_length = 1
    snake_List = []
    deltaX = 0
    deltaY = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.snake_List = []
        self.snake_List.append([self.x, self.y])

    def move_up(self):  
        self.deltaX = 0
        self.deltaY = -self.VEL
        if self.check_gameover():
            print("================= Crash")
            return True
        else:
            self.length_control(self.deltaX, self.deltaY)
            print("=================", self.snake_List[-1][0], " ", self.snake_List[-1][1])
            return False

    def move_right(self):

        self.deltaX = self.VEL
        self.deltaY = 0
        if self.check_gameover():
            print("================= Crash")
            return True
        else:
            self.length_control(self.deltaX, self.deltaY)
            print("=================", self.snake_List[-1][0], " ", self.snake_List[-1][1])
            return False

    def move_down(self):
        self.deltaX = 0
        self.deltaY = self.VEL
        if self.check_gameover():
            print("================= Crash")
            return True
        else:
            self.length_control(self.deltaX, self.deltaY)
            print("=================", self.snake_List[-1][0], " ", self.snake_List[-1][1])
            return False

    def move_left(self):
        self.deltaX = -self.VEL
        self.deltaY = 0
        if self.check_gameover():
            print("================= Crash")
            return True
        else:
            self.length_control(self.deltaX, self.deltaY)
            print("=================", self.snake_List[-1][0], " ", self.snake_List[-1][1])
            return False

    def length_control(self, deltaX, deltaY):
        last_block = self.snake_List[-1]
        self.snake_List.append([last_block[0] + deltaX, last_block[1] + deltaY])
        if len(self.snake_List) > self.snake_length:
            del self.snake_List[0]

    def check_gameover(self):
        last_block = self.snake_List[-1]
        # touch boundary
        if last_block[0] >= WIN_WIDTH-SIZE or last_block[0] < 0+SIZE or last_block[1] >= WIN_HEIGHT-SIZE or last_block[1] < DASHBOARD:
            return True 
        # touch body
        for block in self.snake_List[:-1]:
            if block == self.snake_List[-1]:
                print("================= ", block[0], " ", block[1])
                return True
        return False

    def draw(self, win):
        for block in self.snake_List:
            pygame.draw.rect(win, WHITE, [block[0], block[1], SIZE, SIZE])


class Food():

    # appear_time = 
    randX = 0
    randY = 0

    def __init__(self):
        self.randX = round(random.randrange(SIZE, WIN_WIDTH-SIZE*2)/SIZE) * SIZE
        self.randY = round(random.randrange(DASHBOARD, WIN_HEIGHT-SIZE*2)/SIZE) * SIZE 
  
    def draw(self, win):
        blue = (0,0,255) 
        pygame.draw.rect(win, blue, (self.randX, self.randY, SIZE, SIZE))

    def collide(self, snake):
        if self.randX == snake.snake_List[-1][0] and self.randY == snake.snake_List[-1][1]:
            self.randX = round(random.randrange(SIZE, WIN_WIDTH-SIZE*2)/SIZE) * SIZE
            self.randY = round(random.randrange(DASHBOARD, WIN_HEIGHT-SIZE*2)/SIZE) * SIZE
            print("collide")
            return True
        return False
            

def draw_window(win, snake, food, score):
    win.fill(BLACK)
    pygame.draw.rect(win, YELLOW, (0, 0, WIN_WIDTH, SIZE))
    pygame.draw.rect(win, YELLOW, (0, DASHBOARD-SIZE, WIN_WIDTH, SIZE))
    pygame.draw.rect(win, YELLOW, (0, 0, SIZE, WIN_HEIGHT))
    pygame.draw.rect(win, YELLOW, (WIN_WIDTH-SIZE, 0, SIZE, WIN_HEIGHT))
    pygame.draw.rect(win, YELLOW, (0, WIN_HEIGHT-SIZE, WIN_WIDTH, SIZE))

    snake.draw(win)
    food.draw(win)

    score_label = STAT_FONT.render("Score: " + str(score),1, RED)
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 60, 55))

    x_label = STAT_FONT.render("x: " + str(snake.snake_List[-1][0]), 1, RED)
    win.blit(x_label, (60, 55))
    y_label = STAT_FONT.render("y: " + str(snake.snake_List[-1][1]), 1, RED)
    win.blit(y_label, (120 + x_label.get_width(), 55))

    pygame.display.update()


def control():
    snake = Snake(round(random.randrange(SIZE*3, WIN_WIDTH-SIZE*3)/SIZE) * SIZE, 
                round(random.randrange(DASHBOARD+SIZE*3, WIN_HEIGHT-SIZE*3)/SIZE) * SIZE)
    food = Food()

    END = False
    clock = pygame.time.Clock()
    score = 0
    current = round(random.randrange(0, 4))
    delay = 150
    while not END:
        
        pygame.time.delay(delay)
        clock.tick(10)
        print("running")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                END = True
                current = None
                pygame.quit()
                quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current = 0
                elif event.key == pygame.K_RIGHT:
                    current = 1
                elif event.key == pygame.K_UP:
                    current = 2
                elif event.key == pygame.K_DOWN:
                    current = 3
            
        if current == 0:
            END = snake.move_left()
        elif current == 1:
            END = snake.move_right()
        elif current == 2:
            END = snake.move_up()
        elif current == 3:
            END = snake.move_down()

        if food.collide(snake):
            score += 1
            snake.snake_length += 1
            # speed up
            if(score % 7 == 0):
                delay = round(delay*0.80)
                if delay < 100:
                    delay = 100

        draw_window(WIN, snake, food, score)


if __name__ == '__main__':
    control()



