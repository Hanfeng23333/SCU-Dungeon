#Made by Han_feng
import pygame
from pygame.locals import *
from Libs.Tool_lib import *
pygame.init()

class Skill_tree:
    def __init__(self):
        self.name = ""
        self.text = ""
        self.rect = pygame.Rect(0,0,50,50)
        self.image = None
        self.is_locked = False
        self.level = 0
        self.limit_level = 0
        self.last_skills = []
        self.next_skills = []
    
    def __eq__(self,other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def cast(self,caster,target):
        pass

    def upgrade(self):
        pass

    def make_tree(self):
        #count the skills in the tree
        skill_list = [[self]]
        next_skill = []
        max_length = 1
        while True:
            for skill in skill_list[-1]:
                next_skill += skill.next_skills
            if not next_skill:
                break
            skill_list.append(sorted(list(set(next_skill)),key=lambda x:next_skill.index(x)))
            max_length = max(max_length,len(skill_list[-1]))
            next_skill = []
        
        #make up the background
        surface_size = [max_length*self.rect.width*2,len(skill_list)*self.rect.height*2]
        color_map = [(0,245,255),(25,25,112)] #[start_color,end_color]
        skill_image:pygame.Surface = create_gradient_image(*surface_size,color_map,False)
        skill_image.set_alpha(175)

        #set the position of every skill and draw them up
        for y,skills in enumerate(skill_list):
            start_x = (surface_size[0]-(2*len(skills)-1)*self.rect.width)/2
            for x,skill in enumerate(skills):
                skill.rect.update((start_x+2*x*skill.rect.width,(2*y+0.5)*skill.rect.height),skill.rect.size)
                skill_image.blit(skill.image,skill.rect)
                for last in skill.last_skills:
                    for start,end in establish_connection(last.rect.midbottom,skill.rect.midtop):
                        pygame.draw.line(skill_image,(255,255,255),start,end,3)

        return skill_image

    def set_last(self,last_skill):
        last_skill.next_skills.append(self)
        self.last_skills.append(last_skill)

    def set_next(self,next_skill):
        next_skill.last_skills.append(self)
        self.next_skills.append(next_skill)