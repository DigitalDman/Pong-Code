######################################################
# Name: Daniel Leftley #Date: 21/12/2023
# File: Pong_Leftley_Daniel.py
# Description: A remake of the clasic pong game made by me
######################################################

import os # Setting the spot on the screen where the window generates
x = 100
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'
import random, pygame, pgzero, pgzrun, math
from pygame import mixer #Mixer is for the background music
pygame.mixer.pre_init(44100,16,2,4096) #I honestly dont know what this line and the next one do
pygame.init() # I was just told to put them in when I searched up how to use background music for just quit(The game I made)

#Setting Background music (Its the title screen theme from the terraria calamity mod)
pygame.mixer.music.load('bgmusic.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

WIDTH = 800
HEIGHT = 600

#setting Actors
background = Actor('board')
background.x = 400
background.y = 300

player1 = Actor('paddle')
player1.x = 20
player1.y = 300

player2 = Actor('paddle2')
player2.x = 760
player2.y = 300

ball = Actor('ball')
ball.x = 400
ball.y = 300

pause1 = Actor('pause1')
pause1.pos = 350,50

pause2 = Actor('pause2')
pause2.pos = 350,550

#setting Variables
bounceS = random.randint(1,2)
bounceRD = random.randint(1,2) #RD stands for roof direction (up or down)

bounceHS = random.randint(0,10) #HS stands for height speed
roofhit = 0

P1Lives = 3
P2Lives = 3

P2Score = 0
P1Score = 0
ScoreColldown1 = 0 # I mispelled it... oops
ScoreColldown2 = 0 # The cooldowns (Spelt it right) are so you cant farm points if you get it by one of the edges

win = 0

Level = 1

SpeedUp = 0

Pause = True

def update():
    global bounceS, bounceRD, bounceHS, win, P1Lives, P2Lives, P1Score, P2Score, SpeedUp, ScoreColldown1, ScoreColldown2, Level, Pause

    if Pause: #Unpause's the game if R is pressed
        if keyboard.r:
            Pause = False

    if Pause == False: #Runs everything when unpaused
        #Setting the original y position of both players
        P1Original = player1.y
        P2Original = player2.y

        #Makeing the ScoreCooldown count down
        ScoreColldown1 -= 1/60
        ScoreColldown2 -= 1/60

        #If BounceS = 1, move the ball right and it hasnt hit the roof yet, the ball speed is dependant on the SpeedUp value
        if bounceS == 1:
            ball.x += 5 + SpeedUp
        #moveing the ball left if BounceS = 2 and it has not hit the roof yet
        if bounceS == 2:
            ball.x -= 5 + SpeedUp
        # If bounceRD = 1 move the ball down
        if bounceRD == 1:
            ball.y += bounceHS + SpeedUp
        #move ball up if bounceRD = 2
        if bounceRD == 2:
            ball.y -= bounceHS + SpeedUp

        #Switching ball direction (Up, Down) if it hits one of the edges
        if ball.y > 570:
            bounceRD = 2
        if ball.y < 30:
            bounceRD = 1
        
        #Moveing the players
        if keyboard.w:
            player1.y -= 6.5
        if keyboard.s:
            player1.y += 6.5
        if keyboard.up:
            player2.y -= 6.5
        if keyboard.down:
            player2.y += 6.5

        #Makeing sure the players dont go off the screen
        if player1.y + 50 > 570 or player1.y - 50 < 30: #The + and - 50 are so the player doesnt stop at the center but the bottom and top ends of the paddle
            player1.y = P1Original
        if player2.y + 50 > 570 or player2.y - 50 < 30:
            player2.y = P2Original

        # Detecting if the ball hits player 1
        if ball.colliderect(player1) and ScoreColldown1 <= 0:
            P1Score += 1
            bounceS = 1
            bounceRD = random.randint(1,2)
            bounceHS = random.randint(0,10)
            ScoreColldown1 = 2

        if ball.colliderect(player2) and ScoreColldown2 <= 0:
            P2Score += 1
            bounceS = 2
            bounceRD = random.randint(1,2)
            bounceHS = random.randint(0,10)
            ScoreColldown2 = 2

        # Makeing it so if the ball flies off the screen the players lose a life depending on who's side it flew off on
        if ball.x < 0:
            P1Lives -= 1
            ball.pos = (400,300)
            bounceS = random.randint(1,2)
        if ball.x > 800:
            P2Lives -= 1
            ball.pos = (400,300)
            bounceS = random.randint(1,2)

        # Setting it so if one player has 0 lives, the other player wins
        if P1Lives == 0:
            win = 2
        if P2Lives == 0:
            win = 1
        
        #Setting the level depending on combined score
        if P1Score + P2Score == 10:
            Level = 2
        if P1Score + P2Score == 10 + math.floor(10*1.5): #10*1.5 = 25, just did it like this because I wanted too
            Level = 3
        if P1Score + P2Score == 25 + math.floor(25*1.5): # Thats 47 points
            Level = 4
        if P1Score + P2Score == 62 + math.floor(62*1.5):
            Level = 5
        
        # Setting the final win conditions, Level 5 is just so whenever level 4 ends to check if they win
        # If one player hits 100 points before the end of level 4
        if P1Score == 100 and P1Score > P2Score:
            win = 1
        if P2Score == 100 and P2Score > P1Score:
            win = 2
        # If one player has more points than the other by the end of level 4
        if P1Score > P2Score and Level == 5:
            win = 1
        if P2Score > P1Score and Level == 5:
            win = 2

        # Changeing the SpeedUp variable depending on the Level
        if Level == 1:
            SpeedUp = 0
        if Level == 2:
            SpeedUp = 2
        if Level == 3:
            SpeedUp = 4
        if Level == 4:
            SpeedUp = 6

        # Pauses the game if P is pressed
        if keyboard.p:
            Pause = True

def draw():
    if Pause:
        background.draw()
        pause1.draw()
        pause2.draw()
        player1.draw()
        player2.draw()
        ball.draw()
    elif win == 1:
        screen.fill((0,0,0))
        screen.draw.text('Player 1 wins', center = (400,300), color=(255,255,255), fontsize=30, fontname ="pressstart2p")
    elif win == 2:
        screen.fill((0,0,0))
        screen.draw.text('Player 2 wins', center = (400,300), color=(255,255,255), fontsize=30, fontname = "pressstart2p")
    else:   
        background.draw()
        player1.draw()
        player2.draw()
        ball.draw()
        screen.draw.text(str(P1Score), (320,50), color=(255,255,255), fontsize = 30, fontname ="pressstart2p")
        screen.draw.text(str(P2Score), (470,50), color=(255,255,255), fontsize = 30, fontname ="pressstart2p")
        screen.draw.text('Player 1 Health: ' + str(P1Lives),(10,10), color=(0,0,0), fontsize = 10, fontname ="pressstart2p")
        screen.draw.text('Player 2 Health: ' + str(P2Lives),(615,10), color=(0,0,0), fontsize = 10, fontname ="pressstart2p")
        screen.draw.text('Level:' + str(Level), (370,10), color=(0,0,0), fontsize = 10, fontname = "pressstart2p")

pgzrun.go()