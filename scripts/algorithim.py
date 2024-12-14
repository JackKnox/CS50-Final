import pygame
import random

from scripts.utils import *

#            left     right    down    up
DIRECTIONS = [[1, 0], [-1, 0], [0, 1], [0, -1]]

class WalkerAlgorithm:
    def __init__(self, position, borders, tilemap, autotile):
        self.tilemap = tilemap.tilemap
        self.tilemap_asset = tilemap

        self.position = list(position)
        self.direction = DIRECTIONS[0]
        self.borders = borders
        self.step_history = set()
        self.steps_since_turn = 0
        self.autotile = autotile

        self.step_history.add(tuple(position))

    def compute(self, steps) -> list:
        for _ in range(steps):
            if random.random() <= 0.1 or self.steps_since_turn >= 8:
                self.change_direction()

            if self.step():
                self.step_history.add(tuple(self.position))
            else:
                self.change_direction()

        history = list(self.step_history)
        for location in history:
            x = location[0] 
            y = location[1]
            self.tilemap_asset.set(x, y, "road")
        
        if self.autotile:
            self.tilemap_asset.autotile()
        
        return history

    def step(self) -> bool:
        target_position = [self.position[0] + self.direction[0], self.position[1] + self.direction[1]]

        if self.borders.collidepoint(target_position) and tuple(target_position) not in self.step_history:
            self.steps_since_turn += 1
            self.position = target_position
            return True
        else:
            return False

    def change_direction(self) -> None:
        self.steps_since_turn = 0
        directions = DIRECTIONS.copy()
        directions.remove(self.direction)
        random.shuffle(directions)

        for new_direction in directions:
            target_position = [self.position[0] + new_direction[0], self.position[1] + new_direction[1]]
            if self.borders.collidepoint(target_position):
                self.direction = new_direction
                return
        
        self.direction = DIRECTIONS[0]

class CollisionPlacer:
    def __init__(self, mask, tilemap, collimap):
        self.img = load_image(mask)
        self.tilemap = tilemap
        self.collimap = collimap
        self.tile_size = self.tilemap.tile_size
        self.scale_factor = self.tilemap.tile_size // self.collimap.tile_size

        self.wall_color = (255, 0, 0, 255)
        self.empty_color = (0, 255, 0, 255)

    def compute(self):
        for tile in self.tilemap.values():
            variant = tile["variant"]
            mask_x = variant * self.scale_factor
            mask_y = 0

            tile_x = (tile["pos"][0] * self.tile_size) // self.collimap.tile_size            
            tile_y = (tile["pos"][1] * self.tile_size) // self.collimap.tile_size

            for i in range(self.scale_factor):
                for j in range(self.scale_factor):
                    pixel = self.img.get_at((mask_x+i, mask_y+j))

                    if pixel == self.wall_color:
                        self.collimap.set(tile_x+i, tile_y+j, type="test")
