import pygame

class PhysicsGuy:
    def __init__(self, screen, ground_height=0, sprite=None, walk_acc=None, jump_acc=None, x_pos=None, y_pos=None):
        self.__screen = screen

        self.__sprite = pygame.image.load(sprite)

        self.__height = self.__sprite.get_height()
        self.__width = self.__sprite.get_width()

        self.__max_height = screen.get_height() - ground_height - self.__height
        self.__max_width = screen.get_width() - self.__sprite.get_width()
        self.__min_width = 0
        self.__min_height = 0

        if x_pos:
            self.__x_pos = x_pos
        else:
            self.__x_pos = 0
        if y_pos:
            self.__y_pos = y_pos
        else:
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

        self.__jump_acc = jump_acc
        self.__walk_acc = walk_acc

    def get_location(self):
        return (self.__x_pos, self.__y_pos)
    
    def get_size(self):
        return (self.__width, self.__height)
    
    def jump(self):
        if self.__on_ground():
            self.__accelerate(0, -self.__jump_acc)

    def run_right(self):
        self.__accelerate(self.__walk_acc, 0)

    def run_left(self):
        self.__accelerate(-self.__walk_acc, 0)

    def do_physics_frame(self):
        if self.__on_ground():
            self.__do_friction()
        self.__do_gravity()

        self.__acceleration_checks()
        self.__speed_up(self.__x_acc, self.__y_acc)
        self.__move(self.__x_vel, self.__y_vel)
    
    def draw(self):
        self.__screen.blit(self.__sprite, (self.__x_pos, self.__y_pos))

    def increase_max_speed(self):
        self.__max_vel *= 2

    def decrease_max_speed(self):
        self.__max_vel /= 2

    def check_collisions(self, other):
        width, height = other.get_size()
        x, y = other.get_location()

        if (abs(x - self.__x_pos) < max(self.__width, width) / 1.5) and (abs(y - self.__y_pos) < max(self.__height, height) / 1.5):
            return True
        return False
    
    def reset(self, x, y):
        self.__x_pos = x
        self.__y_pos = y
        self.__x_vel = 0
        self.__y_vel = 0
        self.__x_acc = 0
        self.__y_acc = 0

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

    def __accelerate(self, x_del, y_del):
        self.__x_acc += x_del
        self.__y_acc += y_del

    def __acceleration_checks(self):
        if self.__on_ground() and self.__y_acc > 0:
            self.__y_acc = 0
        if abs(self.__x_acc) > self.__max_acc:
            self.__x_acc = self.__max_acc * (abs(self.__x_acc) / self.__x_acc)
        if (self.__at_left_wall() and self.__x_acc < 0) or (self.__at_right_wall() and self.__x_acc > 0):
            self.__x_acc = 0

    def __speed_up(self, x_del, y_del):
        self.__x_vel += x_del
        self.__y_vel += y_del

        if self.__on_ground() and self.__y_vel > 0:
            self.__y_vel = 0
        if abs(self.__x_vel) < self.__friction / 20:
            self.__x_vel = 0
        if abs(self.__x_vel) > self.__max_vel:
            self.__x_vel = self.__max_vel * (abs(self.__x_vel) / self.__x_vel)
        if (self.__at_left_wall() and self.__x_vel < 0) or (self.__at_right_wall() and self.__x_vel > 0):
            self.__x_vel = - self.__x_vel * self.__collision_elasticity

    def __move(self, x_del, y_del):
        self.__x_pos += x_del
        self.__y_pos += y_del

        if self.__x_pos > self.__max_width:
            self.__x_pos = self.__max_width
        if self.__x_pos < self.__min_width:
            self.__x_pos = self.__min_width
        if self.__y_pos > self.__max_height:
            self.__y_pos = self.__max_height

    def __on_ground(self):
        if self.__y_pos >= self.__max_height:
            return True
        return False
    
    def __at_right_wall(self):
        if self.__x_pos >= self.__max_width:
            return True
        return False
    
    def __at_left_wall(self):
        if self.__x_pos <= self.__min_width:
            return True
        return False
    
    def __at_wall(self):
        return self.__at_left_wall() or self.__at_right_wall()
    
    def __on_screen(self):
        if self.__y_pos > self.__min_height:
            return True
        return False