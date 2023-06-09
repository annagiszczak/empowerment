import pygame
import numpy as np
from sys import exit
from enum import Enum
from random import randint as rand
import timeit
from threading import Thread
#Settings
pygame.init()
width = 800
height = 700
n = 10
m = 10
N = 10000 #ilosc sekwencji
L = 25 #dlugosc
M = 8 #ilosc ruchow
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Empowerment")
clock = pygame.time.Clock()
background = pygame.Surface((width, height))
background.fill((103, 169, 0))
# test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)

class ThreadWithResult(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


class Tiles(Enum):
    PATH = 0
    WALL = 1
    HOLE = -1
    BOX = 2
    GRASS = 3
    SIANO = 4
    SIANOHOLE = 5

def ifBlock(value): 
    if(value == 0 or value == 3 or value == 5):
        return False
    else:
        return True

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
        self.maSianko = False

        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_1 = pygame.transform.scale(player_walk_1, (width/n,height/m))
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        player_walk_2 = pygame.transform.scale(player_walk_2, (width/n,height/m))
        #sianko 
        player_walk_1_sianko = pygame.image.load('graphics/player/player_walk_1_sianko.png').convert_alpha()
        player_walk_1_sianko = pygame.transform.scale(player_walk_1_sianko, (width/n,height/m))
        player_walk_2_sianko = pygame.image.load('graphics/player/player_walk_2_sianko.png').convert_alpha()
        player_walk_2_sianko = pygame.transform.scale(player_walk_2_sianko, (width/n,height/m))

        self.player_walk = [player_walk_1,player_walk_2]
        self.player_walk_sianko = [player_walk_1_sianko,player_walk_2_sianko]
        self.player_index = 0
        self.surface = self.player_walk[self.player_index]
        self.surface = pygame.transform.scale(self.surface, (width/n,height/m))

    def draw_agent(self, map):
        screen.blit(self.surface, (self.x*width/n,self.y*height/m))
        self.animation_state()

    def do(self, action, map):
        if(action == Actions.UP.value and (self.y > 0 and self.y < n) and not ifBlock(map[self.y-1][self.x])):
            self.y -= 1
        elif(action == Actions.DOWN.value and (self.y >= 0 and self.y < n-1) and not ifBlock(map[self.y+1][self.x])):
            self.y += 1
        elif(action == Actions.LEFT.value and (self.x > 0 and self.x < m) and not ifBlock(map[self.y][self.x-1])):
            self.x -= 1
        elif(action == Actions.RIGHT.value and (self.x >= 0 and self.x < m-1) and not ifBlock(map[self.y][self.x+1])):
            self.x += 1

        elif(action == Actions.DO_UP.value and (self.y > 0 and self.y < n)):
            if(self.maSianko):
                if(map[self.y-1][self.x] == Tiles.PATH.value):
                    map[self.y-1][self.x] = Tiles.SIANO.value
                    self.maSianko = False
                elif(map[self.y-1][self.x] == Tiles.HOLE.value):
                    map[self.y-1][self.x] = Tiles.SIANOHOLE.value
                    self.maSianko = False
            else:
                if(map[self.y-1][self.x] == Tiles.SIANO.value):
                    map[self.y-1][self.x] = Tiles.PATH.value
                    self.maSianko = True
                elif(map[self.y-1][self.x] == Tiles.SIANOHOLE.value):
                    map[self.y-1][self.x] = Tiles.HOLE.value
                    self.maSianko = True

        elif(action == Actions.DO_DOWN.value and (self.y >= 0 and self.y < n-1)):
            if(self.maSianko):
                if(map[self.y+1][self.x] == Tiles.PATH.value):
                    map[self.y+1][self.x] = Tiles.SIANO.value
                    self.maSianko = False
                elif(map[self.y+1][self.x] == Tiles.HOLE.value):
                    map[self.y+1][self.x] = Tiles.SIANOHOLE.value
                    self.maSianko = False
            else:
                if(map[self.y+1][self.x] == Tiles.SIANO.value):
                    map[self.y+1][self.x] = Tiles.PATH.value
                    self.maSianko = True
                elif(map[self.y+1][self.x] == Tiles.SIANOHOLE.value):
                    map[self.y+1][self.x] = Tiles.HOLE.value
                    self.maSianko = True

        elif(action == Actions.DO_LEFT.value and (self.x > 0 and self.x < m)):
            if(self.maSianko):
                if(map[self.y][self.x-1] == Tiles.PATH.value):
                    map[self.y][self.x-1] = Tiles.SIANO.value
                    self.maSianko = False
                elif(map[self.y][self.x-1] == Tiles.HOLE.value):
                    map[self.y][self.x-1] = Tiles.SIANOHOLE.value
                    self.maSianko = False
            else:
                if(map[self.y][self.x-1] == Tiles.SIANO.value):
                    map[self.y][self.x-1] = Tiles.PATH.value
                    self.maSianko = True
                elif(map[self.y][self.x-1] == Tiles.SIANOHOLE.value):
                    map[self.y][self.x-1] = Tiles.HOLE.value
                    self.maSianko = True

        elif(action == Actions.DO_RIGHT.value and (self.x >= 0 and self.x < m-1)):
            if(self.maSianko):
                if(map[self.y][self.x+1] == Tiles.PATH.value):
                    map[self.y][self.x+1] = Tiles.SIANO.value
                    self.maSianko = False
                elif(map[self.y][self.x+1] == Tiles.HOLE.value):
                    map[self.y][self.x+1] = Tiles.SIANOHOLE.value
                    self.maSianko = False
            else:
                if(map[self.y][self.x+1] == Tiles.SIANO.value):
                    map[self.y][self.x+1] = Tiles.PATH.value
                    self.maSianko = True
                elif(map[self.y][self.x+1] == Tiles.SIANOHOLE.value):
                    map[self.y][self.x+1] = Tiles.HOLE.value
                    self.maSianko = True

    def getXY(self):
        return [self.x, self.y]

    def quasiMove(self, initAction, map, quasiAgent):
        quasiAgent.x = self.x
        quasiAgent.y = self.y
        quasiAgent.maSianko = self.maSianko
        quasiMap = map.copy()
        # print(quasiMap)
        quasiAgent.do(initAction,quasiMap)
        for i in range(L):
            quasiAgent.do(rand(0, M-1), quasiMap)
        return quasiAgent.getXY()

    def getEmps(self, initAction, map):
        quasiAgent = Agent(self.x, self.y)
        xys = [self.quasiMove(initAction, map, quasiAgent) for i in range(N)]

        return len(np.unique(xys, axis=0))

    def empsForActions(self, map):
        return [self.getEmps(initAction, map) for initAction in range(0,M)]
    
    def empowered(self, map):
        t = [None]*M
        for i in range(0, M):
            t[i]  = ThreadWithResult(target=self.getEmps, args=(i, map))
            t[i].start()

        for i in range(0, M):
            t[i].join()

        emps = [t[i].result for i in range(0, M)]
        # emps = self.empsForActions(map)
        print(emps)
        indices = [index for index, item in enumerate(emps) if item == max(emps)]
        i = rand(0, len(indices)-1)
        print(indices[i], "\n")
        return indices[i]
    
    def animation_state(self):
        if(self.maSianko==True):
            self.player_index += 1
            if self.player_index >= len(self.player_walk_sianko):self.player_index = 0
            self.surface = self.player_walk_sianko[int(self.player_index)]
        else:
            self.player_index += 1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.surface = self.player_walk[int(self.player_index)]

class OurMap:
    def __init__(self, coords):
        self.coords = coords
        self.path_surface = pygame.image.load('graphics/path.png').convert_alpha()
        self.path_surface = pygame.transform.scale(self.path_surface, (width/n,height/m)) 
        self.grass_surface = pygame.image.load('graphics/grass.png').convert_alpha() 
        self.grass_surface = pygame.transform.scale(self.grass_surface, (width/n,height/m)) 
        self.wall_surface = pygame.image.load('graphics/bigstone.png').convert_alpha()
        self.wall_surface = pygame.transform.scale(self.wall_surface, (width/n,height/m)) 
        self.hole_surface = pygame.image.load('graphics/hole.png').convert_alpha() 
        self.hole_surface = pygame.transform.scale(self.hole_surface, (width/n,height/m))
        self.siano_surface = pygame.image.load('graphics/siano.png').convert_alpha() 
        self.siano_surface = pygame.transform.scale(self.siano_surface, (width/n,height/m))
        self.holewith_surface = pygame.image.load('graphics/holewithsiano.png').convert_alpha() 
        self.holewith_surface = pygame.transform.scale(self.holewith_surface, (width/n,height/m))

    def drawMap(self):
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
                elif(self.coords[i,j] == Tiles.SIANO.value):
                    screen.blit(self.siano_surface, (j*width/n,i*height/m))
                elif(self.coords[i,j] == Tiles.SIANOHOLE.value):
                    screen.blit(self.holewith_surface, (j*width/n,i*height/m))

coords  = np.array([[0,1,3,3,0,0,0,0,0,0],
                    [0,1,3,3,0,0,0,0,0,0],
                    [4,1,3,0,0,4,4,4,0,0],
                    [0,1,3,0,0,4,0,4,0,0],
                    [4,-1,-1,0,0,4,4,4,0,0],
                    [0,-1,3,0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,4,-1,0,0],
                    [0,1,0,0,0,0,0,0,0,3],
                    [4,1,0,0,0,0,0,0,3,3],
                    [0,1,3,3,3,3,3,3,3,3]]) 

ourMap = OurMap(coords)
agent = Agent(0,3)
# agent = Agent(6,3)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background, (0, 0))
    ourMap.drawMap()
    agent.draw_agent(ourMap.coords)
    start = timeit.default_timer()

    agent.do(agent.empowered(ourMap.coords), ourMap.coords)

    # agent.do(5, ourMap.coords)


    print("The difference of time is :", timeit.default_timer() - start)
        
    pygame.display.update() 
    clock.tick(10)

