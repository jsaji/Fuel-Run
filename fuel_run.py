import pygame
import time
import sys
import random
from parts import Cloud, Player

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

gameIcon = pygame.image.load("Resources/Images/Icon.png")
pygame.display.set_icon(gameIcon)
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

pause = False
highscore = 0

player = Player(screen, 25)

section = [[(-100, 300), (350, 650), (700, 1000)], [(5, 210), (240, 440), (460, 670)]]
cloud_speed = (-20, -10)

def LevelSelect():
    easy, medium, hard = 6, 12, 16
    easyspeed, mediumspeed, hardspeed = 1.01, 1.02, 1.03
    easyscore, mediumscore, hardscore = 10, 15, 20
    easylives, mediumlives, hardlives = 5, 4, 3
    #easy = {6, 1.01, 5, 3}
    #medium = {12, 1.02, 10, 4}
    #hard = {16, 1.03, 15, 5}

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
                        keep_going = game_loop(easy, easyspeed, easyscore, easylives)
                    return False
                elif 515 + 250 > mouse[0] and mouse[0] > 515 and 400 + 80 > mouse[1] and mouse[1] > 400:
                    pygame.mixer.Sound.play(button_sound)
                    while (keep_going):
                        keep_going = game_loop(medium, mediumspeed, mediumscore, mediumlives)
                    return False
                elif 515 + 250 > mouse[0] and mouse[0] > 515 and 550 + 80 > mouse[1] and mouse[1] > 550:
                    pygame.mixer.Sound.play(button_sound)
                    while (keep_going):
                        keep_going = game_loop(hard, hardspeed, hardscore, hardlives)
                    return False
                
        screen.fill(s_blue)
        
        for cloud in clouds: cloud.update()

        diff_button_size = 40
        display_text("Choose difficulty:", i_red, 50, (display_width/2, display_height/4.5))
        
        mouse = pygame.mouse.get_pos()
        keep_going = True

        if 40 + 160 > mouse[0] and mouse[0] > 40 and 40 + 60 > mouse[1] and mouse[1] > 40:
            pygame.draw.rect(screen, csi_blue, (40, 40, 160, 60))
        else:
            pygame.draw.rect(screen, button_red, (40, 40, 160, 60))
        display_text("Home", a_blue, 30, (65, 60), False)
        
        if 515 + 250 > mouse[0] and mouse[0] > 515 and 250 + 80 > mouse[1] and mouse[1] > 250:
            pygame.draw.rect(screen, buttonover_green, (515, 250, 250, 80))
        else:
            pygame.draw.rect(screen, button_green, (515, 250, 250, 80))
        display_text("Easy", a_blue, diff_button_size, (display_width/2, 290))

        if 515 + 250 > mouse[0] and mouse[0] > 515 and 400 + 80 > mouse[1] and mouse[1] > 400:
            pygame.draw.rect(screen, buttonover_yellow, (515, 400, 250, 80))
        else:
            pygame.draw.rect(screen, button_yellow, (515, 400, 250, 80))
        display_text("Medium", a_blue, diff_button_size, (display_width/2, 440))
        
        if 515 + 250 > mouse[0] and mouse[0] > 515 and 550 + 80 > mouse[1] and mouse[1] > 550:
            pygame.draw.rect(screen, buttonover_red, (515, 550, 250, 80))
        else:
            pygame.draw.rect(screen, button_red, (515, 550, 250, 80))
        display_text("Hard", a_blue, diff_button_size, (display_width/2, 590))
            
        pygame.display.update()
        clock.tick(30)
            
