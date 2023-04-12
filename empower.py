import pygame
import numpy as np
from sys import exit
from enum import Enum
from random import randint as rand

#Settings
pygame.init()
width = 600
height = 600
n = 6
m = 6
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Empowerment")
clock = pygame.time.Clock()
# test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)


class Tiles(Enum):
    PATH = 0
    WALL = 1
    HOLE = -1

class Actions(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    DO_UP = 4
    DO_DOWN = 5
    DO_LEFT = 6
    DO_RIGHT = 7

class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.surface = pygame.Surface((width/n,height/m))
        self.surface.fill("Blue")
        # self.coords = np.array([x,y])

    def draw_agent(self):
        screen.blit(self.surface, (self.x*width/n,self.y*height/m))
# duzo warunkow na to co on moze robic (wziac pod uwage ograniczenia)
# zrobic funkcje ktora nie rusza graficznie agentem ale zwraca jego nowe polozenie
# empowererment to suma wszystkich unikalnych koncowych polozen agenta z wylosowanej probki
#  ta funkcja powinna przyjmowac dlugosc ciagu i ilosc losowan
# na koncu wykonac sekwencje ruchow dazaca do maksymalnego empoweeremtu 
    def do(self):
        action = rand(Actions.UP.value, Actions.RIGHT.value)
        if(action == Actions.UP.value and self.y > 0 and self.y < n):
            self.y -= 1
        elif(action == Actions.DOWN.value and self.y >= 0 and self.y < n-1):
            self.y += 1
        elif(action == Actions.LEFT.value and self.x > 0 and self.x < m):
            self.x -= 1
        elif(action == Actions.RIGHT.value and self.x >= 0 and self.x < m-1):
            self.x += 1
        # elif(action == Actions.DO_UP.value):
        #     self.y -= 2
        # elif(action == Actions.DO_DOWN.value):
        #     self.y += 2
        # elif(action == Actions.DO_LEFT.value):
        #     self.x -= 2
        # elif(action == Actions.DO_RIGHT.value):
        #     self.x += 2


class Our_map:
    def __init__(self):
        self.coords = np.array([[0,0,0,-1,0,0],[0,0,0,-1,0,0],[0,0,0,-1,0,0],[0,1,0,-1,0,0],[0,0,0,-1,0,0],[0,0,0,-1,0,0]]) 
        self.path_surface = pygame.Surface((width/n,height/m))
        self.wall_surface = pygame.Surface((width/n,height/m))
        self.hole_surface = pygame.Surface((width/n,height/m))
        self.path_surface.fill("Green")
        self.wall_surface.fill("Red")
        self.hole_surface.fill("Black")


    def draw_map(self):
        n,m = self.coords.shape
        for j in range(n):
            for i in range(m):
                if(self.coords[i,j] == Tiles.PATH.value):
                    screen.blit(self.path_surface, (j*width/n,i*height/m))
                elif(self.coords[i,j] == Tiles.WALL.value):
                    screen.blit(self.wall_surface, (j*width/n,i*height/m))
                elif(self.coords[i,j] == Tiles.HOLE.value):
                    screen.blit(self.hole_surface, (j*width/n,i*height/m))


our_map = Our_map()
agent = Agent(m-1,n-1)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    our_map.draw_map()
    agent.draw_agent()
    agent.do()



    pygame.display.update() 
    clock.tick(3)

