import pygame
import sys

from scripts.room import Room
from scripts.entities import GameObject
from scripts.utils import load_fonts

class Game:
    def __init__(self, name, fps, size, scale):
        pygame.init()
        self.width = size[0] // scale
        self.height = size[1] // scale

        self.screen_scale = scale
        
        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode(size)
        self.display = pygame.Surface((self.width, self.height))

        self.clock = pygame.time.Clock()
        self.delta_time = 0
        
        self.current_room = None
        self.rooms = {}
        self.fonts = {}

        self.fps = fps
    
    def switch_room(self, room):
        if self.current_room:
            self.room().end()

        self.current_room = room
        self.room().__init__(self, self.room().primary)
        self.room().start()

    def room(self):
        return self.rooms[self.current_room.lower()]

    def update(self) -> None:
        self.room().update(self.delta_time)

    def render(self) -> None:
        self.room().render()

    def get_primary(self) -> Room:
        for room in self.rooms.values():
            if room.primary:
                return room

    def run(self) -> None:
        self.switch_room(self.get_primary().name)
        self.fonts = load_fonts()

        while True:
            self.delta_time = self.clock.tick(self.fps) / 1000
            self.display.fill(self.room().background_col)

            self.update()
            self.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.room().process_events(event)
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()