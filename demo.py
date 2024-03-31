#Made by Han_feng
#Version:Beta 1.0

import json,pygame,math,os
from Libs.Skill_lib import *
from Libs.Tool_lib import *
from pygame.locals import *
pygame.init()
os.environ["SDL_IME_SHOW_UI"] = "1" # This environment variable is important,which isn't added the candidate list will not show

screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("Demo")

font = pygame.font.Font("Assets/Genshin_impact_font.ttf",25)
font1 = pygame.font.Font("Assets/Genshin_impact_font.ttf",50)

text = """<color=#00FF00>全能(5):
两件套:全属性+15%
四件套:每当你造成伤害时,使你后续造成的伤害+7%;每当你受到伤害时,使你后续受到的伤害-7%。两种效果独立存在,且至多叠加3层,持续5s"""

test = Text_box(pygame.Rect(1200,600,0,0),font,310)
test1 = Text_box(pygame.Rect(1200,200,0,0),font1,200)
test.set_text(text)

buttons = [Button_box(pygame.Rect(0,0,100,100),pygame.image.load("%d.png"%i),keep_clicked=True,highlight=True) for i in range(1,6)]
texts = ["始","魔法少女芙乐艾","懒","PantheraLeo","C#是世界上最好的语言",""]
angles = [0,72,144,216,288]
speed = 0.05

event_handler = Event_handler()

while True:
    event_handler.update()

    y_rel = event_handler.get_middle_mouse_rel()
    left_mouse,_,right_mouse = event_handler.get_mouse()
    mouse_x,mouse_y = event_handler.get_mouse_pos()

    target = -1
    pos = list(map(lambda x:(600+300*math.cos(math.radians(x))-50,600+300*math.sin(math.radians(x))-50),angles))

    for i in range(5):
        buttons[i].set_pos(pos[i])
        buttons[i].update((mouse_x,mouse_y),(left_mouse,right_mouse))
        if buttons[i].on_click:
            target = i
            speed = 0 if angles[target] == 90 else (0.3 if (angles[target]+90)%360 < 180 else -0.3)

    test1.set_text(texts[target])

    screen.fill((0,0,0))
    test.show(screen)
    test1.show(screen)
    
    for i in range(5):
        buttons[i].show(screen)
        angles[i] = (angles[i]+speed)%360
    
    if target == -1:
        speed = 0.05
    elif abs(angles[target]-90) < 0.3:
        angles[target] = 90

    pygame.display.update()