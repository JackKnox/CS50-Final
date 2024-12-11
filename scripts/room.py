from scripts.tilemap import Tilemap
from scripts.entities import GameObject

class Room:
    def __init__(self, game, primary=False):
        self.game = game
        self.primary = primary
        self.font = self.game.font

        self.name = type(self).__name__.lower()
        self.game.rooms[self.name] = self
        
        self.tilemap = Tilemap(self)

        self.objects = []
        self.scroll = [0, 0]

    def update(self, delta) -> None:
        if self.get_primary():
            primary = self.get_primary()
            followx = primary.rect().centerx
            followy = primary.rect().centery

            self.scroll[0] += (followx - self.game.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (followy - self.game.display.get_height() / 2 - self.scroll[1]) / 30
        
        for obj in self.objects:
            obj.update(self.tilemap, delta)

    def render(self) -> None:
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
        self.tilemap.render(self.game.display, offset=render_scroll)

        for obj in self.objects:
            obj.render(self.game.display, offset=render_scroll)

    def get_primary(self) -> GameObject:
        for obj in self.objects:
            if obj.primary:
                return obj
    
    def process_events(self, event):
        for obj in self.objects:
            obj.process_events(event)


    def start(self) -> None:
        if self.get_primary():
            primary = self.get_primary()
            followx = primary.rect().centerx
            followy = primary.rect().centery

            self.scroll[0] = (followx - self.game.display.get_width() / 2 - self.scroll[0]) 
            self.scroll[1] = (followy - self.game.display.get_height() / 2 - self.scroll[1])

    def end(self) -> None:
        pass 