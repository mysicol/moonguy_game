from src.physicsguy import PhysicsGuy

class Moonguy(PhysicsGuy):
    def __init__(self, screen, ground_height):
        super().__init__(screen, ground_height, 0, 'src/images/moonguy.png', 0.3, 2)