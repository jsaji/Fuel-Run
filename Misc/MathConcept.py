import random, pygame, time
from pygame.locals import *
from time import sleep



black = ( 0, 0, 0)
white = (255, 255, 255)
green = ( 0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

score = 0
lives = 5

"""def countdown(n):
    v = 1
    while True:
        for i in range(0, 10, 1):
            sleep(1)
            print (10 - i)
            if (KeyboardInterrupt, SystemExit):
                v = v - 1
            else:
                pass"""


print("Welcome to this multiplication game!")
name = input("What's your name? ")
print ("Well,", name, "Good Luck!")


while lives >= 1:
    number1 = random.randint(0, 12)
    number2 = random.randint(0, 12)
    try:
        print(number1, "x", number2, "= ?")
        answer = number1*number2
        choice = int(input("  "))
        if choice == answer:
            print ("Correct")
            score = score + 1
        else:
            print ("Incorrect.", answer, "was the right answer.")
            lives = lives - 1
    except ValueError
    :
        print("Enter something valid.")
    
print ("Darn,", name, "- you lost all your lives.", score, "is your score.")

"""while lives >= 1:
    number1 = random.randint(0, 12)
    number2 = random.randint(0, 12)
    try:
        print(number1, "x", number2, "= ?")
        countdown()
        answer = number1*number2
        choice = int(input("  "))
        if choice == answer:
            print ("Correct")
            score = score + 1
        else:
            print ("Incorrect.", answer, "was the right answer.")
            lives = lives - 1
    except ValueError:
        print("Enter something valid.")
    
print ("Darn,", name, "- you lost all your lives.", score, "is your score.")"""
