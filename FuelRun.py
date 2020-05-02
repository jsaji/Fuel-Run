import pygame, time, sys, random

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

gameIcon = pygame.image.load("Resources/Images/Icon.png")
pygame.display.set_icon(gameIcon)
display_width, display_height = 1280, 720
screen = pygame.display.set_mode((display_width,display_height), 0, 32)
pygame.display.set_caption("Fuel Run")
clock = pygame.time.Clock()

c_blue = (31,117,254)
csi_blue = (40,110,225)
a_blue = (240, 248, 255)
s_blue = (63, 157, 255)
i_red = (237,41,57)
purple = 	(160, 32, 240)
black, white = (0,0,0), (255,255,255)

button_green, buttonover_green = (70, 205, 60), (11, 230, 81)
button_red, buttonover_red = (200,40,50), (255,40,50)
button_orange, buttonover_orange = (255, 125, 24), (255, 159, 24)
button_yellow, buttonover_yellow = (255, 200, 0), (253, 230, 0)

crash_sound = pygame.mixer.Sound("Resources/Sound/WrongAnswer.wav")
coll_sound = pygame.mixer.Sound("Resources/Sound/RightAnswer.wav")
button_sound = pygame.mixer.Sound("Resources/Sound/ButtonPress.wav")
gameover_sound = pygame.mixer.Sound("Resources/Sound/GameOver.wav")

pause = False
lvldiff, highscore = 0, 0

pointerChoice = ["Resources/Images/BluePlane.png", "Resources/Images/GreenPlane.png", "Resources/Images/MonoPlane.png", "Resources/Images/PinkPlane.png", "Resources/Images/RedPlane.png", "Resources/Images/RetroPlane.png", "Resources/Images/TechPlane.png", "Resources/Images/PurplePlane.png", ]
pointerSelect = random.randint(0, 7)
pointer = pygame.image.load(pointerChoice[pointerSelect])

pause = False

##def LoadMedium():
##    medium = 8
##    mediumspeed = 1.02
##    mediumscore = 10
##    mediumlives = 4
##    game_loop(medium, mediumspeed, mediumscore, mediumlives)

def LevelSelect():
    global lvldiff
    
    x_change, y_change = 0, 0
    easy, medium, hard = 6, 12, 16
    easyspeed, mediumspeed, hardspeed = 1.01, 1.02, 1.03
    easyscore, mediumscore, hardscore = 5, 10, 15
    easylives, mediumlives, hardlives = 3, 4, 5
    
    cloud_startx1, cloud_startx2, cloud_startx3 = random.randint(1290, 1345), random.randint(1290, 1345), random.randint(1290, 1345)
    cloud_starty1, cloud_starty2, cloud_starty3 = random.randrange(5, 210), random.randrange(240, 440), random.randrange(470, 670)
    cloud_speed1, cloud_speed2, cloud_speed3 = random.randrange(-15, -10), random.randrange(-15, -10), random.randrange(-15, -10)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -15
                if event.key == pygame.K_RIGHT:
                    x_change = 15
                if event.key == pygame.K_DOWN:
                    y_change = 15
                if event.key == pygame.K_UP:
                    y_change = -15
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    y_change = 0
                
        screen.fill(s_blue)
        
        CloudTop(cloud_startx1, cloud_starty1)
        cloud_startx1 += cloud_speed1
        CloudMid(cloud_startx2, cloud_starty2)
        cloud_startx2 += cloud_speed2
        CloudBot(cloud_startx3, cloud_starty3)
        cloud_startx3 += cloud_speed3

        if cloud_startx1 < -400:
            cloud_startx1, cloud_starty1, cloud_speed1 = random.randint (1290, 1345), random.randint(5, 210), random.randint(-15, -10)
            CloudTop(cloud_startx1, cloud_starty1)
        if cloud_startx2 < -400:
            cloud_startx2, cloud_starty2, cloud_speed2 = random.randrange (1290, 1345), random.randrange(240, 440), random.randrange(-15, -10)
            CloudMid(cloud_startx2, cloud_starty2)
        if cloud_startx3 < -400:
            cloud_startx3, cloud_starty3, cloud_speed3 = random.randrange (1290, 1345), random.randrange(470, 670), random.randrange(-15, -10)
            CloudBot(cloud_startx3, cloud_starty3)

        buttontext = pygame.font.Font("Resources/BULKYPIX.ttf", 40)
        diffchoose = pygame.font.Font("Resources/BULKYPIX.ttf", 50)
        DiffTextSurf, DiffTextRect = text_objects("Choose difficulty:", diffchoose)
        DiffTextRect.center = ((display_width/2),(display_height/4.5))
        screen.blit(DiffTextSurf, DiffTextRect)
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if 515 + 250 > mouse[0] > 515 and 250 + 80 > mouse[1] > 250:
            pygame.draw.rect(screen, buttonover_green, (515, 250, 250, 80))
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                lvldiff = 0
                game_loop(easy, easyspeed, easyscore, easylives)
        else:
            pygame.draw.rect(screen, button_green,  (515, 250, 250, 80))
        EasyTextSurf, EasyTextRect = levelselect_text("Easy", buttontext)
        EasyTextRect.center = ((display_width/2), 290)
        screen.blit(EasyTextSurf, EasyTextRect)

        if 40 + 160 > mouse[0] > 40 and 40 + 60 > mouse[1] > 40:
            pygame.draw.rect(screen, csi_blue, (40, 40, 160, 60))
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                MainMenu()
        else:
            pygame.draw.rect(screen, button_red, (40, 40, 160, 60))
        hometext = pygame.font.Font("Resources/BULKYPIX.ttf", 30)
        Homebutton = hometext.render("Home", True, a_blue)
        screen.blit(Homebutton, (65, 60))
        
        if 515 + 250 > mouse[0] > 515 and 400 + 80 > mouse[1] > 400:
            pygame.draw.rect(screen, buttonover_yellow,  (515, 400, 250, 80))
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                lvldiff = 1
##                LoadMedium()
                game_loop(medium, mediumspeed, mediumscore, mediumlives)
        else:
            pygame.draw.rect(screen, button_yellow,  (515, 400, 250, 80))
        MediumTextSurf, MediumTextRect = levelselect_text("Medium", buttontext)
        MediumTextRect.center = ((display_width/2), 440)
        screen.blit(MediumTextSurf, MediumTextRect)
        
        if 515 + 250 > mouse[0] > 515 and 550 + 80 > mouse[1] > 550:
            pygame.draw.rect(screen, buttonover_red,  (515, 550, 250, 80))
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                lvldiff = 2
                game_loop(hard, hardspeed, hardscore, hardlives)
        else:
            pygame.draw.rect(screen, button_red,  (515, 550, 250, 80))
        HardTextSurf, HardTextRect = levelselect_text("Hard", buttontext)
        HardTextRect.center = ((display_width/2), 590)
        screen.blit(HardTextSurf, HardTextRect)
            
        pygame.display.update()
        clock.tick(60)
        
        
