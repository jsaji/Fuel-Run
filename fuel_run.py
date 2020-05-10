import pygame
import time
import sys
import random
from parts import Cloud, Player, FuelBox

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

game_icon = pygame.image.load("Resources/Images/Icon.png")
pygame.display.set_icon(game_icon)
display_width, display_height = 1280, 720
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Fuel Run")
clock = pygame.time.Clock()

c_blue = (31, 117, 254)
csi_blue = (40, 110, 225)
a_blue = (240, 248, 255)
s_blue = (63, 157, 255)
i_red = (237, 41, 57)
purple = (160, 32, 240)
black, white = (0, 0, 0), (255, 255, 255)

button_green, buttonover_green = (70, 205, 60), (11, 230, 81)
button_red, buttonover_red = (200, 40, 50), (255, 40, 50)
button_orange, buttonover_orange = (255, 125, 24), (255, 159, 24)
button_yellow, buttonover_yellow = (255, 200, 0), (253, 230, 0)

crash_sound = pygame.mixer.Sound("Resources/Sound/WrongAnswer.wav")
coll_sound = pygame.mixer.Sound("Resources/Sound/RightAnswer.wav")
button_sound = pygame.mixer.Sound("Resources/Sound/ButtonPress.wav")
gameover_sound = pygame.mixer.Sound("Resources/Sound/GameOver.wav")

PAUSE = False
HIGHSCORE = 0

player = Player(screen, 25)

# For each difficulty, the following are stored: maximum time table no., speed of the fuel boxes, points gained from each correct answer, and the no. of lives
difficulty = {'easy':[6, 1.01, 5, 3], 'medium': [12, 1.02, 10, 4], 'hard': [16, 1.03, 15, 5]}
section = [[(-100, 300), (350, 650), (700, 1000)], [(5, 210), (240, 440), (460, 670)]]
cloud_speed = (-20, -10)

