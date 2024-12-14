import pygame

from scripts.utils import load_images
from scripts.algorithim import WalkerAlgorithm

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

class Tilemap:
    def __init__(self, game, spr="test", tile_size=32):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.spr = load_images("tiles/" + spr.lower())
        self.offset = [0, 0]
        self.autotile_values = {}

        self.game.tilemaps.append(self)
    
    def values(self):
        return self.tilemap.values()

    def load(self, type, size):
        self.spr = load_images("tiles/" + type.lower())
        self.tile_size = size

    def get_tile(self, type, x, y):
        return self.tilemap.get((x, y), {}).get("type") == type

    def calculate_tile_variant(self, type, x, y):
        value = 1

        if self.get_tile(type, x, y - 1): value += 1
        if self.get_tile(type, x, y + 1): value += 4
        if self.get_tile(type, x - 1, y): value += 8
        if self.get_tile(type, x + 1, y): value += 2

        return value
    
    def set(self, x, y, type, variant=1):
        self.tilemap[(x, y)] = {'type': type, 'variant': variant, 'pos': (x, y)}

    def autotile(self):
        updated = set()
        for (x, y), tile in self.tilemap.items():
            if (x, y) not in updated:
                type = tile["type"]

                variant = self.calculate_tile_variant(type, x, y)
                self.set(x, y, type, variant)
                updated.add((x, y))

                for neighbor in self.tiles_around((x, y)):
                    nx, ny = neighbor["pos"]
                    if (nx, ny) not in updated:
                        neighbor["variant"] = self.calculate_tile_variant(type, nx, ny)
                        updated.add((nx, ny))

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = (tile_loc[0] + offset[0], tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            rects.append(pygame.Rect(tile['pos'][0] * self.tile_size + self.offset[0], tile['pos'][1] * self.tile_size + self.offset[1], self.tile_size, self.tile_size))
        return rects

    def render(self, surf, offset=(0, 0)) -> None:
        # TODO: Preblit static tiles (dirty flag)
        effective_offset = (offset[0] - self.offset[0], offset[1] - self.offset[1])

        x_start = max(0, offset[0] // self.tile_size)
        y_start = max(0, offset[1] // self.tile_size)
        x_end = (offset[0] + surf.get_width()) // self.tile_size + 1
        y_end = (offset[1] + surf.get_height()) // self.tile_size + 1

        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                tile = self.tilemap.get((x, y))
                if tile:
                    surf.blit(self.spr[tile['variant']], (
                        tile['pos'][0] * self.tile_size - effective_offset[0],
                        tile['pos'][1] * self.tile_size - effective_offset[1]
                    ))