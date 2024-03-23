#Made by Han_feng
#Version:Beta 1.0

import json,pygame
from Libs.Skill_lib import *
from Libs.Tool_lib import *
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("Demo")

font = pygame.font.SysFont("simhei",20)
"""
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

"""
text = """喜欢test的原因可以有很多，足够写出长长的小作文来阐述自己的喜爱
喜欢test的原因也可以只有一个，就是，我喜欢test
每个人都有自己的喜欢，我选择的喜欢是test
喜欢很简单，难的是坚持这份喜欢
人的一生很长也很短，可以和test一起度过的时光也只是人生路上的一段
但是在这一段时光里，我喜欢test，我会一直喜欢test"""

test = Text_box(font,170)
test.set_text(text)


test_plus = Scroll_box(test.image,pygame.Rect(0,0,170,200))

while True:
    y_rel = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEWHEEL:
            y_rel = event.y
    
    mouse_x,mouse_y = pygame.mouse.get_pos()
    test_plus.update((mouse_x-900,mouse_y-20),y_rel)

    screen.blit(test.image,(20,20))
    screen.blit(test_plus.image,(900,20))

    pygame.display.update()