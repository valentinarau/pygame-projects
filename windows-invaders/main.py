import pygame
import random
import math

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('arch.png')

# Title and Icon
pygame.display.set_caption("Windows Invaders")
icon = pygame.image.load("www.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("penguin.png")
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('wxp.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "loaded"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bulletImg, (x + 25, y + 20))


# Score
score = 0
font = pygame.font.Font("PKMN RBYGSC.ttf", 32)

textX = 10
textY = 10

def show_score(x,y):
    scoreImg = font.render("Bug fixes: " + str(score), True, (255,0,193))
    screen.blit(scoreImg, (x, y))

# Game Over
over_font = pygame.font.Font("PKMN RBYGSC.ttf", 64)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (150, 250))



# Collision
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "loaded":
                    bulletX = playerX
                    bulletY = 480
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Show, move player
    playerX += playerX_change

    # Check player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Check enemy
    for i in range(num_enemies):
        # Game Over
        if enemyY[i] > 400:
            for j in range(num_enemies):
                enemyY[j] = 2000
            screen.fill((0, 0, 0))
            game_over_text()

            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "loaded"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Check bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "loaded"

    if bullet_state == "fired":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