def GameOver(score):
    global highscore
    global lvldiff
    pygame.mixer.Sound.play(gameover_sound)
    
    easy, medium, hard, extreme = 4, 8, 12, 16
    easyspeed, mediumspeed, hardspeed, extremespeed = 1.01, 1.02, 1.03, 1.04
    easyscore, mediumscore, hardscore, extremescore = 5, 10, 15, 20
    easylives, mediumlives, hardlives, extremelives = 3, 4, 5, 6
    
    cloud_startx1, cloud_startx2, cloud_startx3 = random.randint (-100, 300), random.randint (350, 650), random.randint (700, 1000)
    cloud_starty1, cloud_starty2, cloud_starty3 = random.randint(750, 800), random.randint(750, 800), random.randint(750, 800)
    cloud_speed1, cloud_speed2, cloud_speed3 = random.randint(-20, -15), random.randint(-20, -15), random.randint(-20, -15)
    
    scorefont = pygame.font.Font("Resources/BULKYPIX.ttf", 70)
    x, y = 100, 360
    rotation = 10
    rotate = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.fill(s_blue)
        
        CloudTop(cloud_startx1, cloud_starty1)
        cloud_starty1 += cloud_speed1
        CloudMid(cloud_startx2, cloud_starty2)
        cloud_starty2 += cloud_speed2
        CloudBot(cloud_startx3, cloud_starty3)
        cloud_starty3 += cloud_speed3

        if cloud_starty1 < -100:
            cloud_startx1, cloud_starty1, cloud_speed1 = random.randint (-100, 300), random.randint(750, 800), random.randint(-20, -15)
            CloudTop(cloud_startx1, cloud_starty1)
        if cloud_starty2 < -100:
            cloud_startx2, cloud_starty2, cloud_speed2 = random.randint (350, 650), random.randint(750, 800), random.randint(-20, -15)
            CloudMid(cloud_startx2, cloud_starty2)
        if cloud_starty3 < -100:
            cloud_startx3, cloud_starty3, cloud_speed3 = random.randint (700, 1000), random.randint(750, 800), random.randint(-20, -15)
            CloudBot(cloud_startx3, cloud_starty3)
        
        if highscore <= score:
            highscore = score
            HighScoreTextSurf, HighScoreTextRect = text_objects("New Highscore: "+str(highscore)+"!", scorefont)
            HighScoreTextRect.center = ((display_width/2),(display_height/4.5))
            screen.blit(HighScoreTextSurf, HighScoreTextRect)
        else:
            ScoreTextSurf, ScoreTextRect = text_objects("Score: "+str(score)+"!", scorefont)
            ScoreTextRect.center = ((display_width/2),(display_height/4.5))
            screen.blit(ScoreTextSurf, ScoreTextRect)
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 520 + 240 > mouse[0] > 520 and 310 + 120 > mouse[1] > 310:
            pygame.draw.rect(screen, buttonover_green, (520, 310, 240, 120))
            pygame.draw.polygon(screen, white, ((610,330), (610, 410), (690,370)))
            if click[0] == 1:
                if lvldiff == 0:
                    pygame.mixer.Sound.play(button_sound)
                    game_loop(easy, easyspeed, easyscore, easylives)
                elif lvldiff == 1:
                    game_loop(medium, mediumspeed, mediumscore, mediumlives)
                elif lvldiff == 2:
                    game_loop(hard, hardspeed, hardscore, hardlives)
                elif lvldiff == 3:
                    game_loop(extreme, extremespeed, extremescore, extremelives)
        else:
            pygame.draw.rect(screen, button_red, (520, 310, 240, 120))
            pygame.draw.polygon(screen, white, ((610,330), (610, 410), (690,370)))


        if 540 + 200 > mouse[0] > 540 and 500 + 100 > mouse[1] > 500:
            pygame.draw.rect(screen, csi_blue, (540, 500, 200, 100))
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                MainMenu()
##                pygame.mixer.Sound.play(button_sound)
##                pygame.quit()
##                quit()
        else:
            pygame.draw.rect(screen, button_red, (540, 500, 200, 100))
        quittext = pygame.font.Font("Resources/BULKYPIX.ttf", 45)
        Quitbutton = quittext.render("Home", True, a_blue)
        screen.blit(Quitbutton, (560, 535))
        

        
        rotate += rotation
        planedown = pygame.transform.rotate(pointer, rotate)
        screen.blit(planedown, (300, 360))
        pygame.display.update()
        clock.tick(60)

