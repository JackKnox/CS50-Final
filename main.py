from scripts.game import *
from scripts.room import *
from scripts.tilemap import *
from scripts.entities import *
from scripts.algorithim import *
from scripts.ui import *

class Title(Room):
    def __init__(self, game, primary=False):
        super().__init__(game, primary)

    def update(self, delta):
        super().update(delta)
        
        txt = Text(self, "[RED]Hello, World!\n[WHITE]Hello, World![GREEN]Hello, World!")
        txt.align("MIDDLE_CENTER")
        txt.draw(self.game.width/2, self.game.height/2)

class Main(Room):
    def __init__(self, game, primary=False):
        super().__init__(game, primary)
        self.road = Tilemap(self, "Road", 320)

        WalkerAlgorithm((0, 0), pygame.Rect(0, 0, 20, 20), self.road, True).compute(20)
        CollisionPlacer("road-mask.png", self.road, self.tilemap).compute()

        Car(self, pos=(160, 160), primary=True)

class CarGame(Game):
    def __init__(self) -> None:
        super().__init__("CS50 Final", 60, (1440, 810), 3)
        
        Main(self)
        Title(self, primary=True)


CarGame().run()