#Made by Han_feng
#Version:Beta 1.0

import json,pygame
from Libs.Skill_lib import *
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("SCU Dungeon Demo")

font = pygame.font.Font(None,20)

test = [Skill_tree() for i in range(10)]
for i in range(len(test)):
    test[i].name = "%d"%i
    image = pygame.Surface((50,50))
    image.fill(tuple(map(lambda x:(x+1)*20,(i,i,i))))
    text = font.render(test[i].name,True,(255,255,255))
    image.blit(text,(10,10))
    test[i].image = image

test[0].set_next(test[1])
test[0].set_next(test[2])
test[0].set_next(test[4])
test[1].set_next(test[3])
test[2].set_next(test[3])
test[4].set_next(test[5])
test[6].set_last(test[3])
test[6].set_last(test[5])

screen.blit(test[0].make_tree(),(0,0))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    


    pygame.display.update()