def MainMenu():
    Menu = True
    pygame.mixer.music.load("Resources/Sound/Overworld.mp3")
    pygame.mixer.music.play(-1)
    
    x_change, y_change = 0, 0
    
    cloud_startx1, cloud_startx2, cloud_startx3 = random.randint(1290, 1345), random.randint(1290, 1345), random.randint(1290, 1345)
    cloud_starty1, cloud_starty2, cloud_starty3 = random.randrange(5, 210), random.randrange(240, 440), random.randrange(470, 670)
    cloud_speed1, cloud_speed2, cloud_speed3 = random.randrange(-15, -10), random.randrange(-15, -10), random.randrange(-15, -10)
    
    x, y = 125, 333
    
    while Menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -25
                if event.key == pygame.K_RIGHT:
                    x_change = 25
                if event.key == pygame.K_DOWN:
                    y_change = 25
                if event.key == pygame.K_UP:
                    y_change = -25
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    y_change = 0

        x += x_change
        y += y_change
        screen.fill(s_blue)

        if x > display_width:
            x = -120
        elif x < -120:                                               
            x = display_width
        if y > display_height:
            y = -55
        elif y < -55:                                               
            y = display_height

        CloudTop(cloud_startx1, cloud_starty1)
        cloud_startx1 += cloud_speed1
        CloudMid(cloud_startx2, cloud_starty2)
        cloud_startx2 += cloud_speed2
        CloudBot(cloud_startx3, cloud_starty3)
        cloud_startx3 += cloud_speed3

        if cloud_startx1 < -400:
            cloud_startx1, cloud_starty1, cloud_speed1 = random.randint (1290, 1345), random.randint(5, 210), random.randint(-15, -10)
            CloudTop(cloud_startx1, cloud_starty1)
        if cloud_startx2 < -400:
            cloud_startx2, cloud_starty2, cloud_speed2 = random.randrange (1290, 1345), random.randrange(240, 440), random.randrange(-15, -10)
            CloudMid(cloud_startx2, cloud_starty2)
        if cloud_startx3 < -400:
            cloud_startx3, cloud_starty3, cloud_speed3 = random.randrange (1290, 1345), random.randrange(470, 670), random.randrange(-15, -10)
            CloudBot(cloud_startx3, cloud_starty3)

        message = pygame.font.Font("Resources/BULKYPIX.ttf", 175)
        TextSurf, TextRect = text_objects("Fuel Run", message)
        TextRect.center = ((display_width/2),(display_height/4.5))
        screen.blit(TextSurf, TextRect)
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 520 + 240 > mouse[0] > 520 and 310 + 120 > mouse[1] > 310:
            pygame.draw.rect(screen, buttonover_green, (520, 310, 240, 120))
            pygame.draw.polygon(screen, white, ((610,330), (610, 410), (690,370)))
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                LevelSelect()
        else:
            pygame.draw.rect(screen, button_red, (520, 310, 240, 120))
            pygame.draw.polygon(screen, white, ((610,330), (610, 410), (690,370)))

##        if 540 + 200 > mouse[0] > 540 and 500 + 100 > mouse[1] > 500:
##            pygame.draw.rect(screen, csi_blue, (540, 500, 200, 100))
##            if click[0] == 1:
##                pygame.mixer.Sound.play(button_sound)
##                pygame.quit()
##                quit()
##        else:
##            pygame.draw.rect(screen, button_red, (540, 500, 200, 100))
##        exittext = pygame.font.Font("BULKYPIX.ttf", 60)
##        QuitButton = exittext.render("Quit", True, a_blue)    
##        screen.blit(QuitButton, (560, 525))
        
        MainHighScoreDisplay(highscore)
        plane(x,y)
        
        pygame.display.update()
        clock.tick(60)
        
def unpause():
    global pause
    pause = False

def paused():
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(purple)
        message = pygame.font.Font("Resources/BULKYPIX.ttf", 115)
        TextSurf, TextRect = paused_text("Paused", message)
        TextRect.center = ((display_width/2),(display_height/3))
        screen.blit(TextSurf, TextRect)
        
        mouse = pygame.mouse.get_pos() 
        click = pygame.mouse.get_pressed()
        
        if 520 + 240 > mouse[0] > 520 and 310 + 120 > mouse[1] > 310:
            pygame.draw.rect(screen, buttonover_green, (520, 310, 240, 120))
            pygame.draw.polygon(screen, white, ((610,330), (610, 410), (690,370)))
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                unpause()
        else:
            pygame.draw.rect(screen, button_red, (520, 310, 240, 120))
            pygame.draw.polygon(screen, white, ((610,330), (610, 410), (690,370)))

        if 540 + 200 > mouse[0] > 540 and 500 + 100 > mouse[1] > 500:
            pygame.draw.rect(screen, csi_blue, (540, 500, 200, 100))
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                MainMenu()
        else:
            pygame.draw.rect(screen, button_red, (540, 500, 200, 100))
        buttontext = pygame.font.Font("Resources/BULKYPIX.ttf", 45)
        Quitbutton = buttontext.render("Home", True, a_blue)
        screen.blit(Quitbutton, (560, 535))
        
        pygame.display.update()
        clock.tick(60)
        