def GameOver(score):
    global highscore
    pygame.mixer.Sound.play(gameover_sound)
    
    clouds = [Cloud(cloud_speed, 0, section[0][i], screen) for i in range(3)]
    scorefont = set_font(70)
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

        for cloud in clouds: cloud.update()

        if highscore > score:
            highscore = score
            display_text("New Highscore: "+str(highscore)+"!", i_red, 70, (display_width/2, display_height/4.5))
        else:
            display_text("Score: "+str(score)+"!", i_red, 70, (display_width/2, display_height/4.5))
        
        mouse = pygame.mouse.get_pos()

        if 520 + 240 > mouse[0] and mouse[0] > 520 and 310 + 120 > mouse[1] and mouse[1] > 310:
            pygame.draw.rect(screen, buttonover_green, (520, 310, 240, 120))
        else:
            pygame.draw.rect(screen, button_red, (520, 310, 240, 120))
        pygame.draw.polygon(screen, white, ((610, 330), (610, 410), (690, 370)))

        if 540 + 200 > mouse[0] and mouse[0] > 540 and 500 + 100 > mouse[1] and mouse[1] > 500:
            pygame.draw.rect(screen, csi_blue, (540, 500, 200, 100))
        else:
            pygame.draw.rect(screen, button_red, (540, 500, 200, 100))

        display_text("Home", a_blue, 45, (display_width/2, 555))
        #player.rotate(rotation)

        pygame.display.update()
        clock.tick(30)

def MainMenu():
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
                    if (not LevelSelect()):
                        pygame.mixer.music.load("Resources/Sound/Overworld.mp3")
                        pygame.mixer.music.play(-1)
                if 540 + 200 > mouse[0] and mouse[0] > 540 and 500 + 100 > mouse[1] and mouse[1] > 500:
                    pygame.mixer.Sound.play(button_sound)
                    pygame.quit()
                    sys.exit()

        screen.fill(s_blue)
        
        for cloud in clouds: cloud.update()
        player.move(x_change, y_change)

        display_text("Fuel Run", i_red, 175, (display_width/2, display_height/4.5))
        
        mouse = pygame.mouse.get_pos()
        if 520 + 240 > mouse[0] and mouse[0] > 520 and 310 + 120 > mouse[1] and mouse[1] > 310:
            pygame.draw.rect(screen, buttonover_green, (520, 310, 240, 120))
        else:
            pygame.draw.rect(screen, button_red, (520, 310, 240, 120))
        pygame.draw.polygon(screen, white, ((610, 330), (610, 410), (690, 370)))

        if 540 + 200 > mouse[0] and mouse[0] > 540 and 500 + 100 > mouse[1] and mouse[1] > 500:
            pygame.draw.rect(screen, csi_blue, (540, 500, 200, 100))
        else:
            pygame.draw.rect(screen, button_red, (540, 500, 200, 100))
        display_text("Quit", a_blue, 60, (display_width/2, 555))
        
        display_text("High Score: " + str(highscore), i_red, 45, (50, 650), False)
        
        pygame.display.update()
        clock.tick(30)

def unpause():
    global pause
    pause = False

def paused():
    while pause:
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
        
        if (520 + 240 > mouse[0] and mouse[0] > 520) and (310 + 120 > mouse[1] and mouse[1] > 310):
            pygame.draw.rect(screen, buttonover_green, (520, 310, 240, 120))
        else:
            pygame.draw.rect(screen, button_red, (520, 310, 240, 120))
        pygame.draw.polygon(screen, white, ((610, 330), (610, 410), (690, 370)))

        if 540 + 200 > mouse[0] and mouse[0] > 540 and 500 + 100 > mouse[1] and mouse[1] > 500:
            pygame.draw.rect(screen, csi_blue, (540, 500, 200, 100))
        else:
            pygame.draw.rect(screen, button_red, (540, 500, 200, 100))
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
        disp_pos= text_surface.get_rect()
        disp_pos.center = (int(pos[0]), int(pos[1]))
    screen.blit(text_surface, disp_pos)

def generateNumbers(difficulty):
    num1, num2 = random.randint(1, difficulty), random.randint(1, difficulty)
    answer = num1 * num2
    wrong1, wrong2 = answer, answer
    while (wrong1 == answer):
        wrong1 = abs(num1 + random.randint(1, 2)) * abs(num2 - random.randint(1, 2))
    while (wrong2 == answer or wrong2 == wrong1):
        wrong2 = abs(num1 + random.randint(2, 3)) * abs(num2 - random.randint(1, 2))
    return num1, num2, wrong1, wrong2

