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
STAT_FONT = pygame.font.SysFont("comicsans", 38)
DASHBOARD = 150
gen = 0
best_score = 0

YELLOW = (255,255,0) 
GREEN = (0,255,0) 
BLUE = (0,0,255) 
WHITE = (255,255,255) 
RED = (255,0,0)
BLACK = (0,0,0)

class Snake():

    LENGTH = 7
    VEL = SIZE
    direciton = round(random.randrange(0, 4)) 
    last_direction = direciton
    snake_length = 1
    snake_List = []
    deltaX = 0
    deltaY = 0
    score = 0

    def __init__(self):
        self.x = round(random.randrange(SIZE*3, WIN_WIDTH-SIZE*3)/SIZE) * SIZE
        self.y = round(random.randrange(DASHBOARD+SIZE*3, WIN_HEIGHT-SIZE*3)/SIZE) * SIZE
        self.snake_List = []
        self.snake_List.append([self.x, self.y])

    def move_left(self):
        self.deltaX = -self.VEL
        self.deltaY = 0
        self.direciton = 0
        if self.check_gameover():
            return True
        else:
            self.length_control(self.deltaX, self.deltaY)
            return False

    def move_right(self):

        self.deltaX = self.VEL
        self.deltaY = 0
        self.direciton = 1
        if self.check_gameover():
            return True
        else:
            self.length_control(self.deltaX, self.deltaY)
            return False

    def move_up(self):  
        self.deltaX = 0
        self.deltaY = -self.VEL
        self.direciton = 2
        if self.check_gameover():
            return True
        else:
            self.length_control(self.deltaX, self.deltaY)
            return False

    def move_down(self):
        self.deltaX = 0
        self.deltaY = self.VEL
        self.direciton = 3
        if self.check_gameover():
            return True
        else:
            self.length_control(self.deltaX, self.deltaY)
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
                return True
        return False

    def draw(self, win):
        for block in self.snake_List:
            pygame.draw.rect(win, WHITE, [block[0], block[1], SIZE, SIZE])


class Food():
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
            return True
        return False

    def generate(self):
        self.randX = round(random.randrange(SIZE, WIN_WIDTH-SIZE*2)/SIZE) * SIZE
        self.randY = round(random.randrange(DASHBOARD, WIN_HEIGHT-SIZE*2)/SIZE) * SIZE
            

def draw_window(win, snakes, food, best_score, gen):
    win.fill(BLACK)
    pygame.draw.rect(win, YELLOW, (0, 0, WIN_WIDTH, SIZE))
    pygame.draw.rect(win, YELLOW, (0, DASHBOARD-SIZE, WIN_WIDTH, SIZE))
    pygame.draw.rect(win, YELLOW, (0, 0, SIZE, WIN_HEIGHT))
    pygame.draw.rect(win, YELLOW, (WIN_WIDTH-SIZE, 0, SIZE, WIN_HEIGHT))
    pygame.draw.rect(win, YELLOW, (0, WIN_HEIGHT-SIZE, WIN_WIDTH, SIZE))

    score = 0
    max = 0
    for i, snake in enumerate(snakes):
        snake.draw(win)
        if snake.score > max:
            max = snake.score
    score = max
    food.draw(win)

    score_label = STAT_FONT.render("Score: " + str(score) + " [Best : " + str(best_score) + "]", 1, RED)
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 60, 55))
    
    gen_label = STAT_FONT.render("Generation: " + str(gen), 1, RED)
    win.blit(gen_label, (60, 55))

    pygame.display.update()


def control(genomes, config):
    global best_score
    global gen
    gen += 1

    food = Food()

    nets = []
    ge = []
    snakes = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness value 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(Snake())
        ge.append(genome)


    END = False
    clock = pygame.time.Clock()
    score = 0
    delay = 150
    frame = 1
    
    while (not END) and (len(snakes) > 0):
        pygame.time.delay(delay)
        clock.tick(10)
        # print("running, frame : ", frame)
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                END = True
                current = None
                pygame.quit()
                quit()
                break

        # give each snake a fitness of 0.1 for each frame it stays alive
        for x, snake in enumerate(snakes):  
            ge[x].fitness -= 0.1

        # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            dist = math.sqrt((snake.snake_List[-1][0] - food.randX)**2 + (snake.snake_List[-1][1] - food.randY)**2)
            radian = math.atan2((snake.snake_List[-1][0] - food.randX), (snake.snake_List[-1][1] - food.randY))
            degree = math.degrees(radian)
            output = nets[snakes.index(snake)].activate((snake.last_direction, dist, degree,
                snake.snake_List[-1][0], snake.snake_List[-1][1], food.randX, food.randY))

            for i, value in enumerate(output):
                print(value)
                
            max_value = max(output)
            snake.direction = output.index(max_value)

            # print("snake ", x, " x ", snake.snake_List[-1][0], " y ", snake.snake_List[-1][1])
            print("direction : ", snake.direction, " last : ", snake.last_direction)
            isDead = False
            if snake.direction == 0:
                isDead = snake.move_left()
            elif snake.direction == 1:
                isDead = snake.move_right()
            elif snake.direction == 2:
                isDead = snake.move_up()
            elif snake.direction == 3:
                isDead = snake.move_down()
            snake.last_direction = snake.direciton

            if isDead:
                ge[x].fitness -= 5
                nets.pop(snakes.index(snake))
                ge.pop(snakes.index(snake))
                snakes.pop(snakes.index(snake))

            elif food.collide(snake):
                food.generate()
                ge[x].fitness += 25
                snake.score += 1
                if snake.score > best_score:
                    best_score = snake.score

                snake.snake_length += 1
                for idx, other_snake in enumerate(snakes):
                    if other_snake is not snake:
                        ge[idx].fitness -= 5
                # END = True

                # speed up
                # if(score % 7 == 0):
                #     delay = round(delay*0.80)
                #     if delay < 100:
                #         delay = 100

            else: # get closer
                if dist < 50:
                    ge[x].fitness += 0.2
                elif dist < 100:
                    ge[x].fitness += 0.1
               
        if frame > 70:
            for snake in snakes:
                ge[snakes.index(snake)].fitness -= 5
                END = True
        draw_window(WIN, snakes, food, best_score, gen)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # create population, the top-level object for a NEAT run.
    p = neat.Population(config)

    # stdout reporter to show progress in terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for 100 generations.
    winner = p.run(control, 100)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # set configuration file to current working directory
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

