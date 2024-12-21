import sys

from scripts.game import *
from scripts.room import *
from scripts.tilemap import *
from scripts.entities import *
from scripts.algorithim import *
from scripts.ui import *

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
            Button(self, "Quit Game!", onclick=lambda: sys.exit()),
        ])
        cont.starting_format("main-font", PALETTE_WHITE)
        cont.align(MIDDLE_CENTER)
        cont.draw(self.game.width/2, self.game.height/2)

class Main(Room):
    def __init__(self, game, primary=False):
        super().__init__(game, primary)
        self.road = Tilemap(self, "Road", 320)

        self.checkpoint = WalkerAlgorithm((0, 0), pygame.Rect(0, 0, 20, 20), self.road, True).compute(20).get_end()
        CollisionPlacer("road-mask.png", self.road, self.tilemap).compute()
        
        Car(self, pos=(160, 160), primary=True)

    def main_update(self):
        # Enter finish race
        if self.checkpoint.colliderect(self.get_primary().rect()):
            self.set_state("finish_race", pause=True)
            self.elapsed_time = pygame.time.get_ticks() - self.start_time

    def finish_race_render(self):
        minutes = self.elapsed_time // (1000 * 60)
        seconds = (self.elapsed_time // 1000) % 60

        if self.game.high_score < (minutes * 60 + seconds):
            self.game.high_score = (minutes * 60 + seconds)

        cont = Container(self, [
            Text(self, f"Time: {minutes:02}:{seconds:02}"),
            Text(self, f"High Score: {self.game.high_score // 60:02}:{self.game.high_score % 60:02}"),
            CONTAINER_SPACE,
            Button(self, "Restart!", onclick=lambda self: self.game.switch_room("Main"))
        ])
        cont.starting_format("main-font", PALETTE_WHITE)
        cont.align(MIDDLE_CENTER)
        cont.draw(self.game.width/2, self.game.height/2)

    def countdown_update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 1000:
            self.timer -= 1
            self.start_time = current_time

        if self.timer <= 0:
            self.set_state(MAIN_STATE)

    def countdown_render(self):
        text = Text(self, self.timer)
        text.starting_format("main-font", PALETTE_WHITE)
        text.align(MIDDLE_CENTER)
        text.scale(2)
        text.draw(self.game.width/2, self.game.height/2)

    def start(self):
        super().start()
        
        # Enter countdown
        self.timer = 3
        self.set_state("countdown", pause=True)

class CarGame(Game):
    def __init__(self) -> None:
        super().__init__("CS50 Final", 60, (1440, 810), 3)
        self.high_score = 0
        
        Main(self)
        Title(self, primary=True)

CarGame().run()