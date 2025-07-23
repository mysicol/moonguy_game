import os
os.system("pip install -r src/requirements.txt")

import pygame
from src.moonguy import Moonguy
from src.enemy import Enemy

width = 500
height = 500
grass_height = int(height * 0.2)

pygame.init()
rect = pygame.Rect(0, height - grass_height, width, grass_height)

screen = pygame.display.set_mode((width,height))
end_game = False

moonguy = Moonguy(screen, grass_height)

clock = pygame.time.Clock()
fps = 60

circle = pygame.image.load('src/images/moon.png')
circles = []
circle_count = 0
max_circles = 100

instructions = pygame.image.load('src/images/instructions.png')

# create enemies
enemies = [Enemy(screen, grass_height, width / 2)]
enemies.append(Enemy(screen, grass_height, width / 4))

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
                circles = []
                circle_count = 0
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
        circles.append(moonguy.get_location())
        # check if we maxed out on drawing pixels
        if circle_count > max_circles:
            circles.pop(0)
        else:
            circle_count += 1

    # advance physics for characters
    moonguy.do_physics_frame()
    for enemy in enemies:
        enemy.do_physics_frame()

    # draw background
    screen.fill((50, 50, 50))
    pygame.draw.rect(screen, (117, 91, 26), rect)

    # draw moons that guy has left
    for circle_location in circles:
        screen.blit(circle, circle_location)

    # write instructions
    screen.blit(instructions, (0, 0))

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
