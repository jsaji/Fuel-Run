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


class Player:
    def __init__(self, screen, move_speed):
        plane_choice = ["Blue", "Green", "Mono", "Pink", "Red", "Retro", "Tech", "Purple", ]
        self.img = pygame.image.load("Resources/Images/"+plane_choice[random.randint(0, 7)]+"Plane.png")
        self.screen = screen
        self.x_pos = int(self.screen.get_size()[0]/5)
        self.y_pos = int(self.screen.get_size()[1]/2)
        self.move_speed = move_speed
        self.draw()
        self.rotation = 0

    def move(self, move_x, move_y, rotate=0):
        if move_x > 0: self.x_pos += self.move_speed
        elif move_x < 0: self.x_pos -= self.move_speed
        if move_y > 0: self.y_pos += self.move_speed
        elif move_y < 0: self.y_pos -= self.move_speed
        self.draw()

    def rotate(self, rotation):
        self.img = pygame.transform.rotate(self.img, rotate)
        self.draw()

    def move_to(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.draw()

    def reset(self):
        self.x_pos = int(self.screen.get_size()[0]/5)
        self.y_pos = int(self.screen.get_size()[1]/2)
        self.rotate(-self.rotation)
        self.draw()

    def draw(self):
        self.check_bounds()
        self.screen.blit(self.img, (self.x_pos, self.y_pos))

    def check_bounds(self):
        screen_dim = self.screen.get_size()
        if self.x_pos > screen_dim[0]:
            self.x_pos = 0
        elif self.x_pos < -120:
            self.x_pos = screen_dim[0]
        if self.y_pos > screen_dim[1]:
            self.y_pos = 0
        elif self.y_pos < -55:
            self.y_pos = screen_dim[1]
        