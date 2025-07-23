import os
os.system("pip install -r src/requirements.txt")

import pygame
from src.guys import Enemy, Moonguy, Moon

# initialize pygame environment
pygame.init()

# font settings
pygame.font.init()
health_font = pygame.font.SysFont('Monospace', 15)

# create screen
width = 500
height = 500
screen = pygame.display.set_mode((width,height))

# create ground
grass_height = int(height * 0.2)
ground = pygame.Rect(0, height - grass_height, width, grass_height)

# game state settings
clock = pygame.time.Clock()
end_game = False
fps = 60

# drawing settings
moons = []
moon_count = 0
max_moons = 100

# load instructions
instructions = pygame.image.load('src/images/instructions.png')

# create moonguy
moonguy = Moonguy(screen, grass_height)

# create enemies
enemies = [Enemy(screen, grass_height, width / 2)]
enemies.append(Enemy(screen, grass_height, width / 4))

# health init
health = 100

while True:
    for event in pygame.event.get():
        # check for quit
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            end_game = True
            break
        # button press events
        if event.type == pygame.KEYDOWN:
            # jump
            if (event.key == pygame.K_UP):
                moonguy.jump()
            # clear drawing
            if (event.key == pygame.K_x):
                moons = []
                moon_count = 0
            # enter running mode
            if (event.key == pygame.K_LSHIFT):
                moonguy.increase_max_speed()
        # leave running mode
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LSHIFT):
                moonguy.decrease_max_speed()

    # check for quitting
    if end_game:
        break

    # button hold events
    keys = pygame.key.get_pressed()
    # right
    if keys[pygame.K_RIGHT]:
        moonguy.run_right()
    # left
    if keys[pygame.K_LEFT]:
        moonguy.run_left()
    # draw
    if keys[pygame.K_c]:
        moons.append(Moon(screen, moonguy.get_location()))
        # check if we maxed out on drawing pixels
        if moon_count > max_moons:
            moons.pop(0)
        else:
            moon_count += 1

    # advance physics for characters
    moonguy.do_physics_frame()
    for enemy in enemies:
        enemy.do_physics_frame()

        # check for moonguy collisions with enemy
        if moonguy.check_collisions(enemy):
            health -= 3

        # check for enemy collisions with moons
        for moon in moons:
            if enemy.check_collisions(moon):
                enemies.remove(enemy)
                break

    # draw background
    screen.fill((50, 50, 50))
    pygame.draw.rect(screen, (117, 91, 26), ground)

    # draw moons that guy has left
    for moon in moons:
        moon.draw()

    # write instructions
    screen.blit(instructions, (0, 0))

    # write health
    health_display = health_font.render('health: ' + str(health), True, (250, 250, 250))
    screen.blit(health_display, (width - width / 5, 10))

    # draw enemies
    for enemy in enemies:
        enemy.choose_action()
        enemy.draw()

    # draw moonguy
    moonguy.draw()

    # update display
    pygame.display.flip()

    # ensure correct fps
    clock.tick(fps)

pygame.quit()
