import pygame
from src.physicsguy import PhysicsGuy
import random
import time

class Enemy(PhysicsGuy):
    def __init__(self, screen, grass_height, x_pos):
        super().__init__(screen, grass_height, x_pos, 'src/images/enemy.png', 11, 1.5)
        
        self.__action_cooldown = 3
        self.__action_start = time.time() - random.random() * self.__action_cooldown

    def choose_action(self):
        if (time.time() - self.__action_start > self.__action_cooldown):
            choice = random.randint(1, 3)
            match choice:
                case 1:
                    self.jump()
                case 2:
                    self.run_left()
                case 3:
                    self.run_right()
            self.__action_start = time.time()