#made by Han_feng
import pygame
from pygame.locals import *
pygame.init()

def create_gradient_image(width:int,height:int,color_path:tuple,is_lateral:bool = True) -> pygame.Surface:
    image = pygame.Surface([width,height])
    if is_lateral:
        color_step = tuple(map(lambda x,y:(y-x)/width,*color_path))
        for i in range(width):
            color = tuple(map(lambda x,s:int(x+s*i),color_path[0],color_step))
            pygame.draw.line(image,color,(i,0),(i,height))
    else:
        color_step = tuple(map(lambda x,y:(y-x)/height,*color_path))
        for i in range(height):
            color = tuple(map(lambda x,s:int(x+s*i),color_path[0],color_step))
            pygame.draw.line(image,color,(0,i),(width,i))
    return image

def establish_connection(start:tuple,end:tuple) -> list:
    middle_y = (start[1]+end[1])/2
    res = [[start,(start[0],middle_y)],[(end[0],middle_y),end]]
    if start[0] != end[0]:
        res.append(sorted([(start[0],middle_y),(end[0],middle_y)],key=lambda x:x[0]))
    return res