import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200
DELTA = 200
FONT = pygame.font.SysFont('Verdana', 20)

COLOR_RED = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.transform.scale(pygame.image.load('pic/background.png'), (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

IMAGE_PATH = ('pic/goose')
PLAYER_IMAGES = os.listdir(IMAGE_PATH)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

PLAYER_SIZE = (120, 60)
player = pygame.transform.scale(pygame.image.load('pic/player.png'), PLAYER_SIZE)
player_rect = pygame.Rect(0, HEIGHT // 2, *PLAYER_SIZE)
speed = 4
player_move_down = [0, speed]
player_move_up = [0, -speed]
player_move_right = [speed, 0]
player_move_left = [-speed, 0]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []
def create_enemy():
    enemy_size = (60, 30)
    enemy = pygame.transform.scale(pygame.image.load('pic/enemy.png'), enemy_size)
    enemy_rect = pygame.Rect(WIDTH, random.randint(DELTA, HEIGHT - DELTA), *enemy_size)
    enemy_move = [random.randint(-5, -1), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 500)
bonuses = []
def create_bonus():
    bonus_size = (50, 90)
    bonus = pygame.transform.scale(pygame.image.load('pic/bonus.png'), bonus_size)
    bonus_rect = pygame.Rect(random.randint(DELTA, WIDTH - DELTA), 0, *bonus_size)
    bonus_move = [0, random.randint(1, 1)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ROCKET = pygame.USEREVENT + 4
pygame.time.set_timer(CREATE_ROCKET, 500)
rockets = []
def create_bonus():
    bonus_size = (50, 90)
    bonus = pygame.transform.scale(pygame.image.load('pic/bonus.png'), bonus_size)
    bonus_rect = pygame.Rect(random.randint(DELTA, WIDTH - DELTA), 0, *bonus_size)
    bonus_move = [0, random.randint(1, 1)]
    return [bonus, bonus_rect, bonus_move]

playing = True
score = 0
image_index = 0
lives_count = 3
COUNT_TIMER = pygame.USEREVENT + 3
pygame.time.set_timer(COUNT_TIMER, 100)
timer = 0

while lives_count > 0 and playing:
    FPS.tick(200)

    for event in pygame.event.get():
        if event.type == COUNT_TIMER:
            timer += 1
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index])), PLAYER_SIZE)
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
          
    bg_x1 -= bg_move
    bg_x2 -= bg_move

    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            # playing = False
            lives_count -= 1
            enemies.pop(enemies.index(enemy))
            print(lives_count)


    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))
            
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(FONT.render(str(lives_count), True, COLOR_RED), (WIDTH - 70, 20))
    main_display.blit(FONT.render(str(timer / 10), True, COLOR_BLACK), (WIDTH - 130, 20))
    main_display.blit(player, player_rect)
    
    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))