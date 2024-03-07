#Made by Han_feng
#Version:Beta 1.0

import json,pygame
from Libs.Skill_lib import *
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((1200,900))
pygame.display.set_caption("SCU Dungeon Demo")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    