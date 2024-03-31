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

def text_insert(text:str,pos:int,insert_text:str):
    return text[:pos] + insert_text + text[pos:]

class Base_box:
    def __init__(self,rect:pygame.Rect):
        self.rect = rect
        self.image = pygame.Surface(self.rect.size)
    
    def set_pos(self,pos:tuple):
        self.rect.topleft = pos

    def show(self,surface:pygame.Surface):
        surface.blit(self.image,self.rect)

    def __contains__(self,rect:pygame.Rect):
        return rect in self.rect

class Text_box(Base_box):
    def __init__(self,rect:pygame.Rect,font:pygame.font.Font,width:int=0): #rect.size is meaningless,the size will generate automatically
        Base_box.__init__(self,rect)
        self.text = ""
        self.width = width
        self.font = font

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
        self.rect.size = self.image.get_size()
        
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

class Scroll_box(Base_box):
    def __init__(self,rect:pygame.Rect,image:pygame.Surface,bar_width=0):
        Base_box.__init__(self,rect)
        self.master_image = image
        self.bar_width = bar_width
        self.image_y = 0

    def update(self,mouse_pos:tuple=(-1,-1),mouse_y_rel:int=0):
        self.image.fill((0,0,0))
        mouse_rect = pygame.Rect(mouse_pos,(0,0))
        delta_height = self.master_image.get_height()-self.rect.height
        self.image_y = min(delta_height,max(0,self.image_y+mouse_y_rel*-10)) if mouse_rect in self.rect else self.image_y
        image_rect = self.rect.move(0,self.image_y)

        #whether to draw the scroll bar
        if self.bar_width and delta_height > 0:
            bar_height = self.rect.height**2/self.master_image.get_height()
            bar_y = self.image_y*(self.rect.height-bar_height)/delta_height
            image_rect.size = (image_rect.width-self.bar_width,image_rect.height)
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

class Button_box(Base_box):
    def __init__(self,rect:pygame.Rect,image:pygame.Surface,keep_clicked:bool=False,highlight:bool=False):
        Base_box.__init__(self,rect)
        self.master_image = image
        self.keep_clicked = keep_clicked
        self.highlight = highlight
        self.on_click = False

        if not image.get_rect(topleft=self.rect.topleft) in self.rect:
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
        self.rect = rect if rect else self.master_image.get_rect(topleft=self.rect.topleft)
        if not self.master_image.get_rect(topleft=self.rect.topleft) in rect:
            raise OverflowError("The rect offered is smaller than the rect of the image!")
        self.update()
        
    def set_image(self,image:pygame.Surface):
        self.master_image = image.copy()
        if not image.get_rect(topleft=self.rect.topleft) in self.rect:
            self.rect = image.get_rect()
        self.update()

class Input_box(Base_box):
    def __init__(self,rect:pygame.Rect,text_font:pygame.font.Font,description_font:pygame.font.Font=None,length_limit:int=0):
        Base_box.__init__(self,rect)
        self.text_box = Text_box(pygame.Rect(rect.topleft,(0,0)),text_font,rect.width)
        self.description_box = Text_box(pygame.Rect(rect.topleft,(0,0)),description_font if description_font else text_font)
        self.description_width = 0
        self.length_limit = length_limit
        self.is_input = False
        self.is_cursor = False
        self.cursor_pos = 0
        self.last_time = 0
        self.text = ""
        self.res_text = ""

    def update(self,current_time=0,mouse_pos:tuple=(-1,-1),mouse_click:tuple=(False,False),text_input:list=["","",0],enter_click:bool=False,move_cursor:tuple=(False,False)) -> bool: #text_input <- Event_handler.get_text_input()
        mouse_rect = pygame.Rect(mouse_pos,(0,0))
        if self.is_input:
            if mouse_click[1] or (mouse_click[0] and mouse_rect not in pygame.Rect(0,self.description_width,self.rect.width-self.description_width,self.rect.height)):
                self.is_input = False
                self.is_cursor = False
                self.text = text_insert(self.text,self.cursor_pos,text_input[1])
                self.text_box.set_text(self.text)
                pygame.key.stop_text_input()
                return False
            if enter_click:
                self.submit_text()
                return True
            if current_time - self.last_time >= 60:
                self.is_cursor = not self.is_cursor
            if text_input[0]:
                self.text = text_insert(self.text,self.cursor_pos,text_input[1])
                self.cursor_pos += len(self.text)
            if not text_input[1]:
                if move_cursor[0]:
                    self.cursor_pos = max(self.cursor_pos-1,0)
                elif move_cursor[1]:
                    self.cursor_pos = min(self.cursor_pos+1,len(self.text))
            text_list = [self.text[:self.cursor_pos],"<underline=True>",text_input[1][:text_input[2]],"|" if self.is_cursor else "",text_input[1][text_input[2]:],"<underline=False>",self.text[self.cursor_pos:]]
            self.text_box.set_text("".join(text_list))
            pygame.key.set_text_input_rect(pygame.Rect(self.text_box.font.size(text_list[0]+text_list[2])[0]%(self.text_box.width if self.text_box.width else self.text_box.rect.width)+self.text_box.rect.width,self.text_box.rect.height,0,0))
        elif mouse_click[0] and mouse_rect in pygame.Rect(self.description_width,self.rect.top,self.rect.width-self.description_width,self.rect.height):
            self.is_input = True
            self.cursor_pos = len(self.text)
            pygame.key.start_text_input()
        return False
            
    def set_description(self,description:str=""):
        self.description_box.set_text(description)
        self.description_width = self.description_box.image.get_width()
        self.text_box.set_width(self.rect.width-self.description_width)
        self.text_box.rect.left = self.rect.left + self.description_width
        self.update()

    def submit_text(self):
        self.res_text = self.text
        self.text = ""
        self.cursor_pos = 0
        self.update()

    def set_pos(self,pos:tuple):
        super().set_pos(pos)
        self.description_box.rect.topleft = pos
        self.text_box.rect.topleft = (self.rect.left+self.description_width,self.rect.top)

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