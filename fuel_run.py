import pygame
import time
import sys
import random
from parts import Cloud, Player, FuelBox

pygame.init()
pygame.font.init()
pygame.mixer.pre_init()

game_icon = pygame.image.load("Resources/Images/Icon.png")
trophy = pygame.transform.scale(pygame.image.load("Resources/Images/Trophy.png"), (90, 90))
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

leaderboard_list = open("leaderboard.txt", "a+")
leaderboard_list.close()
player = Player(screen, 25)

# For each difficulty: maximum time table no., speed of  fuel boxes, points gained from each correct answer, and no. of lives
difficulty = {'easy':[6, 1.01, 5, 3], 'medium': [12, 1.02, 10, 4], 'hard': [16, 1.03, 15, 5]}
section = [[(-100, 300), (350, 650), (700, 1000)], [(5, 210), (240, 440), (460, 670)]]
cloud_speed = (-20, -10)

def display_text(text, colour, size, pos, is_centered=True):
    font = pygame.font.Font("Resources/BULKYPIX.ttf", size)
    text_surface = font.render(text, True, colour) #i_red
    disp_pos = (int(pos[0]), int(pos[1]))
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

def player_keydown(event, direction):
    if event.key == pygame.K_LEFT:
        direction[0] = -1
    if event.key == pygame.K_RIGHT:
        direction[0] = 1
    if event.key == pygame.K_DOWN:
        direction[1] = 1
    if event.key == pygame.K_UP:
        direction[1] = -1
    return direction

def player_keyup(event, direction):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
        direction[0] = 0
    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
        direction[1] = 0
    return direction

def update_highscores(name, highscore):
    updated = False
    entry = name.ljust(30 - len(str(highscore))) + str(highscore)+"\n"
    with open("leaderboard.txt", "r+") as f:
        scores = f.readlines()
        num_scores = len(scores)
        if num_scores == 0:
            f.write(entry)
            updated = True
        else:
            index = 0
            for index, item in enumerate(scores):
                curr_score = int(item.strip("\n").split()[1])
                if highscore > curr_score:
                    updated = True
                    break
            if not updated and num_scores < 10:
                index = num_scores
                updated = True
            scores.insert(index, entry)
            num_scores = num_scores + 1
            if num_scores > 10: scores.pop()
            f.seek(0)
            f.writelines(scores)
    return updated

def get_highscores():
    out = []
    with open("leaderboard.txt", "r") as f:
        for item in f.readlines():
            out.append(item.strip("\n"))
    if not out:
        out.append("No highscores yet!")
    return out

def get_highscore():
    try:
        top_score = int(get_highscores()[0].split()[1])
    except ValueError:
        return 0
    return top_score

def main_menu():
    global HIGHSCORE
    global clouds
    HIGHSCORE = get_highscore()
    pygame.mixer.music.load("Resources/Sound/Overworld.mp3")
    pygame.mixer.music.play(-1)
    
    move_direction = [0, 0]
    clouds = [Cloud(cloud_speed, 1, section[1][i], screen) for i in range(3)]
    player.reset()

    MAIN_MENU = True
    while MAIN_MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                move_direction = player_keydown(event, move_direction)
                if event.key == pygame.K_SPACE:
                    player.change_style()
            if event.type == pygame.KEYUP:
                move_direction = player_keyup(event, move_direction)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if 520 + 240 > mouse[0] and mouse[0] > 520 and 250 + 120 > mouse[1] and mouse[1] > 250:
                    pygame.mixer.Sound.play(button_sound)
                    if (not level_select()):
                        pygame.mixer.music.load("Resources/Sound/Overworld.mp3")
                        pygame.mixer.music.play(-1)
                if 540 + 200 > mouse[0] and mouse[0] > 540 and 400 + 100 > mouse[1] and mouse[1] > 400:
                    pygame.mixer.Sound.play(button_sound)
                    leaderboard()
                if 540 + 200 > mouse[0] and mouse[0] > 540 and 530 + 100 > mouse[1] and mouse[1] > 530:
                    pygame.mixer.Sound.play(button_sound)
                    pygame.quit()
                    sys.exit()

        screen.fill(s_blue)
        
        for cloud in clouds: cloud.draw()
        player.move(move_direction)

        display_text("Fuel Run", i_red, 175, (display_width/2, display_height/5))
        
        mouse = pygame.mouse.get_pos()

        btn_hover = 520 + 240 > mouse[0] and mouse[0] > 520 and 250 + 120 > mouse[1] and mouse[1] > 250
        pygame.draw.rect(screen, buttonover_green*btn_hover or button_red*(not btn_hover), (520, 250, 240, 120))
        pygame.draw.polygon(screen, white, ((610, 270), (610, 350), (690, 310)))

        btn_hover = 540 + 200 > mouse[0] and mouse[0] > 540 and 400 + 100 > mouse[1] and mouse[1] > 400
        pygame.draw.rect(screen, csi_blue*btn_hover or button_red*(not btn_hover), (540, 400, 200, 100))
        trophy_size = trophy.get_rect().size
        screen.blit(trophy, (int(display_width/2 - trophy_size[0]/2), int(450-trophy_size[1]/2)))

        btn_hover = 540 + 200 > mouse[0] and mouse[0] > 540 and 530 + 100 > mouse[1] and mouse[1] > 530
        pygame.draw.rect(screen, csi_blue*btn_hover or button_red*(not btn_hover), (540, 530, 200, 100))
        display_text("Quit", a_blue, 60, (display_width/2 + 5, 590))
        
        pygame.display.update()
        clock.tick(30)

