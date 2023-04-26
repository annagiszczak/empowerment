import pygame
import numpy as np
from sys import exit
from enum import Enum
from random import randint as rand
import copy 

#Settings
pygame.init()
width = 600
height = 600
n = 10
m = 10
N = 100 #ilosc sekwencji
L = 25 #dlugosc
M = 4 #ilosc ruchow
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Empowerment")
clock = pygame.time.Clock()
background = pygame.Surface((width, height))
background.fill((103, 169, 0))
# test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)


class Tiles(Enum):
    PATH = 0
    WALL = 1
    HOLE = -1
    BOX = 2
    GRASS = 3


class Actions(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    DO_UP = 4
    DO_DOWN = 5
    DO_LEFT = 6
    DO_RIGHT = 7

class Agent(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        #
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_1 = pygame.transform.scale(player_walk_1, (width/n,height/m))
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        player_walk_2 = pygame.transform.scale(player_walk_2, (width/n,height/m))
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.surface = self.player_walk[self.player_index]
        self.surface = pygame.transform.scale(self.surface, (width/n,height/m))
        #

        # self.surface = pygame.image.load('graphics/player.png').convert_alpha()
        # self.surface = pygame.transform.scale(self.surface, (width/n,height/m)) 

    def draw_agent(self):
        screen.blit(self.surface, (self.x*width/n,self.y*height/m))
        self.animation_state()

    def do(self, action, mapa):
        if(action == Actions.UP.value and self.y > 0 and self.y < n and mapa[self.y-1][self.x] != Tiles.WALL.value and mapa[self.y-1][self.x] != Tiles.HOLE.value):
            self.y -= 1
        elif(action == Actions.DOWN.value and self.y >= 0 and self.y < n-1 and mapa[self.y+1][self.x] != Tiles.WALL.value and mapa[self.y+1][self.x] != Tiles.HOLE.value):
            self.y += 1
        elif(action == Actions.LEFT.value and self.x > 0 and self.x < m and mapa[self.y][self.x-1] != Tiles.WALL.value and mapa[self.y][self.x-1] != Tiles.HOLE.value):
            self.x -= 1
        elif(action == Actions.RIGHT.value and self.x >= 0 and self.x < m-1 and mapa[self.y][self.x+1] != Tiles.WALL.value and mapa[self.y][self.x+1] != Tiles.HOLE.value):
            self.x += 1

        # if(mapa[self.y])
        # elif(action == Actions.DO_UP.value):
        #     self.y -= 2
        # elif(action == Actions.DO_DOWN.value):
        #     self.y += 2
        # elif(action == Actions.DO_LEFT.value):
        #     self.x -= 2
        # elif(action == Actions.DO_RIGHT.value):
        #     self.x += 2

    def quasiMove(self, initAction, sequence, mapa):
        quasiAgent = Agent(self.getXY()[0], self.getXY()[1])
        quasiAgent.do(initAction,mapa)
        for action in sequence:
            quasiAgent.do(action, mapa)
        return quasiAgent.getXY()

    def getXY(self):
        return [self.x, self.y]
    
    def empsForActions(self, mapa):
        emps = []
        for initAction in range(M):
            seqs =[]
            xys = []
            for i in range(N):
                sequence = []
                for j in range(L):
                    sequence.append(np.random.randint(0,3)) #losowanie ruchow po DANYM ruchu (w prawo)
                seqs.append(sequence)
            for i in range(N):
                    xys.append(self.quasiMove(initAction, seqs[i], mapa))
            emps.append(len(np.unique(xys, axis=0)))
        return emps
    
    def empowered(self, mapa):
        emps = self.empsForActions(mapa)
        print(emps)
        indices = [index for index, item in enumerate(emps) if item == max(emps)]
        i = np.random.randint(len(indices))
        print(indices[i], "\n")
        return indices[i] #wziac losowa wartosc z najwiekszych wartosci
    
    def animation_state(self):
        self.player_index += 1
        if self.player_index >= len(self.player_walk):self.player_index = 0
        self.surface = self.player_walk[int(self.player_index)]
        print(int(self.player_index))


class Our_map:
    def __init__(self):
        self.coords = np.array([[0,1,3,3,0,0,0,0,0,0],
                                [0,1,3,3,0,0,0,0,0,0],
                                [0,1,3,0,0,0,0,0,0,0],
                                [0,1,3,0,0,0,0,0,0,0],
                                [0,-1,3,0,0,0,0,0,0,0],
                                [0,-1,3,0,0,0,0,0,0,0],
                                [0,1,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,0],
                                [0,1,0,0,0,0,0,0,0,0],
                                [0,1,0,0,0,0,0,0,0,0]]) 
        self.path_surface = pygame.image.load('graphics/path.png').convert_alpha() #!
        self.path_surface = pygame.transform.scale(self.path_surface, (width/n,height/m)) #!
        self.grass_surface = pygame.image.load('graphics/grass.png').convert_alpha()  #!
        self.grass_surface = pygame.transform.scale(self.grass_surface, (width/n,height/m)) #!
        self.wall_surface = pygame.image.load('graphics/bigstone.png').convert_alpha()  #! convert()
        self.wall_surface = pygame.transform.scale(self.wall_surface, (width/n,height/m)) #!
        self.hole_surface = pygame.image.load('graphics/hole.png').convert()  #!
        self.hole_surface = pygame.transform.scale(self.hole_surface, (width/n,height/m)) #!


        # self.path_surface = pygame.Surface((width/n,height/m))
        # self.wall_surface = pygame.Surface((width/n,height/m))
        # self.hole_surface = pygame.Surface((width/n,height/m))
        # self.path_surface.fill("Green")
        # self.wall_surface.fill("Red")
        # self.hole_surface.fill("Black")


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
                elif(self.coords[i,j] == Tiles.GRASS.value):
                    screen.blit(self.grass_surface, (j*width/n,i*height/m))

our_map = Our_map()
agent = Agent(0,0)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background, (0, 0))
    our_map.draw_map()
    agent.draw_agent()
    agent.do(agent.empowered(our_map.coords), our_map.coords)
    


    pygame.display.update() 
    clock.tick(3)