def level_select():

    clouds = [Cloud(cloud_speed, 1, section[1][i], screen) for i in range(3)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if 40 + 160 > mouse[0] and mouse[0] > 40 and 40 + 60 > mouse[1] and mouse[1] > 40:
                    pygame.mixer.Sound.play(button_sound)
                    return False
                elif 515 + 250 > mouse[0] and mouse[0] > 515 and 250 + 80 > mouse[1] and mouse[1] > 250:
                    pygame.mixer.Sound.play(button_sound)
                    while (keep_going):
                        keep_going = game_loop(difficulty['easy'])
                    return False
                elif 515 + 250 > mouse[0] and mouse[0] > 515 and 400 + 80 > mouse[1] and mouse[1] > 400:
                    pygame.mixer.Sound.play(button_sound)
                    while (keep_going):
                        keep_going = game_loop(difficulty['medium'])
                    return False
                elif 515 + 250 > mouse[0] and mouse[0] > 515 and 550 + 80 > mouse[1] and mouse[1] > 550:
                    pygame.mixer.Sound.play(button_sound)
                    while (keep_going):
                        keep_going = game_loop(difficulty['hard'])
                    return False
                
        screen.fill(s_blue)
        for cloud in clouds: cloud.draw()

        display_text("Choose difficulty:", i_red, 50, (display_width/2, display_height/4.5))
        diff_button_size = 40
        mouse = pygame.mouse.get_pos()
        keep_going = True

        btn_hover = 40 + 160 > mouse[0] and mouse[0] > 40 and 40 + 60 > mouse[1] and mouse[1] > 40
        pygame.draw.rect(screen, csi_blue*btn_hover or button_red*(not btn_hover), (40, 40, 160, 60))
        display_text("Home", a_blue, 30, (65, 60), False)
        
        btn_hover = 515 + 250 > mouse[0] and mouse[0] > 515 and 250 + 80 > mouse[1] and mouse[1] > 250
        pygame.draw.rect(screen, buttonover_green*btn_hover or button_green*(not btn_hover), (515, 250, 250, 80))
        display_text("Easy", a_blue, diff_button_size, (display_width/2, 290))

        btn_hover = 515 + 250 > mouse[0] and mouse[0] > 515 and 400 + 80 > mouse[1] and mouse[1] > 400
        pygame.draw.rect(screen, buttonover_yellow*btn_hover or button_yellow*(not btn_hover), (515, 400, 250, 80))
        display_text("Medium", a_blue, diff_button_size, (display_width/2, 440))
        
        btn_hover = 515 + 250 > mouse[0] and mouse[0] > 515 and 550 + 80 > mouse[1] and mouse[1] > 550
        pygame.draw.rect(screen, buttonover_red*btn_hover or button_red*(not btn_hover), (515, 550, 250, 80))
        display_text("Hard", a_blue, diff_button_size, (display_width/2, 590))

        pygame.display.update()
        clock.tick(30)
            
def game_over(score):
    global HIGHSCORE
    pygame.mixer.Sound.play(gameover_sound)
    
    clouds = [Cloud(cloud_speed, 0, section[0][i], screen) for i in range(3)]
    rotation = 1
    player.reset()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if 520 + 240 > mouse[0] and mouse[0] > 520 and 310 + 120 > mouse[1] and mouse[1] > 310:
                    pygame.mixer.Sound.play(button_sound)
                    return True
                if 540 + 200 > mouse[0] and mouse[0] > 540 and 500 + 100 > mouse[1] and mouse[1] > 500:
                    pygame.mixer.Sound.play(button_sound)
                    return False
        
        screen.fill(s_blue)

        for cloud in clouds: cloud.draw()

        if HIGHSCORE > score:
            HIGHSCORE = score
            display_text("New Highscore: "+str(HIGHSCORE)+"!", i_red, 70, (display_width/2, display_height/4.5))
        else:
            display_text("Score: "+str(score)+"!", i_red, 70, (display_width/2, display_height/4.5))
        
        mouse = pygame.mouse.get_pos()

        btn_hover = 520 + 240 > mouse[0] and mouse[0] > 520 and 310 + 120 > mouse[1] and mouse[1] > 310
        pygame.draw.rect(screen, buttonover_green*btn_hover or button_red*(not btn_hover), (520, 310, 240, 120))
        pygame.draw.polygon(screen, white, ((610, 330), (610, 410), (690, 370)))

        btn_hover = 540 + 200 > mouse[0] and mouse[0] > 540 and 500 + 100 > mouse[1] and mouse[1] > 500
        pygame.draw.rect(screen, csi_blue*btn_hover or button_red*(not btn_hover), (540, 500, 200, 100))
        display_text("Home", a_blue, 45, (display_width/2, 555))
        #player.rotate(rotation)

        pygame.display.update()
        clock.tick(30)

def main_menu():
    pygame.mixer.music.load("Resources/Sound/Overworld.mp3")
    pygame.mixer.music.play(-1)
    
    x_change, y_change = 0, 0
    clouds = [Cloud(cloud_speed, 1, section[1][i], screen) for i in range(3)]
    player.reset()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -1
                if event.key == pygame.K_RIGHT:
                    x_change = 1
                if event.key == pygame.K_DOWN:
                    y_change = 1
                if event.key == pygame.K_UP:
                    y_change = -1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    y_change = 0
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if 520 + 240 > mouse[0] and mouse[0] > 520 and 310 + 120 > mouse[1] and mouse[1] > 310:
                    pygame.mixer.Sound.play(button_sound)
                    if (not level_select()):
                        pygame.mixer.music.load("Resources/Sound/Overworld.mp3")
                        pygame.mixer.music.play(-1)
                if 540 + 200 > mouse[0] and mouse[0] > 540 and 500 + 100 > mouse[1] and mouse[1] > 500:
                    pygame.mixer.Sound.play(button_sound)
                    pygame.quit()
                    sys.exit()

        screen.fill(s_blue)
        
        for cloud in clouds: cloud.draw()
        player.move(x_change, y_change)

        display_text("Fuel Run", i_red, 175, (display_width/2, display_height/4.5))
        
        mouse = pygame.mouse.get_pos()

        btn_hover = 520 + 240 > mouse[0] and mouse[0] > 520 and 310 + 120 > mouse[1] and mouse[1] > 310
        pygame.draw.rect(screen, buttonover_green*btn_hover or button_red*(not btn_hover), (520, 310, 240, 120))
        pygame.draw.polygon(screen, white, ((610, 330), (610, 410), (690, 370)))

        btn_hover = 540 + 200 > mouse[0] and mouse[0] > 540 and 500 + 100 > mouse[1] and mouse[1] > 500
        pygame.draw.rect(screen, csi_blue*btn_hover or button_red*(not btn_hover), (540, 500, 200, 100))
        display_text("Quit", a_blue, 60, (display_width/2, 555))
        
        display_text("High Score: " + str(HIGHSCORE), i_red, 45, (50, 650), False)
        
        pygame.display.update()
        clock.tick(30)

def unpause():
    global PAUSE
    PAUSE = False

def paused():
    while PAUSE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if (520 + 240 > mouse[0] and mouse[0] > 520) and (310 + 120 > mouse[1] and mouse[1] > 310):
                    pygame.mixer.Sound.play(button_sound)
                    return False
                if (540 + 200 > mouse[0] and mouse[0] > 540 and 500 + 100 > mouse[1] and mouse[1] > 500):
                    pygame.mixer.Sound.play(button_sound)
                    return True

        screen.fill(purple)
        display_text("Paused", button_yellow, 115, (display_width/2, display_height/3))
        
        mouse = pygame.mouse.get_pos()
        
        btn_hover = 520 + 240 > mouse[0] and mouse[0] > 520 and 310 + 120 > mouse[1] and mouse[1] > 310
        pygame.draw.rect(screen, buttonover_green*btn_hover or button_red*(not btn_hover), (520, 310, 240, 120))
        pygame.draw.polygon(screen, white, ((610, 330), (610, 410), (690, 370)))

        btn_hover = 540 + 200 > mouse[0] and mouse[0] > 540 and 500 + 100 > mouse[1] and mouse[1] > 500
        pygame.draw.rect(screen, csi_blue*btn_hover or button_red*(not btn_hover), (540, 500, 200, 100))
        display_text("Home", a_blue, 45, (560, 535))
        
        pygame.display.update()
        clock.tick(30)

def set_font(size):
    return pygame.font.Font("Resources/BULKYPIX.ttf", size)

def display_text(text, colour, size, pos, is_centered=True):
    font = set_font(size)
    text_surface = font.render(text, True, colour) #i_red
    disp_pos = pos
    if is_centered:
        disp_pos = text_surface.get_rect()
        disp_pos.center = (int(pos[0]), int(pos[1]))
    screen.blit(text_surface, disp_pos)

def generate_numbers(time_table):
    num1, num2 = random.randint(1, time_table), random.randint(1, time_table)
    answer = num1 * num2
    wrong1, wrong2 = answer, answer
    while (wrong1 == answer):
        wrong1 = abs(num1 + random.randint(1, 2)) * abs(num2 - random.randint(1, 2))
    while (wrong2 == answer or wrong2 == wrong1):
        wrong2 = abs(num1 + random.randint(2, 3)) * abs(num2 - random.randint(1, 2))
    return [wrong1, wrong2, num1, num2]

def reset_fuel_boxes(fuel_boxes, answer_section, numbers, fuel_speed):
    j = 0
    for i in range(len(fuel_boxes)):
        if i == answer_section:
            fuel_boxes[i].reset(numbers[-1]*numbers[-2], fuel_speed)
        else:
            fuel_boxes[i].reset(numbers[j], fuel_speed)
            j += 1
    return fuel_boxes

def game_loop(difficulty_settings):
    global PAUSE
    global HIGHSCORE
    trigger = True
    pygame.mixer.music.load("Resources/Sound/Bit Quest.mp3")
    pygame.mixer.music.play(-1)
    fuel_box_sections = [(100, 120), (300, 320), (500, 520)]
    fuel_boxes = [FuelBox(fuel_box_sections[i], 100, 35, screen) for i in range(3)]

    player.reset()
    x_change, y_change = 0, 0
    fuel_speed = -10
    score = 0
    time_table = difficulty_settings[0]
    boxspeed = difficulty_settings[1]
    points = difficulty_settings[2]
    lives = difficulty_settings[3]
    
    clouds = [Cloud(cloud_speed, 1, section[1][i], screen) for i in range(3)]
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -1
                if event.key == pygame.K_RIGHT:
                    x_change = 1
                if event.key == pygame.K_DOWN:
                    y_change = 1
                if event.key == pygame.K_UP:
                    y_change = -1
                if event.key == pygame.K_ESCAPE:
                    PAUSE = True
                    go_back = paused()
                    if(go_back):
                        return False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        screen.fill(s_blue)
        for cloud in clouds: cloud.draw()
        player.move(x_change, y_change)

        if (trigger):
            numbers = generate_numbers(time_table)
            answer_section = random.randint(0, 2)
            fuel_boxes = reset_fuel_boxes(fuel_boxes, answer_section, numbers, fuel_speed)
            trigger = False
            
        hit = -1
        for i in range(len(fuel_boxes)):
            fuel_boxes[i].draw()
            fuel_gone = fuel_boxes[i].check_bounds()
            x, y = fuel_boxes[i].x_pos, fuel_boxes[i].y_pos
            if player.hit_object((x - 110, x + 110), (y - 50, y + 100)):
                hit = i

        fuel_gone = False
        if(hit+1 or fuel_gone):
            trigger = True
            if hit == answer_section:
                score += points
                if score > HIGHSCORE: HIGHSCORE = score
                pygame.mixer.Sound.play(coll_sound)
                fuel_speed = fuel_speed*boxspeed
            else:
                pygame.mixer.Sound.play(crash_sound)
                lives -= 1
                if lives == 0:
                    pygame.mixer.Sound.play(gameover_sound)
                    return game_over(score)

        display_text("Score: " + str(score), i_red, 40, (50, 650), False)
        display_text("Highscore: " + str(HIGHSCORE), i_red, 25, (50, 600), False)
        display_text(str(lives) + " Lives", i_red, 50, (1000, 650), False)
        display_text(str(numbers[-1]) + " x " + str(numbers[-2]) + " = ?", i_red, 80, (display_width/2, 75))

        pygame.display.update()
        clock.tick(30)

main_menu()

pygame.quit()
sys.exit()