def text_objects(text, font):
    textSurface = font.render(text, True, i_red)
    return textSurface, textSurface.get_rect()
def paused_text(text, font):
    textSurface = font.render(text, True, button_yellow)
    return textSurface, textSurface.get_rect()
def levelselect_text(text, font):
    textSurface = font.render(text, True, a_blue)
    return textSurface, textSurface.get_rect()
def box_text(text, font):
    textSurface = font.render(text, True, a_blue)
    return textSurface, textSurface.get_rect()

def ScoreDisplay(score):
    scorefont = pygame.font.Font("Resources/BULKYPIX.ttf", 40)
    ScoreCount = scorefont.render("Score: " + str(score), True, i_red)
    screen.blit(ScoreCount, (50, 650))
def HighScoreDisplay(highscore):
    highscorefont = pygame.font.Font("Resources/BULKYPIX.ttf", 25)
    HighScoreCount = highscorefont.render("High Score: " + str(highscore), True, i_red)
    screen.blit(HighScoreCount, (50, 600))
def MainHighScoreDisplay(highscore):
    highscorefont = pygame.font.Font("Resources/BULKYPIX.ttf", 45)
    HighScoreCount = highscorefont.render("High Score: " + str(highscore), True, i_red)
    screen.blit(HighScoreCount, (50, 650))
def LivesDisplay(lives):
    lifefont = pygame.font.Font("Resources/BULKYPIX.ttf", 50)
    LifeCount = lifefont.render(str(lives)+" Lives", True, i_red)
    screen.blit(LifeCount, (1000, 650))

def Question(number1, number2):
    ingame = pygame.font.Font("Resources/BULKYPIX.ttf", 80)
    Line = ingame.render(str(number1)+" x "+str(number2)+" = ?", True, i_red)
    screen.blit(Line, (400, 50))
def Answer(number1, number2, fuel_startx, fuel_starty):
    boxtext = pygame.font.Font("Resources/BULKYPIX.ttf", 35)
    answer = number1*number2
    TextSurf, TextRect = box_text(str(answer), boxtext)
    TextRect.center = ((fuel_startx + 55),(fuel_starty + 55))
    screen.blit(TextSurf, TextRect)
def GenWrong1(RandNumber1, RandNumber2, RandNumber3, RandNumber4, fuel_startx, fuel_starty, number1, number2):
    boxtext = pygame.font.Font("Resources/BULKYPIX.ttf", 35)
    WrongAnswer1 = RandNumber1*RandNumber2
    TextSurf, TextRect = box_text(str(WrongAnswer1), boxtext)
    TextRect.center = ((fuel_startx + 55),(fuel_starty + 55))
    screen.blit(TextSurf, TextRect)
def GenWrong2(RandNumber1, RandNumber2, RandNumber3, RandNumber4, fuel_startx, fuel_starty, number1, number2):
    boxtext = pygame.font.Font("Resources/BULKYPIX.ttf",35)
    WrongAnswer2 = RandNumber3*RandNumber4
    TextSurf, TextRect = box_text(str(WrongAnswer2), boxtext)
    TextRect.center = ((fuel_startx + 55),(fuel_starty + 55))
    screen.blit(TextSurf, TextRect)

def FuelBoxTop(fuelx, fuely, color):
    pygame.draw.rect(screen, color, [fuelx, fuely, 100, 100])
def FuelBoxMid(fuelx, fuely, color):
    pygame.draw.rect(screen, color, [fuelx, fuely, 100, 100])
def FuelBoxBot(fuelx, fuely, color):
    pygame.draw.rect(screen, color, [fuelx, fuely, 100, 100])

def CloudTop(cloud_x, cloud_y):
    cloud = pygame.image.load("Resources/Images/Cloud.png")
    screen.blit(cloud, (cloud_x, cloud_y))
def CloudMid(cloud_x, cloud_y):
    cloud = pygame.image.load("Resources/Images/Cloud.png")
    screen.blit(cloud, (cloud_x, cloud_y))
def CloudBot(cloud_x, cloud_y):
    cloud = pygame.image.load("Resources/Images/Cloud.png")
    screen.blit(cloud, (cloud_x, cloud_y))

def plane(x,y):
    screen.blit(pointer,(x,y))

