import pygame
import random as r
import math
from pygame import mixer

# Initialization of package
pygame.init()

# screen creation
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space.png")
pygame.display.set_icon(icon)

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Background
background = pygame.image.load('background.png')

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = list()
enemyX = list()
enemyY = list()
enemyX_change = list()
enemyY_change = list()
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(r.randint(0, 735))
    enemyY.append(r.randint(50, 150))
    enemyX_change.append(6)
    enemyY_change.append(55)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8
""" Ready - You can't see bullet on the screen
    Fire -- The bullet is currently moving
"""
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(ex, ey, bx, by):
    distance = math.sqrt((math.pow(ex - bx, 2)) + (math.pow(ey - by, 2)))
    # print(distance)
    if distance < 27:
        return True
    return False


# Game Loop
running = True

while running:
    # RGB - red, green, blue
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # to check for keystroke whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    for i in range(num_of_enemies):

        if enemyY[i] >= 350:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

            # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = r.randint(0, 735)
            enemyY[i] = r.randint(50, 150)

            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
        enemy(enemyX[i], enemyY[i], i)
    # Bullet movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