def leaderboard():
    scores = get_highscores()
    move_direction = [0, 0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                move_direction = player_keydown(event, move_direction)
            elif event.type == pygame.KEYUP:
                move_direction = player_keyup(event, move_direction)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if 40 + 160 > mouse[0] and mouse[0] > 40 and 40 + 60 > mouse[1] and mouse[1] > 40:
                    pygame.mixer.Sound.play(button_sound)
                    return False
                elif 515 + 250 > mouse[0] and mouse[0] > 515 and 250 + 80 > mouse[1] and mouse[1] > 250:
                    pygame.mixer.Sound.play(button_sound)

                elif 515 + 250 > mouse[0] and mouse[0] > 515 and 400 + 80 > mouse[1] and mouse[1] > 400:
                    pygame.mixer.Sound.play(button_sound)

                elif 515 + 250 > mouse[0] and mouse[0] > 515 and 550 + 80 > mouse[1] and mouse[1] > 550:
                    pygame.mixer.Sound.play(button_sound)
        screen.fill(s_blue)

        for cloud in clouds: cloud.draw()
        player.move(move_direction)

        display_text("Leaderboard", i_red, 70, (display_width/2, display_height/6))

        i = 1
        for score in scores:
            name, highscore = score.split()
            display_text(name, i_red, 40, (350, display_height/5 + 50*i))
            display_text(highscore, i_red, 40, (925, display_height/5 + 50*i))
            i = i + 1

        mouse = pygame.mouse.get_pos()
        btn_hover = 40 + 160 > mouse[0] and mouse[0] > 40 and 40 + 60 > mouse[1] and mouse[1] > 40
        pygame.draw.rect(screen, csi_blue*btn_hover or button_red*(not btn_hover), (40, 40, 160, 60))
        display_text("Home", a_blue, 30, (65, 60), False)

        pygame.display.update()
        clock.tick(30)

def level_select():
    move_direction = [0, 0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                move_direction = player_keydown(event, move_direction)
            elif event.type == pygame.KEYUP:
                move_direction = player_keyup(event, move_direction)
            elif event.type == pygame.MOUSEBUTTONUP:
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
        player.move(move_direction)
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

def unpause():
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
        display_text("Home", a_blue, 45, (display_width/2, 535))
        
        pygame.display.update()
        clock.tick(30)

def game_loop(difficulty_settings):
    global PAUSE
    global HIGHSCORE
    HIGHSCORE = get_highscore()
    PAUSE = False
    trigger = True
    pygame.mixer.music.load("Resources/Sound/Bit Quest.mp3")
    pygame.mixer.music.play(-1)
    fuel_box_sections = [(100, 120), (300, 320), (500, 520)]
    fuel_boxes = [FuelBox(fuel_box_sections[i], 100, 35, screen) for i in range(3)]

    player.reset()
    move_direction = [0, 0]
    fuel_speed = -10
    score = 0
    time_table = difficulty_settings[0]
    boxspeed = difficulty_settings[1]
    points = difficulty_settings[2]
    lives = difficulty_settings[3]
    
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    PAUSE = True
                    go_back = paused()
                    if(go_back):
                        return False
                move_direction = player_keydown(event, move_direction)
            if event.type == pygame.KEYUP:
                move_direction = player_keyup(event, move_direction)

        screen.fill(s_blue)
        for cloud in clouds: cloud.draw()
        player.move(move_direction)

        if (trigger):
            numbers = generate_numbers(time_table)
            answer_section = random.randint(0, 2)
            fuel_boxes = reset_fuel_boxes(fuel_boxes, answer_section, numbers, fuel_speed)
            trigger = False
            
        hit = -1
        fuel_gone = False
        for i in range(len(fuel_boxes)):
            fuel_boxes[i].draw()
            fuel_gone = fuel_gone or fuel_boxes[i].check_bounds()
            x, y = fuel_boxes[i].x_pos, fuel_boxes[i].y_pos
            if player.hit_object((x - 110, x + 110), (y - 50, y + 100)):
                hit = i

        if(hit+1 or fuel_gone):
            trigger = True
            if hit == answer_section:
                score += points
                pygame.mixer.Sound.play(coll_sound)
                fuel_speed = fuel_speed*boxspeed
            else:
                pygame.mixer.Sound.play(crash_sound)
                lives -= 1
                if lives == 0:
                    pygame.mixer.Sound.play(gameover_sound)
                    return game_over(score)

        display_text("Score: " + str(score), i_red, 40, (50, 650), False)
        is_new = score > HIGHSCORE
        display_text("Highscore: " + str(HIGHSCORE*(not is_new) + score*is_new), i_red, 25, (50, 600), False)
        display_text(str(lives) + " Lives", i_red, 50, (1000, 650), False)
        display_text(str(numbers[-1]) + " x " + str(numbers[-2]) + " = ?", i_red, 80, (display_width/2, 75))

        pygame.display.update()
        clock.tick(30)

def game_over(score):
    if score > HIGHSCORE: text = "New Highscore: "
    else: text = "Score: "
    prompt = "Done?"
    pygame.mixer.Sound.play(gameover_sound)
    
    clouds_down = [Cloud(cloud_speed, 0, section[0][i], screen) for i in range(3)]
    rotation = 1
    player.reset()
    name = ""
    name_entered = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if name_entered and 520 + 240 > mouse[0] and mouse[0] > 520 and 310 + 120 > mouse[1] and mouse[1] > 310:
                    pygame.mixer.Sound.play(button_sound)
                    for cloud in clouds: cloud.reset()
                    return True
                elif 540 + 200 > mouse[0] and mouse[0] > 540 and 500 + 100 > mouse[1] and mouse[1] > 500:
                    if name_entered:
                        pygame.mixer.Sound.play(button_sound)
                        for cloud in clouds: cloud.reset()
                        return False
                    else:
                        pygame.mixer.Sound.play(button_sound)
                        name_entered = True
                        if not name:
                            name = "player"
                        update_highscores(name, score)
                        prompt = "Home"
            if not name_entered and event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and len(name) < 9:
                    name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

        screen.fill(s_blue)

        for cloud in clouds_down: cloud.draw()

        display_text(text+str(score)+"!", i_red, 70, (display_width/2, display_height/5))
        
        mouse = pygame.mouse.get_pos()

        if name_entered:
            display_text("Well done, " + name, i_red, 50, (display_width/2, display_height/3))
            btn_hover = 520 + 240 > mouse[0] and mouse[0] > 520 and 310 + 120 > mouse[1] and mouse[1] > 310
            pygame.draw.rect(screen, buttonover_green*btn_hover or button_red*(not btn_hover), (520, 310, 240, 120))
            pygame.draw.polygon(screen, white, ((610, 330), (610, 410), (690, 370)))
        else:
            display_text("Enter your name:", i_red, 50, (display_width/2, display_height/3))
            display_text(name, i_red, 50, (display_width/2, display_height/3 + 70))

        btn_hover = 540 + 200 > mouse[0] and mouse[0] > 540 and 500 + 100 > mouse[1] and mouse[1] > 500
        pygame.draw.rect(screen, csi_blue*btn_hover or button_red*(not btn_hover), (540, 500, 200, 100))
        display_text(prompt, a_blue, 45, (display_width/2, 555))

        #player.rotate(rotation)

        pygame.display.update()
        clock.tick(30)

main_menu()

pygame.quit()
sys.exit()
