from scripts.game import Game
from scripts.room import Room
from scripts.entities import *

from scripts.algorithim import WalkerAlgorithm

class Title(Room):
    def __init__(self, game, primary=False):
        super().__init__(game, primary)

class Main(Room):
    def __init__(self, game, primary=False):
        super().__init__(game, primary)
        self.tilemap.load("Road", 320)
        WalkerAlgorithm((1, 1), pygame.Rect(1, 1, 20, 20), self.tilemap).compute(20)

        Car(self, pos=(0, 0), primary=True)

class CarGame(Game):
    def __init__(self) -> None:
        super().__init__("CS50 Final", 60, (1440, 810), 1)
        
        Main(self, primary=True)
        Title(self)


CarGame().run()