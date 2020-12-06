import pygame
import random
import Client.game_objects as go

CELL = 10
WIDTH = 80
HEIGHT = 60
FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH * CELL, HEIGHT * CELL))
clock = pygame.time.Clock()
running = True


def GenerateField(width, height):
    field = []
    for x in range(width):
        field.append([])
        for y in range(height):
            field[x].append(go.Air)
    return field


def GenerateDirt(field, count):
    while count != 0:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if field[x][y] != go.Dirt:
            field[x][y] = go.Dirt
            count -= 1
    return field


def GenerateRock(field, step):
    for x in range(step - 1, WIDTH, step):
        for y in range(step - 1, HEIGHT, step):
            field[x][y] = go.Rock
    return field

def EmptyStart(field, x=0, y=0, radius=3):
    x_start = 0 if (x - radius) < 0 else x - radius
    y_start = 0 if (y - radius) < 0 else y - radius
    x_end = (x + radius) % len(field)
    y_end = (y + radius) % len(field[0])
    for i in range(x_start, x_end + 1):
        for j in range(y_start, y_end + 1):
            if field[i][j] == go.Dirt:
                field[i][j] = go.Air
    return field

def CheckMove(player, field, shift_x, shift_y):
    if player.x == 0 and shift_x < 0 or \
        player.x == len(field) - 1 and shift_x > 0 or \
        player.y == 0 and shift_y < 0 or \
        player.y == len(field[0]) - 1 and shift_y > 0:
        return False
    if field[player.x + shift_x][player.y + shift_y] != go.Air:
        return False
    return True

def GenerateFire(field, x, y, radius=2):
    x_start = 0 if (x - radius) < 0 else x - radius
    y_start = 0 if (y - radius) < 0 else y - radius
    x_end = (x + radius) % len(field)
    y_end = (y + radius) % len(field[0])
    for i in range(x_start, x_end + 1):
        field[i][y] = go.Fire()
    for j in range(y_start, y_end + 1):
        field[x][j] = go.Fire()
    return field

field = EmptyStart(GenerateRock(GenerateDirt(GenerateField(WIDTH, HEIGHT), 2500), 3))
player = go.Player(0, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if CheckMove(player, field, 0, -1):
                    player.y -= 1
            if event.key == pygame.K_s:
                if CheckMove(player, field, 0, 1):
                    player.y += 1
            if event.key == pygame.K_a:
                if CheckMove(player, field, -1, 0):
                    player.x -= 1
            if event.key == pygame.K_d:
                if CheckMove(player, field, 1, 0):
                    player.x += 1
            if event.key == pygame.K_SPACE:
                field[player.x][player.y] = go.Bomb()


    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isinstance(field[x][y], go.Bomb):
                if field[x][y].tick():
                    field = GenerateFire(field, x, y)
            if isinstance(field[x][y], go.Fire):
                if field[x][y].tick():
                    field[x][y] = go.Air
            pygame.draw.rect(screen, field[x][y].color, (CELL * x, CELL * y, CELL, CELL))
    pygame.draw.rect(screen, player.color, (CELL * player.x, CELL * player.y, CELL, CELL))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
