# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import pygame
from pygame import mixer
import time
import threading
import math
import sys

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# background
background = pygame.image.load('background1.png')
background_music = pygame.mixer.Sound('Undertale - Megalovania.wav')
background_music.play(-1)
background_music.set_volume(0.00)



# title
pygame.display.set_caption('Spacy')
icon = pygame.image.load('startup.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('spaceship.png')
playerX = 400
playerY = height - 64
playerX_change = 0

# alien
alienX_change = []
alienY_change = []
alienX = []
alienimg = []
alienY = []
global num_of_aliens
num_of_aliens = 6
global y_min_placement
y_min_placement = 0
global y_max_placement
y_max_placement = 128

def summon_alien(y_min,y_max):
    if y_max >= height -128:
        y_max = height - 128
    alienimg.append(pygame.image.load('ufo.png'))
    alienX.append(random.randint(0, width - 64))
    alienY.append(random.randint(y_min, y_max))
    alienX_change.append(2.5)
    alienY_change.append(20)


for i in range(num_of_aliens):
    summon_alien(y_min_placement,y_max_placement)
    print(i)


# bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = height - 64
bulletX_change = 0
bulletY_change = 6.5
bullet_state = False

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#game over
over_font = pygame.font.Font('freesansbold.ttf',32)

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255,255,255))
    screen.blit(over_text, (width/2 - 84, height/2))
    background_music.set_volume(0.00)


#level complete
complete_font = pygame.font.Font('freesansbold.ttf',32)

def level_complete_text():
    # complete_text = complete_font.render('level complete', True, (255,255,255))
    # screen.blit(complete_text, (width/2 - 84, height/2))
    global level_complete
    global alienX
    global alienY
    alienX = []
    alienY = []
    if times == 0:
        for i in range(num_of_aliens):
            summon_alien(y_min_placement,y_max_placement)


def show_score(x,y):
    score = font.render('score :' +str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerimg, (x, y))


def alien(i,x, y):
    screen.blit(alienimg[i], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = True
    screen.blit(bulletimg, (x + 16, y + 10))


def alien_hit(x1, x2, y1, y2):

    distancex = abs(x1-x2)
    distancey = abs(y1-y2)
    if distancex + distancey < 36 and bullet_state:
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        explosion_sound.set_volume(0.0)
        return True
    return False


# game loop
running = True
move_Left = False
move_Right = False
fire_again = True
game_over = False
times = 0
global level_complete
level_complete = False
up_down = 0
x_movement = 0
while running:

    # screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        # keystroke

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5

                move_Left = True

            elif event.key == pygame.K_RIGHT:
                move_Right = True
                playerX_change = 5


            if event.key == pygame.K_SPACE and not bullet_state:
                x_pos = playerX
                fire(x_pos, playerY)
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bullet_sound.set_volume(0.0)

        #attemps to fix movement
        if move_Left and move_Right:
            pygame.event.wait()
            move_Right = event.key == pygame.K_RIGHT
            move_Left = event.key == pygame.K_LEFT

        elif event.type == pygame.KEYUP:
            move_Right = False
            move_Left = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX = playerX + playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= width - 64:
        playerX = width - 64

    # alien boundries
    num_dead = 0
    for i in range(num_of_aliens):

        if abs(alienX[i] - playerX) < 36 and abs(alienY[i] - playerY) < 36:
            for j in range(num_of_aliens):
                alienY[j] = height + 64
            game_over = True
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            explosion_sound.set_volume(0.3)
            break



        alienX[i] = alienX[i] + alienX_change[i]




        if alienX[i] <= 0:
            alienX_change[i] = 2.5
            alienY[i] = alienY[i] + alienY_change[i]
        if alienX[i] >= width - 64:
            alienY[i] = alienY[i] + alienY_change[i]
            alienX_change[i] = -2.5

    
        # collision
        collide = alien_hit(alienX[i], bulletX, alienY[i], bulletY)

        if collide:
            bulletY = playerY
            bullet_state = False
            score_value = score_value + 1
            alienX[i] = 0
            alienY[i] = height + 64

        if alienY[i] > height:
            num_dead = num_dead + 1
        if num_dead == num_of_aliens:
            level_complete = True
            num_of_aliens = num_of_aliens + 2
            y_min_placement = y_min_placement + 64
            y_max_placement = y_max_placement + 64
        alien(i,alienX[i], alienY[i])

    # bullet movement
    if bullet_state:
        bulletX = x_pos
        fire(x_pos, bulletY)
        bulletY = bulletY - bulletY_change
    else:
        bulletX = playerX

    if bulletY <= 0:
        bulletY = playerY
        bullet_state = False

    if game_over:
        game_over_text()
        break
    if level_complete:
        level_complete_text()
        level_complete = False
        # if times == 25:
        #
        #     times = 0
        # times = times + 1


    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()

