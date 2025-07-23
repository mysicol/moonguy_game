import os
os.system("pip install -r src/requirements.txt")

import pygame
import random
from src.guys import Enemy, Moonguy, Moon
from src.timers import EventTimer, IntervalEvent

# initialize pygame environment
pygame.init()

# font settings
pygame.font.init()
health_font = pygame.font.SysFont('Monospace', 15)

# create screen
width = 250
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
max_moons = 20

# load instructions
instructions = pygame.image.load('src/images/instructions.png')

# create moonguy
moonguy = Moonguy(screen, grass_height)

# create list for timed events
events = []

failure_display = health_font.render('FAILURE.', True, (250, 250, 250))
reset_display = health_font.render('RESET', True, (250, 250, 250))

health = None
score = None
moons = None
enemies = None
moon_count = None

def reset():
    global health, score, moons, enemies, moon_count
    health = 100
    score = 0
    moons = []
    moon_count = 0
    enemies = []
    moonguy.reset(0, height)

def show_controls():
    start_pos = 100
    spacing = 15
    screen.blit(health_font.render('controls.', True, (250, 250, 250)), (10, height / 2 - start_pos))
    screen.blit(health_font.render('arrows - move', True, (250, 250, 250)), (20, height / 2 - start_pos + spacing))
    screen.blit(health_font.render('c      - moon trail', True, (250, 250, 250)), (20, height / 2 - start_pos + (spacing * 2)))
    screen.blit(health_font.render('x      - clear moons', True, (250, 250, 250)), (20, height / 2 - start_pos + (spacing * 3)))
    screen.blit(health_font.render('v      - spawn enemy', True, (250, 250, 250)), (20, height / 2 - start_pos + (spacing * 4)))
    screen.blit(health_font.render('r      - reset', True, (250, 250, 250)), (20, height / 2 - start_pos + (spacing * 5)))
    screen.blit(health_font.render('Shift  - run', True, (250, 250, 250)), (20, height / 2 - start_pos + (spacing * 6)))
    screen.blit(health_font.render('esc    - quit', True, (250, 250, 250)), (20, height / 2 - start_pos + (spacing * 7)))

def decrement_score():
    global score
    score -= 1

reset()

# create enemy to start
enemies.append(Enemy(screen, grass_height, width / 2))

# add score decrement timer
events.append(IntervalEvent(0.5, decrement_score, "score_decrement", repeat=True))

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
            if (event.key == pygame.K_v):
                enemies.append(Enemy(screen, grass_height, random.random() * width))
            # reset
            if event.key == pygame.K_r:
                events.append(EventTimer(3, lambda: screen.blit(reset_display, (width / 2 - reset_display.get_width() / 2, height / 2)), "center_screen"))
                reset()
        # leave running mode
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LSHIFT):
                moonguy.decrease_max_speed()

    if health <= 0:
        events.append(EventTimer(3, lambda: screen.blit(failure_display, (width / 2 - failure_display.get_width() / 2, height / 2)), "center_screen"))
        reset()

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
            health -= 5
            score -= 10

        # check for enemy collisions with moons
        for moon in moons:
            if enemy.check_collisions(moon):
                enemies.remove(enemy)
                score += 50
                break

    # check for moonguy collisions with moons
    # for moon in moons:
    #     if moonguy.check_collisions(moon):
    #         score -= 2

    # draw background
    screen.fill((50, 50, 50))
    pygame.draw.rect(screen, (117, 91, 26), ground)

    # write stats
    health_display = health_font.render('health: ' + str(health), True, (250, 250, 250))
    score_display = health_font.render('score: ' + str(score), True, (250, 250, 250))
    screen.blit(health_display, (width - 110, 10))
    screen.blit(score_display, (width - 110, 20))

    # show help message
    if keys[pygame.K_h]:
        events.append(EventTimer(0.25, show_controls, "center_screen"))

    # timed events
    for event in events:
        for event_2 in events:
            if event != event_2 and event.get_type() == event_2.get_type():
                events.remove(event)
        if event.done():
            events.remove(event)

    # draw moons that guy has left
    for moon in moons:
        moon.draw()

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