def fuelBox(number, fuel_startx, fuel_starty, color):
    pygame.draw.rect(screen, color, [int(fuel_startx), int(fuel_starty), 100, 100])
    display_text(str(number), a_blue, 35, (fuel_startx + 55, fuel_starty + 55))

def game_loop(difficulty, boxspeed, scorepoints, lifesum):
    global highscore
    global pause
    trigger = True
    pygame.mixer.music.load("Resources/Sound/Bit Quest.mp3")
    pygame.mixer.music.play(-1)

    player.reset()
    x_change, y_change = 0, 0
    fuel_speed = -10
    score = 0
    clouds = [Cloud(cloud_speed, 1, section[1][i], screen) for i in range(3)]
    game_exit = False
    lives = lifesum

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
                    pause = True
                    escapeToMenu = paused()
                    if(escapeToMenu):
                        return False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        screen.fill(s_blue)
        for cloud in clouds: cloud.update()
        player.move(x_change, y_change)

        if (trigger):
            fuel_startx1, fuel_startx2, fuel_startx3 = random.randint(1300, 1350), random.randint(1300, 1350), random.randint(1300, 1350)
            fuel_starty1, fuel_starty2, fuel_starty3 = random.randint(100, 120), random.randint(300, 320), random.randint(500, 520)
            answer_num1, answer_num2, wrong1, wrong2 = generateNumbers(difficulty)
            AnswerQuad = random.randint(0, 2)
            trigger = False

        if AnswerQuad == 0:
            topBox = fuelBox(answer_num1*answer_num2, fuel_startx1, fuel_starty1, purple)
            midBox = fuelBox(wrong1, fuel_startx2, fuel_starty2, purple)
            botBox = fuelBox(wrong2, fuel_startx3, fuel_starty3, purple)
        elif AnswerQuad == 1:
            midBox = fuelBox(answer_num1*answer_num2, fuel_startx2, fuel_starty2, purple)
            topBox = fuelBox(wrong1, fuel_startx1, fuel_starty1, purple)
            botBox = fuelBox(wrong2, fuel_startx3, fuel_starty3, purple)
        elif AnswerQuad == 2:
            botBox = fuelBox(answer_num1*answer_num2, fuel_startx3, fuel_starty3, purple)
            midBox = fuelBox(wrong1, fuel_startx2, fuel_starty2, purple)
            topBox = fuelBox(wrong2, fuel_startx1, fuel_starty1, purple)

        fuel_startx1 += fuel_speed
        fuel_startx2 += fuel_speed
        fuel_startx3 += fuel_speed

        if player.hit_object((fuel_startx1 - 110, fuel_startx1 + 110), (fuel_starty1 - 50, fuel_starty1 + 100)):
            hit = 0
        elif player.hit_object((fuel_startx2 - 110, fuel_startx2 + 110), (fuel_starty2 - 50, fuel_starty2 + 100)):
            hit = 1
        elif player.hit_object((fuel_startx3 - 110, fuel_startx3 + 110), (fuel_starty3 - 50, fuel_starty3 + 100)):
            hit = 2
        else:
            hit = -1

        fuelGone = (fuel_startx1 + fuel_startx2 + fuel_startx3 < -600)
        if(hit+1 or fuelGone):
            trigger = True
            if(hit == AnswerQuad):
                score += scorepoints
                if score > highscore:
                    highscore = score
                pygame.mixer.Sound.play(coll_sound)
                fuel_speed = fuel_speed*boxspeed
            else:
                pygame.mixer.Sound.play(crash_sound)
                lives -= 1
                hit = -1
                if lives == 0:
                    pygame.mixer.Sound.play(gameover_sound)
                    return GameOver(score)

        display_text("Score: " + str(score), i_red, 40, (50, 650), False)
        display_text("Highscore: " + str(highscore), i_red, 25, (50, 600), False)
        display_text(str(lives) + " Lives", i_red, 50, (1000, 650), False)
        display_text(str(answer_num1) + " x " + str(answer_num2) + " = ?", i_red, 80, (display_width/2, 75))

        pygame.display.update()
        clock.tick(30)

MainMenu()

pygame.quit()
sys.exit()
