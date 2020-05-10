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

    def draw(self):
        if self.is_horizontal: self.x_pos += self.speed
        else: self.y_pos += self.speed
        if self.y_pos < -100 or self.x_pos < -400: self.reset()
        self.screen.blit(self.img, (self.x_pos, self.y_pos))

    def reset(self):
        self.speed = random.randint(self.speed_range[0], self.speed_range[1])
        if self.is_horizontal:
            self.x_pos = self.screen.get_size()[0] + random.randint(10, 60)
            self.y_pos = random.randint(self.pos_range[0], self.pos_range[1])
        else:
            self.y_pos = self.screen.get_size()[1] + random.randint(30, 80)
            self.x_pos = random.randint(self.pos_range[0], self.pos_range[1])

class FuelBox:
    def __init__(self, pos_range, box_size, text_size, screen):
        self.pos_range = pos_range
        self.screen = screen
        self.box_size = box_size
        self.text_size = text_size
        self.number = 0
        self.box_colour = (160, 32, 240)
        self.text_colour = (240, 248, 255)
        self.speed = -10
        self.x_pos = 0
        self.y_pos = 0

    def reset(self, number, speed):
        self.x_pos = self.screen.get_size()[0] + random.randint(30, 70)
        self.y_pos = random.randint(self.pos_range[0], self.pos_range[1])
        self.number = number
        self.speed = speed

    def draw(self):
        self.x_pos += self.speed
        pygame.draw.rect(self.screen, self.box_colour, (self.x_pos, self.y_pos, self.box_size, self.box_size))
        self.display_text(str(self.number), (self.x_pos, self.y_pos))

    def check_bounds(self):
        return self.x_pos < -2 * self.box_size
    
    def display_text(self, text, pos):
        font = pygame.font.Font("Resources/BULKYPIX.ttf", self.text_size)
        text_surface = font.render(text, True, self.text_colour)
        disp_pos = text_surface.get_rect()
        disp_pos.center = (int(pos[0] + self.box_size/2), int(pos[1] + self.box_size/2))
        self.screen.blit(text_surface, disp_pos)
    
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

    def move(self, move_x, move_y):
        if move_x > 0: self.x_pos += self.move_speed
        elif move_x < 0: self.x_pos -= self.move_speed
        if move_y > 0: self.y_pos += self.move_speed
        elif move_y < 0: self.y_pos -= self.move_speed
        self.draw()

    def rotate(self, rotation):
        self.img = pygame.transform.rotate(self.img, rotation)
        self.draw()

    def move_to(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.draw()

    def reset(self):
        self.x_pos = int(self.screen.get_size()[0]/5)
        self.y_pos = int(self.screen.get_size()[1]/2)
        if (self.rotation):
            self.rotate(-self.rotation)
            self.rotation = 0
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

    def hit_object(self, x_range, y_range):
        return (self.x_pos >= x_range[0] and self.x_pos <= x_range[1] and self.y_pos >= y_range[0] and self.y_pos <= y_range[1])
        