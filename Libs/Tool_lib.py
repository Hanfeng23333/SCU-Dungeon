#Made by Han_feng
import pygame,re
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
        res.append([(start[0],middle_y),(end[0],middle_y)])
    return res

def image_selected(surface:pygame.Surface,color:tuple=(255,215,0),size=3):
    width,height = surface.get_size()
    res_image = surface.copy()
    pygame.draw.line(res_image,color,(0,0),(width/4,0),size)
    pygame.draw.line(res_image,color,(0,0),(0,height/4),size)
    pygame.draw.line(res_image,color,(0,height-1),(0,height*3/4),size)
    pygame.draw.line(res_image,color,(0,height-1),(width/4,height-1),size)
    pygame.draw.line(res_image,color,(width-1,0),(width*3/4,0),size)
    pygame.draw.line(res_image,color,(width-1,0),(width-1,height/4),size)
    pygame.draw.line(res_image,color,(width-1,height-1),(width-1,height*3/4),size)
    pygame.draw.line(res_image,color,(width-1,height-1),(width*3/4,height-1),size)
    return res_image

class Text_box:
    def __init__(self,font:pygame.font.Font,width:int=0):
        self.text = ""
        self.font = font
        self.width = width
        self.image = pygame.Surface([width,0])

    def update(self):
        #Preprocess
        step, operations = 0,[]
        for tag in re.finditer(r"<.*?>",self.text.replace("\n","")):
            start,end = tag.span()
            order = tag.group()[1:-1].split("=")
            if order[0] == "color":
                operations.append((order[0],order[1],start-step))
            else:
                operations.append((order[0],eval(order[1]),start-step))
            step += end-start
        text = re.sub("<.*?>","",self.text)

        #create multiple lines of string
        width, max_width, str_list, line = 0, 0, [], ""
        for char,w in zip(text,[i[4] for i in self.font.metrics(text)]):
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
        attrs = {"color":"#FFFFFF","underline":False,"bold":False,"strikethrough":False,"italic":False}
        funs = {"color":lambda color:None,
                "underline":self.font.set_underline,
                "bold":self.font.set_bold,
                "strikethrough":self.font.set_strikethrough,
                "italic":self.font.set_italic}
        self.image = pygame.Surface([self.width if self.width else max_width,height_per_line*len(str_list)])

        attr,value,position = operations.pop(0) if operations else (0,0,-1)
        step,width = 0,0
        for i,line in enumerate(str_list):
            length,pos = len(line),position-step
            while pos >= 0 and pos < length:
                print(attr,value,pos,line[:pos])
                font_image = self.font.render(line[:pos],True,attrs["color"])
                self.image.blit(font_image,(width,height_per_line*i))
                width += font_image.get_width()
                step += len(line[:pos])
                line = line[pos:]
                attrs[attr] = value
                funs[attr](value)
                attr,value,position = operations.pop(0) if operations else (0,0,-1)
                pos = position-step
            self.image.blit(self.font.render(line,True,attrs["color"]),(width,height_per_line*i))
            step += len(line)
            width = 0
        
        #Font reset
        for i in funs:
            funs[i](False)
    
    def set_text(self,text:str):
        if self.text != text:
            self.text = text
            self.update()

    def set_font(self,font:pygame.font.Font):
        self.font = font
        self.update()

    def set_width(self,width=0):
        self.width = width
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
        self.master_image = image.copy()
        self.update()

class Button_box:
    def __init__(self,image:pygame.Surface,rect:pygame.Rect=None,keep_clicked:bool=False,highlight:bool=False):
        self.master_image = image
        self.rect = rect if rect else image.get_rect()
        self.image = pygame.Surface(self.rect.size)
        self.keep_clicked = keep_clicked
        self.highlight = highlight
        self.on_click = False

        if not image.get_rect() in self.rect:
            raise OverflowError("The rect offered is smaller than the rect of the image!")
        
    def update(self,mouse_pos:tuple=(-1,-1),mouse_click:tuple=(False,False)) -> bool:
        clicked = False
        self.image.fill((0,0,0))
        mouse_rect = pygame.Rect(mouse_pos,(0,0))
        if mouse_click[1]:
            self.on_click = False
        elif mouse_click[0]:
            if mouse_rect in self.rect:
                clicked = True
                self.on_click = self.keep_clicked
            else:
                self.on_click = False
        self.image.blit(self.master_image,((self.rect.width-self.master_image.get_width())/2,(self.rect.height-self.master_image.get_height())/2))
        if (mouse_rect in self.rect and self.highlight) or self.on_click:
            self.image = image_selected(self.image)
        return clicked

    def set_rect(self,rect:pygame.Rect):
        self.rect = rect if rect else self.master_image.get_rect()
        if not self.master_image.get_rect() in rect:
            raise OverflowError("The rect offered is smaller than the rect of the image!")
        self.update()
        
    def set_image(self,image:pygame.Surface):
        self.master_image = image.copy()
        if not image.get_rect() in self.rect:
            self.rect = image.get_rect()
        self.update()

class Event_handler:
    def __init__(self):
        self.last_mouse = None
        self.last_key = None
        self.mouse = None
        self.key = None
        self.middle_mouse_y_rel = 0
        self.mouse_rel = [0,0]
        self.mouse_transform = {"left":0,"middle":1,"right":2}
        self.mouse_pos = [0,0]
        self.text = ""
        self.edit_text = ""
        self.edit_pos = 0
        self.clock = pygame.time.Clock()

        self.update()

    def update(self):
        self.last_mouse = self.mouse
        self.last_key = self.key
        self.middle_mouse_y_rel = 0
        self.edit_text = ""
        self.edit_pos = 0
        self.text = ""

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEWHEEL:
                self.middle_mouse_y_rel = event.y
            elif event.type == TEXTEDITING:
                self.edit_text = event.text
                self.edit_pos = event.start
            elif event.type == TEXTINPUT:
                self.text = event.text

        self.key = pygame.key.get_pressed()
        self.mouse = pygame.mouse.get_pressed()
        self.mouse_rel = pygame.mouse.get_rel()
        self.mouse_pos = pygame.mouse.get_pos()
        self.clock.tick_busy_loop()

    def get_key(self,key_value:int=-1):
        if key_value == -1:
            return [not i and j for i,j in zip(self.last_key,self.key)]
        return not self.last_key[key_value] and self.key[key_value]

    def get_mouse(self,mouse_value:str=""):
        if not mouse_value:
            return [not i and j for i,j in zip(self.last_mouse,self.mouse)]
        return not self.last_mouse[self.mouse_transform[mouse_value]] and self.mouse[self.mouse_transform[mouse_value]]

    def get_hold_key(self,key_value:int=-1):
        if key_value == -1:
            return [i for i in self.key]
        return self.key[key_value]

    def get_hold_mouse(self,mouse_value:str=""):
        if not mouse_value:
            return [i for i in self.mouse]
        return self.mouse[self.mouse_transform[mouse_value]]

    def get_middle_mouse_rel(self):
        return self.middle_mouse_y_rel
    
    def get_mouse_rel(self):
        return self.mouse_rel
    
    def get_mouse_pos(self):
        return self.mouse_pos
    
    def get_text_input(self):
        return [self.text,self.edit_text,self.edit_pos]
    
    def get_past_time(self):
        return self.clock.get_time()
    
    def get_current_time(self):
        return pygame.time.get_ticks()