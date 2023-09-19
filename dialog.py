import pygame
from settings import *

class DialogBox:
    
    X_POSITION = 200
    Y_POSITION = screen.get_height() - 200
    
    def __init__(self, texts):
        self.box = pygame.image.load('graphics/dialog/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (1200, 150))
        self.texts = texts
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font('graphics/font/Enchanted_Land.otf', 50)
        self.reading = False
        
    def execute(self):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
        
    def render(self):
        if self.reading:
            self.letter_index += 1
            
            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
            
            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (self.X_POSITION + 80, self.Y_POSITION + 10))
        
    def next_text(self):
        self.text_index += 1
        self.letter_index = 0
        
        if self.text_index >= len(self.texts):
            self.reading = False