def game_loop(difficulty, boxspeed, scorepoints, lifesum):
    global highscore
    global pause
    
    pygame.mixer.music.load("Resources/Sound/Bit Quest.mp3")
    pygame.mixer.music.play(-1)
    x, y = 75, 333
    x_change, y_change = 0, 0
    
    fuel_speed = -5    
    score = 0
    
    if score == 0:
        fuel_startx1, fuel_startx2, fuel_startx3 = random.randint(1300, 1350), random.randint(1300, 1350), random.randint(1300, 1350)
        fuel_starty1, fuel_starty2, fuel_starty3 = random.randint(100, 120), random.randint(300, 320), random.randint(500, 520)
        
        cloud_startx1, cloud_startx2, cloud_startx3 = random.randint(1290, 1345), random.randint(1290, 1345), random.randint(1290, 1345)
        cloud_starty1, cloud_starty2, cloud_starty3 = random.randrange(5, 210), random.randrange(240, 440), random.randrange(470, 670)
        cloud_speed1, cloud_speed2, cloud_speed3 = random.randrange(-15, -10), random.randrange(-15, -10), random.randrange(-15, -10)
    
        AnswerQuad = random.randint(0, 2)

        number1, number2 = random.randint(1, difficulty), random.randint(1, difficulty)
        deduceFactor1, deduceFactor2, deduceFactor3, deduceFactor4 = random.randint(0, 1), random.randint(1, 2), random.randint(2, 3), random.randint(1, 2)
        RandNumber1, RandNumber2, RandNumber3, RandNumber4 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2), abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)

        if RandNumber1*RandNumber2 == number1*number2:
            deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
            RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
            if RandNumber1*RandNumber2 == number1*number2:
                deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
        if RandNumber3*RandNumber4 == number1*number2:
            deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
            RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
            if RandNumber3*RandNumber4 == number1*number2:
                deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
            
    gameExit = False

    lives = lifesum
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -30
                if event.key == pygame.K_RIGHT:
                    x_change = 30
                if event.key == pygame.K_DOWN:
                    y_change = 30
                if event.key == pygame.K_UP:
                    y_change = -30
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        x += x_change
        y += y_change
        screen.fill(s_blue)

        if x > display_width:
            pygame.mixer.Sound.play(crash_sound)
            x, y = 100, 333
            lives += -1
            if lives == 0:
                pygame.mixer.Sound.play(gameover_sound)
                GameOver(score)
            continue
        elif x < -120:                    
            pygame.mixer.Sound.play(crash_sound)
            x, y = 100, 333
            lives += -1
            if lives == 0:
                pygame.mixer.Sound.play(gameover_sound)
                GameOver(score)
            continue
        if y > display_height:
            pygame.mixer.Sound.play(crash_sound)
            x, y = 100, 333
            lives += -1
            if lives == 0:
                pygame.mixer.Sound.play(gameover_sound)
                GameOver(score)
            continue
        elif y < -55:                   
            pygame.mixer.Sound.play(crash_sound)
            x, y = 100, 333
            lives += -1
            if lives == 0:
                pygame.mixer.Sound.play(gameover_sound)
                GameOver(score)
            continue

        CloudTop(cloud_startx1, cloud_starty1)
        cloud_startx1 += cloud_speed1
        CloudMid(cloud_startx2, cloud_starty2)
        cloud_startx2 += cloud_speed2
        CloudBot(cloud_startx3, cloud_starty3)
        cloud_startx3 += cloud_speed3

        if cloud_startx1 < -400:
            cloud_startx1, cloud_starty1, cloud_speed1 = random.randint (1290, 1345), random.randint(5, 210), random.randint(-15, -10)
            CloudTop(cloud_startx1, cloud_starty1)
        if cloud_startx2 < -400:
            cloud_startx2, cloud_starty2, cloud_speed2 = random.randrange (1290, 1345), random.randrange(240, 440), random.randrange(-15, -10)
            CloudMid(cloud_startx2, cloud_starty2)
        if cloud_startx3 < -400:
            cloud_startx3, cloud_starty3, cloud_speed3 = random.randrange (1290, 1345), random.randrange(470, 670), random.randrange(-15, -10)
            CloudBot(cloud_startx3, cloud_starty3)

        FuelBoxTop(fuel_startx1, fuel_starty1, purple)
        fuel_startx1 += fuel_speed
        FuelBoxMid(fuel_startx2, fuel_starty2, purple)
        fuel_startx2 += fuel_speed
        FuelBoxBot(fuel_startx3, fuel_starty3, purple)
        fuel_startx3 += fuel_speed
        
        if (fuel_startx1 + fuel_startx2 + fuel_startx3) < -600:
            lives += -1
            pygame.mixer.Sound.play(crash_sound)
            if lives == 0:
                pygame.mixer.Sound.play(gameover_sound)
                GameOver(score)
                
            fuel_startx1, fuel_startx2, fuel_startx3 = random.randint(1300, 1350), random.randint(1300, 1350), random.randint(1300, 1350)
            fuel_starty1, fuel_starty2, fuel_starty3 = random.randint(100, 120), random.randint(300, 320), random.randint(500, 520)
            
            number1, number2 = random.randint(1, difficulty), random.randint(1, difficulty)
            deduceFactor1, deduceFactor2, deduceFactor3, deduceFactor4 = random.randint(0, 1), random.randint(1, 2), random.randint(2, 3), random.randint(1, 2)
            RandNumber1, RandNumber2, RandNumber3, RandNumber4 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2), abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
            
            if RandNumber1*RandNumber2 == number1*number2:
                deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                if RandNumber1*RandNumber2 == number1*number2:
                    deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                    RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
            if RandNumber3*RandNumber4 == number1*number2:
                deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                if RandNumber3*RandNumber4 == number1*number2:
                    deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                    RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                
            AnswerQuad = random.randint(0, 2)
            continue

           
        if AnswerQuad == 0:
            Answer(number1, number2, fuel_startx1, fuel_starty1)
            GenWrong1(RandNumber1, RandNumber2, RandNumber3, RandNumber4, fuel_startx2, fuel_starty2, number1, number2)
            GenWrong2(RandNumber1, RandNumber2, RandNumber3, RandNumber4, fuel_startx3, fuel_starty3, number1, number2)
            if fuel_startx1 <= x <= (fuel_startx1 + 100) or fuel_startx1 < x + 110 < fuel_startx1 + 100:
                if fuel_starty1 <= y <= (fuel_starty1 + 100) or fuel_starty1 <= y + 50 <= fuel_starty1 + 100:
                    score += scorepoints
                    if score >= highscore:
                        highscore = score
                    pygame.mixer.Sound.play(coll_sound)
                    fuel_startx1, fuel_startx2, fuel_startx3 = random.randint(1300, 1350), random.randint(1300, 1350), random.randint(1300, 1350)
                    fuel_starty1, fuel_starty2, fuel_starty3 = random.randint(100, 120), random.randint(300, 320), random.randint(500, 520)
            
                    number1, number2 = random.randint(1, difficulty), random.randint(1, difficulty)
                    deduceFactor1, deduceFactor2, deduceFactor3, deduceFactor4 = random.randint(0, 1), random.randint(1, 2), random.randint(2, 3), random.randint(1, 2)
                    RandNumber1, RandNumber2, RandNumber3, RandNumber4 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2), abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)

                    if RandNumber1*RandNumber2 == number1*number2:
                        deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                        RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                        if RandNumber1*RandNumber2 == number1*number2:
                            deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                            RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                    if RandNumber3*RandNumber4 == number1*number2:
                        deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                        RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                        if RandNumber3*RandNumber4 == number1*number2:
                            deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                            RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    fuel_speed = fuel_speed*boxspeed
                    
                    AnswerQuad = random.randint(0, 2)                    
                    continue                
            if fuel_startx2 <= x <= (fuel_startx2 + 100) or fuel_startx2 < x + 110 < fuel_startx2 + 100:
                if fuel_starty2 <= y <= (fuel_starty2 + 100) or fuel_starty2 <= y + 54 <= fuel_starty2 + 100:
                    lives += -1
                    pygame.mixer.Sound.play(crash_sound)
                    if lives == 0:
                        pygame.mixer.Sound.play(gameover_sound)
                        GameOver(score)
                    fuel_startx1, fuel_startx2, fuel_startx3 = random.randint(1300, 1350), random.randint(1300, 1350), random.randint(1300, 1350)
                    fuel_starty1, fuel_starty2, fuel_starty3 = random.randint(100, 120), random.randint(300, 320), random.randint(500, 520)
                    
                    number1, number2 = random.randint(1, difficulty), random.randint(1, difficulty)
                    deduceFactor1, deduceFactor2, deduceFactor3, deduceFactor4 = random.randint(0, 1), random.randint(1, 2), random.randint(2, 3), random.randint(1, 2)
                    RandNumber1, RandNumber2, RandNumber3, RandNumber4 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2), abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)

                    if RandNumber1*RandNumber2 == number1*number2:
                        deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                        RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                        if RandNumber1*RandNumber2 == number1*number2:
                            deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                            RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                    if RandNumber3*RandNumber4 == number1*number2:
                        deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                        RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                        if RandNumber3*RandNumber4 == number1*number2:
                            deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                            RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    AnswerQuad = random.randint(0, 2)
                    continue
            if fuel_startx3 <= x <= (fuel_startx3 + 100) or fuel_startx3 < x + 110 < fuel_startx3 + 100:
                if fuel_starty3 <= y <= (fuel_starty3 + 100) or fuel_starty3 <= y + 54 <= fuel_starty3 + 100:
                    lives += -1
                    pygame.mixer.Sound.play(crash_sound)
                    if lives == 0:
                        pygame.mixer.Sound.play(gameover_sound)
                        GameOver(score)
                    fuel_startx1, fuel_startx2, fuel_startx3 = random.randint(1300, 1350), random.randint(1300, 1350), random.randint(1300, 1350)
                    fuel_starty1, fuel_starty2, fuel_starty3 = random.randint(100, 120), random.randint(300, 320), random.randint(500, 520)
                    
                    number1, number2 = random.randint(1, difficulty), random.randint(1, difficulty)
                    deduceFactor1, deduceFactor2, deduceFactor3, deduceFactor4 = random.randint(0, 1), random.randint(1, 2), random.randint(2, 3), random.randint(1, 2)
                    RandNumber1, RandNumber2, RandNumber3, RandNumber4 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2), abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)

                    if RandNumber1*RandNumber2 == number1*number2:
                        deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                        RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                        if RandNumber1*RandNumber2 == number1*number2:
                            deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                            RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                    if RandNumber3*RandNumber4 == number1*number2:
                        deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                        RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                        if RandNumber3*RandNumber4 == number1*number2:
                            deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                            RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    AnswerQuad = random.randint(0, 2)
                    continue

    
        if AnswerQuad == 1:
            Answer(number1, number2, fuel_startx2, fuel_starty2)
            GenWrong1(RandNumber1, RandNumber2, RandNumber3, RandNumber4, fuel_startx1, fuel_starty1, number1, number2)
            GenWrong2(RandNumber1, RandNumber2, RandNumber3, RandNumber4, fuel_startx3, fuel_starty3, number1, number2)
            if fuel_startx1 <= x <= (fuel_startx1 + 100) or fuel_startx1 < x + 110 < fuel_startx1 + 100:
                if fuel_starty1 <= y <= (fuel_starty1 + 100) or fuel_starty1 <= y + 50 <= fuel_starty1 + 100:
                    lives += -1
                    pygame.mixer.Sound.play(crash_sound)
                    if lives == 0:
                        pygame.mixer.Sound.play(gameover_sound)
                        GameOver(score)
                    fuel_startx1, fuel_startx2, fuel_startx3 = random.randint(1300, 1350), random.randint(1300, 1350), random.randint(1300, 1350)
                    fuel_starty1, fuel_starty2, fuel_starty3 = random.randint(100, 120), random.randint(300, 320), random.randint(500, 520)
                    
                    number1, number2 = random.randint(1, difficulty), random.randint(1, difficulty)
                    deduceFactor1, deduceFactor2, deduceFactor3, deduceFactor4 = random.randint(0, 1), random.randint(1, 2), random.randint(2, 3), random.randint(1, 2)
                    RandNumber1, RandNumber2, RandNumber3, RandNumber4 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2), abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)

                    if RandNumber1*RandNumber2 == number1*number2:
                        deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                        RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                        if RandNumber1*RandNumber2 == number1*number2:
                            deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                            RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                    if RandNumber3*RandNumber4 == number1*number2:
                        deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                        RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                        if RandNumber3*RandNumber4 == number1*number2:
                            deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                            RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    AnswerQuad = random.randint(0, 2)
                    continue
                
            if fuel_startx2 <= x <= (fuel_startx2 + 100) or fuel_startx2 < x + 110 < fuel_startx2 + 100:
                if fuel_starty2 <= y <= (fuel_starty2 + 100) or fuel_starty2 <= y + 54 <= fuel_starty2 + 100:
                    score += scorepoints
                    if score >= highscore:
                        highscore = score
                    pygame.mixer.Sound.play(coll_sound)
                    fuel_startx1, fuel_startx2, fuel_startx3 = random.randint(1300, 1350), random.randint(1300, 1350), random.randint(1300, 1350)
                    fuel_starty1, fuel_starty2, fuel_starty3 = random.randint(100, 120), random.randint(300, 320), random.randint(500, 520)
                    
                    number1, number2 = random.randint(1, difficulty), random.randint(1, difficulty)
                    deduceFactor1, deduceFactor2, deduceFactor3, deduceFactor4 = random.randint(0, 1), random.randint(1, 2), random.randint(2, 3), random.randint(1, 2)
                    RandNumber1, RandNumber2, RandNumber3, RandNumber4 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2), abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    if RandNumber1*RandNumber2 == number1*number2:
                        deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                        RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                        if RandNumber1*RandNumber2 == number1*number2:
                            deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                            RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                    if RandNumber3*RandNumber4 == number1*number2:
                        deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                        RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                        if RandNumber3*RandNumber4 == number1*number2:
                            deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                            RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    fuel_speed = fuel_speed*boxspeed

                    AnswerQuad = random.randint(0, 2)
                    continue
            if fuel_startx3 <= x <= (fuel_startx3 + 100) or fuel_startx3 < x + 110 < fuel_startx3 + 100:
                if fuel_starty3 <= y <= (fuel_starty3 + 100) or fuel_starty3 <= y + 54 <= fuel_starty3 + 100:
                    lives += -1
                    pygame.mixer.Sound.play(crash_sound)
                    if lives == 0:
                        pygame.mixer.Sound.play(gameover_sound)
                        GameOver(score)
                    fuel_startx1, fuel_startx2, fuel_startx3 = random.randint(1300, 1350), random.randint(1300, 1350), random.randint(1300, 1350)
                    fuel_starty1, fuel_starty2, fuel_starty3 = random.randint(100, 120), random.randint(300, 320), random.randint(500, 520)
                    
                    number1, number2 = random.randint(1, difficulty), random.randint(1, difficulty)
                    deduceFactor1, deduceFactor2, deduceFactor3, deduceFactor4 = random.randint(0, 1), random.randint(1, 2), random.randint(2, 3), random.randint(1, 2)
                    RandNumber1, RandNumber2, RandNumber3, RandNumber4 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2), abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    if RandNumber1*RandNumber2 == number1*number2:
                        deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                        RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                        if RandNumber1*RandNumber2 == number1*number2:
                            deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                            RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                    if RandNumber3*RandNumber4 == number1*number2:
                        deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                        RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                        if RandNumber3*RandNumber4 == number1*number2:
                            deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                            RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    AnswerQuad = random.randint(0, 2)
                    continue


        if AnswerQuad == 2:
            Answer(number1, number2, fuel_startx3, fuel_starty3)
            GenWrong1(RandNumber1, RandNumber2, RandNumber3, RandNumber4, fuel_startx1, fuel_starty1, number1, number2)
            GenWrong2(RandNumber1, RandNumber2, RandNumber3, RandNumber4, fuel_startx2, fuel_starty2, number1, number2)
            if fuel_startx1 <= x <= (fuel_startx1 + 100) or fuel_startx1 < x + 110 < fuel_startx1 + 100:
                if fuel_starty1 <= y <= (fuel_starty1 + 100) or fuel_starty1 <= y + 50 <= fuel_starty1 + 100:
                    lives += -1
                    pygame.mixer.Sound.play(crash_sound)
                    if lives == 0:
                        pygame.mixer.Sound.play(gameover_sound)
                        GameOver(score)
                    fuel_startx1, fuel_startx2, fuel_startx3 = random.randint(1300, 1350), random.randint(1300, 1350), random.randint(1300, 1350)
                    fuel_starty1, fuel_starty2, fuel_starty3 = random.randint(100, 120), random.randint(300, 320), random.randint(500, 520)
                    
                    number1, number2 = random.randint(1, difficulty), random.randint(1, difficulty)
                    deduceFactor1, deduceFactor2, deduceFactor3, deduceFactor4 = random.randint(0, 1), random.randint(1, 2), random.randint(2, 3), random.randint(1, 2)
                    RandNumber1, RandNumber2, RandNumber3, RandNumber4 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2), abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    if RandNumber1*RandNumber2 == number1*number2:
                        deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                        RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                        if RandNumber1*RandNumber2 == number1*number2:
                            deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                            RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                    if RandNumber3*RandNumber4 == number1*number2:
                        deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                        RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                        if RandNumber3*RandNumber4 == number1*number2:
                            deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                            RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    AnswerQuad = random.randint(0, 2)
                    continue
                
            if fuel_startx2 <= x <= (fuel_startx2 + 100) or fuel_startx2 < x + 110 < fuel_startx2 + 100:
                if fuel_starty2 <= y <= (fuel_starty2 + 100) or fuel_starty2 <= y + 54 <= fuel_starty2 + 100:
                    lives += -1
                    if lives == 0:
                        pygame.mixer.Sound.play(gameover_sound)
                        GameOver(score)
                    pygame.mixer.Sound.play(crash_sound)
                    fuel_startx1, fuel_startx2, fuel_startx3 = random.randint(1300, 1350), random.randint(1300, 1350), random.randint(1300, 1350)
                    fuel_starty1, fuel_starty2, fuel_starty3 = random.randint(100, 120), random.randint(300, 320), random.randint(500, 520)
                    
                    number1, number2 = random.randint(1, difficulty), random.randint(1, difficulty)
                    deduceFactor1, deduceFactor2, deduceFactor3, deduceFactor4 = random.randint(0, 1), random.randint(1, 2), random.randint(2, 3), random.randint(1, 2)
                    RandNumber1, RandNumber2, RandNumber3, RandNumber4 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2), abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    if RandNumber1*RandNumber2 == number1*number2:
                        deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                        RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                        if RandNumber1*RandNumber2 == number1*number2:
                            deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                            RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                    if RandNumber3*RandNumber4 == number1*number2:
                        deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                        RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                        if RandNumber3*RandNumber4 == number1*number2:
                            deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                            RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    AnswerQuad = random.randint(0, 2)
                    continue
                
            if fuel_startx3 <= x <= (fuel_startx3 + 100) or fuel_startx3 < x + 110 < fuel_startx3 + 100:
                if fuel_starty3 <= y <= (fuel_starty3 + 100) or fuel_starty3 <= y + 54 <= fuel_starty3 + 100:
                    score += scorepoints
                    if score >= highscore:
                        highscore = score
                    pygame.mixer.Sound.play(coll_sound)
                    fuel_startx1, fuel_startx2, fuel_startx3 = random.randint(1300, 1350), random.randint(1300, 1350), random.randint(1300, 1350)
                    fuel_starty1, fuel_starty2, fuel_starty3 = random.randint(100, 120), random.randint(300, 320), random.randint(500, 520)

                    number1, number2 = random.randint(1, difficulty), random.randint(1, difficulty)
                    deduceFactor1, deduceFactor2, deduceFactor3, deduceFactor4 = random.randint(0, 1), random.randint(1, 2), random.randint(2, 3), random.randint(1, 2)
                    RandNumber1, RandNumber2, RandNumber3, RandNumber4 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2), abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    if RandNumber1*RandNumber2 == number1*number2:
                        deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                        RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                        if RandNumber1*RandNumber2 == number1*number2:
                            deduceFactor1, deduceFactor2 = random.randint(1, 2), random.randint(1, 2)
                            RandNumber1, RandNumber2 = abs(number1 + deduceFactor1), abs(number2 - deduceFactor2)
                    if RandNumber3*RandNumber4 == number1*number2:
                        deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                        RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                        if RandNumber3*RandNumber4 == number1*number2:
                            deduceFactor3, deduceFactor4 = random.randint(2, 3), random.randint(1, 2)
                            RandNumber3, RandNumber4 = abs(number2 + deduceFactor3), abs(number1 - deduceFactor4)
                    
                    fuel_speed = fuel_speed*boxspeed
                    AnswerQuad = random.randint(0, 2)
                    continue
        plane(x,y)
        HighScoreDisplay(highscore)    
        ScoreDisplay(score)
        LivesDisplay(lives)
        Question(number1, number2)
        mouse = pygame.mouse.get_pos() #Buttons start
        click = pygame.mouse.get_pressed()

        pygame.display.update()
        clock.tick(60)

MainMenu()

pygame.quit()
quit()
