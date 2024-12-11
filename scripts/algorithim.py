import pygame
import random

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
    def __init__(self, length, tilemap, collimap):
        self.len = length
        self.tilemap = tilemap
        self.collimap = tilemap

        self.base = []

        tile_size = self.tilemap.tile_size

        self.base.append([pygame.Rect(0, length, tile_size-length, tile_size - length*2)  , [[None] * tile_size] * tile_size]) # left
        self.base.append([pygame.Rect(length, length, tile_size-length, tile_size - length*2), [[None] * tile_size] * tile_size]) # right
        self.base.append([pygame.Rect(0, length, tile_size - length*2, tile_size-length)  , [[None] * tile_size] * tile_size]) # up
        self.base.append([pygame.Rect(length, length, tile_size - length*2, tile_size-length), [[None] * tile_size] * tile_size]) # down
        
        for rect, walls in self.base:
            for x in range(len(walls)):
                for y in range(len(walls[x])):
                    if (x == rect.left-1 or x == rect.right+1 - 1 or y == rect.top-1 or y == rect.bottom+1):
                        walls[x][y] = True
                    else:
                        walls[x][y] = False

    def compute(self):
        for tile in self.tilemap.tilemap.values():
            print(tile)

    def get_tile_neighbours(self, value):
        neighbours = []

        if value & 2:
            neighbours.append(DIRECTIONS[0])
        if value & 4:
            neighbours.append(DIRECTIONS[2])
        if value & 8:
            neighbours.append(DIRECTIONS[1])
        if value & 16:
            neighbours.append(DIRECTIONS[3])
        
        return neighbours