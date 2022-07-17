import pygame
import sys
import random

#Creating global variables
GRIDSIZE = 30
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
#Key positions
LEFT = (-1,0)
RIGHT = (1,0)
UP = (0,-1)
DOWN = (0,1)

#Method that creates the grid
def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x+y)%2 == 0:
                i = pygame.Rect((x*GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface,(151, 150 , 157), i)
            else:
                j = pygame.Rect((x*GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (137, 124, 128), j)

#Creating class Fruit that has some methods, such as draw() - draws the fruit and random_position() - draws the fruit at the random postion every time the action happens
class Fruit():
    def __init__(self):
        self.position = (0,0)
        self.color = (110, 152, 135)
        self.random_position()

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (181, 191, 161), r, 1)

    def random_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)

#Creating class Snake that has class methods
class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (242, 131, 182)
        self.score = 0

    #Method that gets the postion of the first block of the snake
    def get_position(self):
        return self.positions[0]

    #Method that lets the snake turn into any of the four sides
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        current = self.get_position()
        x,y = self.direction
        new = (((current[0] + (x * GRIDSIZE)) % SCREEN_WIDTH), (current[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    #Method that resets the snake to the default when the game ends
    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_WIDTH / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    #Method that draws the snake
    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (224,108, 159), r, 1)

    #Method that defines which keys can move the snake in to different sides
    def keys(self):
        for action in pygame.event.get():
            if action.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif action.type == pygame.KEYDOWN:
                if action.key == pygame.K_a:
                    self.turn(LEFT)
                elif action.key == pygame.K_d:
                    self.turn(RIGHT)
                elif action.key == pygame.K_w:
                    self.turn(UP)
                elif action.key == pygame.K_s:
                    self.turn(DOWN)

def main():
    #Creating game enviroment
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    #Calling drawGrid function that draws the surface and updates it after each action
    drawGrid(surface)
    myfont = pygame.font.SysFont("arial", 24 )
    snake = Snake()
    fruit = Fruit()

    while (True):
        clock.tick(10)
        snake.keys()
        drawGrid(surface)
        snake.move()
        if snake.get_position() == fruit.position:
            snake.length += 1
            snake.score += 1
            fruit.random_position()
        snake.draw(surface)
        fruit.draw(surface)
        screen.blit(surface, (0,0))
        text = myfont.render("Your score is: {0}".format(snake.score), 1, (0,0,0))
        screen.blit(text, (8,14))
        pygame.display.update()

main()