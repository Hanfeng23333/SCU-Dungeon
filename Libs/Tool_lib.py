#Made by Han_feng
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

class Text_box:
    def __init__(self,font:pygame.font.Font,width:int=0,color:tuple=(255,255,255)):
        self.text = ""
        self.font = font
        self.width = width
        self.color = color
        self.image = None

    def update(self):
        #create multiple lines of string
        width, max_width, str_list, line = 0, 0, [], ""
        for char,w in zip(self.text,[i[4] for i in self.font.metrics(self.text)]):
            if char == "\n" or (width + w > self.width and self.width):
                str_list.append(line)
                width,line = 0,""
                if char == "\n":
                    continue
            line += char
            width += w
            max_width = max(max_width,width)
        if line:
            str_list.append(line)

        #create a blank image and draw the lines on it
        height_per_line = self.font.get_linesize()
        self.image = pygame.Surface([self.width if self.width else max_width,height_per_line*len(str_list)])
        for i,line in enumerate(str_list):
            self.image.blit(self.font.render(line,True,self.color),(0,height_per_line*i))
        
    
    def set_text(self,text:str):
        self.text = text
        self.update()

    def set_font(self,font:pygame.font.Font):
        self.font = font
        self.update()

    def set_width(self,width=0):
        self.width = width
        self.update()

    def set_color(self,color:tuple):
        self.color = color
        self.update()

class Scroll_box:
    def __init__(self,image:pygame.Surface,rect:pygame.Rect,bar_width=0):
        self.master_image = image
        self.rect = rect
        self.image = pygame.Surface(self.rect.size)
        self.bar_width = bar_width
        self.image_y = 0

    def update(self,mouse_pos:tuple=(0,0),mouse_y_rel:int=0):
        self.image.fill((0,0,0))
        mouse_rect = pygame.Rect(mouse_pos,(0,0))
        delta_height = self.master_image.get_height()-self.rect.height
        self.image_y = min(delta_height,max(0,self.image_y+mouse_y_rel*-10)) if mouse_rect in self.rect else self.image_y
        image_rect = self.rect.move(0,self.image_y)

        #whether to draw the scroll bar
        if self.bar_width and delta_height > 0:
            bar_height = self.rect.height**2/self.master_image.get_height()
            bar_y = self.image_y*(self.rect.height-bar_height)/delta_height
            image_rect.update(image_rect.topleft,(image_rect.width-self.bar_width,image_rect.height))
            bar_rect = pygame.Rect(self.rect.width-self.bar_width,0,self.bar_width,self.rect.height)

            #draw the scroll bar
            pygame.draw.line(self.image,(255,255,255),bar_rect.topleft,bar_rect.bottomleft)
            pygame.draw.rect(self.image,(119,136,153),pygame.Rect(bar_rect.left+1,bar_y,self.bar_width-1,bar_height))

        try:
            image_crop = self.master_image.subsurface(image_rect)
        except:
            image_crop = self.master_image
        
        self.image.blit(image_crop,(0,0))

    def set_image(self,image:pygame.Surface):
        self.image = image
        self.update()