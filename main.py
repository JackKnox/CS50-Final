from scripts.game import Game
from scripts.room import Room
from scripts.tilemap import Tilemap

from scripts.entities import *
from scripts.algorithim import *

class Title(Room):
    def __init__(self, game, primary=False):
        super().__init__(game, primary)

class Main(Room):
    def __init__(self, game, primary=False):
        super().__init__(game, primary)

        self.road = Tilemap(self, "Road", 320)
        WalkerAlgorithm((0, 0), pygame.Rect(0, 0, 20, 20), self.road, True).compute(20)
        CollisionPlacer(64, self.road, self.tilemaps[0]).compute()

        Car(self, pos=(160, 160), primary=True)

class CarGame(Game):
    def __init__(self) -> None:
        super().__init__("CS50 Final", 60, (1440, 810), 2)
        
        Main(self, primary=True)
        Title(self)


CarGame().run()