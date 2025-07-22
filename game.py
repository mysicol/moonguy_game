import pygame
from moonguy import Moonguy

width = 250
height = 500
grass_height = int(height * 0.2)

pygame.init()
rect = pygame.Rect(0, height - grass_height, width, grass_height)

screen = pygame.display.set_mode((width,height))
end_game = False

moonguy = Moonguy(screen, grass_height)

clock = pygame.time.Clock()
fps = 60

circle = pygame.image.load('images/moon.png')
circles = []
circle_count = 0
max_circles = 100

instructions = pygame.image.load('images/instructions.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            end_game = True
            break
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP):
                moonguy.jump()
            if (event.key == pygame.K_x):
                circles = []
                circle_count = 0
            if (event.key == pygame.K_LSHIFT):
                moonguy.increase_max_speed()
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LSHIFT):
                moonguy.decrease_max_speed()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        moonguy.run_right()
    if keys[pygame.K_LEFT]:
        moonguy.run_left()
    if keys[pygame.K_c]:
        circles.append(moonguy.get_location())
        if circle_count > max_circles:
            circles.pop(0)
        else:
            circle_count += 1

    moonguy.do_physics_frame()

    screen.fill((50, 50, 50))
    pygame.draw.rect(screen, (117, 91, 26), rect)

    for circle_location in circles:
        screen.blit(circle, circle_location)

    screen.blit(instructions, (0, 0))

    moonguy.draw()

    if end_game:
        break

    pygame.display.flip()

    clock.tick(fps)

pygame.quit()
