import pygame
from src.physicsguy import PhysicsGuy
import random
import time

class Moonguy(PhysicsGuy):
    def __init__(self, screen, ground_height):
        super().__init__(screen, ground_height=ground_height, sprite='src/images/moonguy.png', walk_acc=0.3, jump_acc=2)

class Enemy(PhysicsGuy):
    def __init__(self, screen, ground_height, x_pos):
        super().__init__(screen, ground_height=ground_height, x_pos=x_pos, sprite='src/images/enemy.png', walk_acc=11, jump_acc=1.5)
        
        self.__action_cooldown = 1
        self.__action_start = time.time() - random.random() * self.__action_cooldown

    def choose_action(self):
        if (time.time() - self.__action_start > self.__action_cooldown):
            choice = random.randint(1, 4)
            if choice < 3:
                self.jump()
            elif choice < 4:
                self.run_left()
            else:
                self.run_right()
            self.__action_start = time.time()

class Moon(PhysicsGuy):
    def __init__(self, screen, position):
        x, y = position
        super().__init__(screen, sprite='src/images/moon.png', x_pos=x, y_pos=y)