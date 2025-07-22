import pygame

class Moonguy:
    def __init__(self, screen, ground_height):
        self.__screen = screen

        self.__sprite = pygame.image.load('moonguy.png')

        self.__height = self.__sprite.get_height()
        self.__width = self.__sprite.get_width()

        self.__max_height = screen.get_height() - ground_height - self.__height
        self.__max_width = screen.get_width() - self.__sprite.get_width()
        self.__min_width = 0
        self.__min_height = 0

        self.__x_pos = 0
        self.__y_pos = self.__max_height

        self.__x_vel = 0
        self.__y_vel = 0

        self.__x_acc = 0
        self.__y_acc = 0

        self.__max_vel = 5
        self.__max_acc = self.__max_vel / 5

        self.__friction = 0.1
        self.__gravity = 0.2

        self.__stopping = False

        self.__collision_elasticity = 0.8

    def do_physics_frame(self):
        if self.on_ground():
            self.__do_friction()
        self.__do_gravity()

        self.__acceleration_checks()
        self.__speed_up(self.__x_acc, self.__y_acc)
        self.__move(self.__x_vel, self.__y_vel)

    def __do_friction(self):
        if abs(self.__x_acc) > self.__friction:
            self.__stopping = False
            if self.__x_acc > 0:
                self.__x_acc -= self.__friction
            elif self.__x_acc < 0:
                self.__x_acc += self.__friction
        else:
            self.__stopping = True
        if self.__stopping:
            self.__x_acc = 0
            self.__x_vel /= 10

    def __do_gravity(self):
        if self.__y_acc < 0:
            self.__y_acc += self.__gravity

    def accelerate(self, x_del, y_del):
        self.__x_acc += x_del
        self.__y_acc += y_del

    def __acceleration_checks(self):
        if self.on_ground() and self.__y_acc > 0:
            self.__y_acc = 0
        if abs(self.__x_acc) > self.__max_acc:
            self.__x_acc = self.__max_acc * (abs(self.__x_acc) / self.__x_acc)
        if (self.at_left_wall() and self.__x_acc < 0) or (self.at_right_wall() and self.__x_acc > 0):
            self.__x_acc = 0

    def __speed_up(self, x_del, y_del):
        self.__x_vel += x_del
        self.__y_vel += y_del

        if self.on_ground() and self.__y_vel > 0:
            self.__y_vel = 0
        if abs(self.__x_vel) < self.__friction / 20:
            self.__x_vel = 0
        if abs(self.__x_vel) > self.__max_vel:
            self.__x_vel = self.__max_vel * (abs(self.__x_vel) / self.__x_vel)
        if (self.at_left_wall() and self.__x_vel < 0) or (self.at_right_wall() and self.__x_vel > 0):
            self.__x_vel = - self.__x_vel * self.__collision_elasticity

    def __move(self, x_del, y_del):
        self.__x_pos += x_del
        self.__y_pos += y_del

        if self.__x_pos > self.__max_width:
            self.__x_pos = self.__max_width
        if self.__x_pos < self.__min_width:
            self.__x_pos = self.__min_width

    def appear(self):
        self.__screen.blit(self.__sprite, (self.__x_pos, self.__y_pos))

    def on_ground(self):
        if self.__y_pos >= self.__max_height:
            return True
        return False
    
    def at_right_wall(self):
        if self.__x_pos >= self.__max_width:
            return True
        return False
    
    def at_left_wall(self):
        if self.__x_pos <= self.__min_width:
            return True
        return False
    
    def at_wall(self):
        return self.at_left_wall() or self.at_right_wall()
    
    def on_screen(self):
        if self.__y_pos > self.__min_height:
            return True
        return False