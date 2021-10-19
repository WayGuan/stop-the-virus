# press left or right arrow to move the guard and aim the virus
# press the space button to allow the guard shot a mask to mask the virus
import math
import random
import pygame
from pygame import mixer

# initialize
pygame.init()

# create the screen
screen = pygame.display.set_mode((600, 700))

# Title and Icon
pygame.display.set_caption("Stop the virus")
icon = pygame.image.load('fierce_virus.png')
pygame.display.set_icon(icon)

# Audio
mixer.music.set_volume(0.1)
mixer.music.load("stop_the_virus.mp3")
mixer.music.play(-1)

# Guard
guardImage = pygame.image.load("guard.png")
guardX = 270
guardY = 600
guardX_change = 0

# Virus
virusImgs = []
virusXs = []
virusYs = []
virusX_changes = []
virusY_changes = []
num_of_viruses = 5
virusImg = pygame.image.load("fierce_virus.png")
virus_status = "fierce"
virus_width = 64
virus_height = 64

for i in range(num_of_viruses):
    virusImgs.append(virusImg)
    virusXs.append(random.randint(0, 536))
    virusYs.append(random.randint(50, 150))
    virusX_changes.append(0.2)
    virusY_changes.append(50)

# MASKED VIRUS
maskedImg = pygame.image.load("virus.png")
maskedX = 0
maskedY = 0

# Mask, mask is shot out and moves up when mask_status is fire
maskImg = []
maskImage = pygame.image.load("mask.png")
maskX = guardX
maskY = 600
maskY_change = 0.5
mask_status = "ready"

# Score
score = 0
score_font = pygame.font.SysFont(None, 32)
textX = 10
textY = 10


# Game Over
game_over_font = pygame.font.SysFont(None, 64)


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (180, 250))
    pygame.mixer.music.unload()


def show_score(x, y):
    score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))


def guard():
    screen.blit(guardImage, (guardX, guardY))


def virus():
    screen.blit(virusImgs[i], (virusXs[i], virusYs[i]))


def masked_virus(img, x, y):
    screen.blit(img, (x, y))


def mask():
    global mask_status
    mask_status = "fire"
    screen.blit(maskImage, (maskX + 16, maskY - 10))


def is_collision(virusX, virusY, maskX, maskY):
    distance = math.sqrt((math.pow(virusX - maskX, 2) + math.pow(virusY - maskY, 2)))
    if distance < 50:
        return True
    else:
        return False


# Game loop
# flag variable
game_running = True
while game_running:
    #  background RGB color fill
    screen.fill((10, 10, 0))
    # check the key stroke events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        # when key pressed, set the guardX_change accordingly
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                guardX_change = -0.4
            if event.key == pygame.K_RIGHT:
                guardX_change = 0.4
            if event.key == pygame.K_SPACE:
                if mask_status == "ready":
                    maskX = guardX
                    mask()
        # when left or right key released, set the guardX_change back to 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                guardX_change = 0

    # update the guardX
    guardX += guardX_change
    # ensure guard is inside the boundary
    if guardX >= 536:
        guardX = 536
    if guardX <= 0:
        guardX = 0

    # update the virusX
    for i in range(num_of_viruses):
        # Game over
        if virusYs[i] >= 550:
            for j in range(num_of_viruses):
                virusYs[j] = 1000
            game_over()
            break
        virusXs[i] += virusX_changes[i]
        # ensure virus is inside the boundary,
        # change the movement direction when hit the boundary and move downward
        if virusXs[i] >= 536:
            virusX_changes[i] = -0.2
            virusYs[i] += virusY_changes[i]

        if virusXs[i] <= 0:
            virusX_changes[i] = 0.2
            virusYs[i] += virusY_changes[i]

        # check collision
        collision = is_collision(virusXs[i], virusYs[i], maskX, maskY)
        if collision:
            masked_virus_sound = mixer.Sound("ahh.wav")
            masked_virus_sound.play(0)
            virus_status = "masked"
            maskedX = virusXs[i]
            maskedY = virusYs[i]
            maskY = 600
            mask_status = "ready"
            # score increase when collision
            score += 1
            print(score)
            # reset a new virus location
            virusXs[i] = random.randint(0, 536)
            virusYs[i] = random.randint(50, 150)

        # display the virus
        virus()

    # mask movement
    if maskY <= 0:
        maskY = 600
        mask_status = "ready"
    if mask_status == "fire":
        mask()
        maskY -= maskY_change

    # clock = pygame.time.Clock()
    # scale down the masked virus image
    if virus_status == "masked":
        virus_width = virus_width / 1.005
        virus_height = virus_height / 1.005
        virusImg = pygame.transform.scale(virusImg, (int(virus_width), int(virus_height)))
        masked_virus(virusImg, maskedX, maskedY)
        # when virus width is smaller than 1, reset the width, height, status and reload the fierce_virus image
        if virus_width <= 1:
            virus_width = 64
            virus_height = 64
            virus_status = "fierce"
            virusImg = pygame.image.load("fierce_virus.png")

    # display the guard
    guard()
    show_score(textX, textY)
    # update the display
    pygame.display.update()
