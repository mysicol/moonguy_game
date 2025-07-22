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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            end_game = True
            break
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
            if moonguy.on_ground():
                moonguy.accelerate(0, -2)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        moonguy.accelerate(0.3, 0)
    if keys[pygame.K_LEFT]:
        moonguy.accelerate(-0.3, 0)
    
    screen.fill((50, 50, 50))
    pygame.draw.rect(screen, (117, 91, 26), rect)

    moonguy.do_physics_frame()
    moonguy.appear()

    if end_game:
        break

    pygame.display.flip()

    clock.tick(fps)

pygame.quit()
