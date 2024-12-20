import pygame
from math import floor

from scripts.tilemap import Tilemap
from scripts.entities import GameObject

MAIN_STATE = "main"

class Room:
    def __init__(self, game, primary=False):
        self.game = game
        self.primary = primary

        self.name = type(self).__name__.lower()
        self.game.rooms[self.name] = self
        
        self.tilemaps = []
        self.tilemap = Tilemap(self, tile_size=32)

        self.objects = []
        self.scroll = [0, 0]
        self.background_col = (0, 0, 0)
        self.state = MAIN_STATE
        self.paused = False

    def set_state(self, state, pause=False):
        self.state = state
        self.paused = pause

    def update(self, delta) -> None:
        if self.state == MAIN_STATE:
            if self.get_primary():
                primary = self.get_primary()
                followx = primary.rect().centerx
                followy = primary.rect().centery

                self.scroll[0] += (followx - self.game.display.get_width() / 2 - self.scroll[0]) / 10
                self.scroll[1] += (followy - self.game.display.get_height() / 2 - self.scroll[1]) / 10
            
            for obj in self.objects:
                obj.update(self.tilemaps[0], delta)
        
        if hasattr(self, self.state + "_update"):
            state_update = getattr(self, self.state + "_update")
            state_update()

    def render(self) -> None:
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        for tilemap in self.tilemaps:
            tilemap.render(self.game.display, offset=render_scroll)

        for obj in self.objects:
            obj.render(self.game.display, offset=render_scroll)

        if self.paused:
            surf = pygame.Surface((self.game.width, self.game.height))
            surf.fill((0, 0, 0))
            surf.set_alpha(127.5)
            self.game.display.blit(surf, (0, 0))

        if hasattr(self, self.state + "_render"):
            state_update = getattr(self, self.state + "_render")
            state_update()

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
        
        self.start_time = pygame.time.get_ticks()

    def end(self) -> None:
        pass 