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

test = Text_box(font,170)
test_plus = Scroll_box(test.image,pygame.Rect(0,0,170,200))

buttons = [Button_box(pygame.image.load("%d.png"%i),keep_clicked=True,highlight=True) for i in range(1,6)]

while True:
    y_rel = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEWHEEL:
            y_rel = event.y
    
    mouse_x,mouse_y = pygame.mouse.get_pos()
    left_mouse,_,right_mouse = pygame.mouse.get_pressed()
    target = -1

    for i in range(5):
        buttons[i].update((mouse_x-1000,mouse_y-150*(i+1)),(left_mouse,right_mouse))
        if buttons[i].on_click:
            target = i
    test.set_text(texts[target])
    test_plus.set_image(test.image)
    test_plus.update((mouse_x-20,mouse_y-20),y_rel)

    screen.fill((0,0,0))
    for i in range(5):
        screen.blit(buttons[i].image,(1000,150*(i+1)))
    screen.blit(test_plus.image,(100,100))

    pygame.display.update()