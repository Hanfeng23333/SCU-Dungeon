#Made by Han_feng
import pygame
from pygame.locals import *
pygame.init()

class Skill_tree:
    def __init__(self):
        self.name = ""
        self.text = ""
        self.image = None
        self.limit_level = 0
        self.last_skills = []
        self.next_skills = []
    
    def init(self,name:str = "",image:pygame.Surface = pygame.Surface((50,50)),level:int = 0,last:list = [],next:list = []):
        self.name = name
        self.image = image
        self.limit_level = level
        self.last_skills = last
        self.next_skills = next

    def load_text(self,text:str = ""):
        self.text = text
    
    def cast(self,caster,target):
        pass

    def create_image(self):
        skill_seq = [[self]]
        depth = 0
        while True:
            next_depth_skills = []
            for skill in skill_seq[depth]:
                next_depth_skills += skill.next_skills
            if not next_depth_skills:
                break
            skill_seq.append(next_depth_skills)
            depth += 1
        skill_board = None
