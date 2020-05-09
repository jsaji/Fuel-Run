import pygame
import random    

class Cloud:
    def __init__(self, speed_range, is_horizontal, pos_range, screen):
        self.x_pos = 0
        self.y_pos = 0
        self.speed = 0
        self.speed_range = speed_range
        self.is_horizontal = is_horizontal
        self.pos_range = pos_range
        self.screen = screen
        self.img = pygame.image.load("Resources/Images/Cloud.png")
        self.reset()

    def update(self):
        if self.is_horizontal:
            self.x_pos += self.speed
        else:
            self.y_pos += self.speed
        
        if self.y_pos < -100 or self.x_pos < -400:
            self.reset()
        
        self.screen.blit(self.img, (self.x_pos, self.y_pos))

    def reset(self):
        self.speed = random.randint(self.speed_range[0], self.speed_range[1])
        if self.is_horizontal:
            self.x_pos = self.screen.get_size()[0] + random.randint(10, 60)
            self.y_pos = random.randint(self.pos_range[0], self.pos_range[1])
        else:
            self.y_pos = self.screen.get_size()[1] + random.randint(30, 80)
            self.x_pos = random.randint(self.pos_range[0], self.pos_range[1])