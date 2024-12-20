import sys

from scripts.game import *
from scripts.room import *
from scripts.tilemap import *
from scripts.entities import *
from scripts.algorithim import *
from scripts.ui import *

def mix_colors(*colors: object) -> tuple:
    num_colors = len(colors)
    
    summed_color = [0, 0, 0]
    for color in colors:
        for i in range(3):
            summed_color[i] += color[i]
    
    return tuple(s // num_colors for s in summed_color)

class Title(Room):
    def __init__(self, game, primary=False):
        super().__init__(game, primary)
        self.background_col = mix_colors(PALETTE_PURPLE, PALETTE_WHITE)

    def update(self, delta):
        super().update(delta)

        cont = Container(self, [
            Text(self, "CS50 Final!"),
            CONTAINER_SPACE,
            Button(self, "Start Game!", onclick=lambda self: self.game.switch_room("Main")),
            Button(self, "Quit Game!", onclick=lambda self: sys.exit()),
        ])
        cont.starting_format("main-font", PALETTE_WHITE)
        cont.align(MIDDLE_CENTER)
        cont.draw(self.game.width/2, self.game.height/2)

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