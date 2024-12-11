import pygame
import random

DIRECTIONS = [[1, 0], [-1, 0], [0, 1], [0, -1]]

class WalkerAlgorithm:
    def __init__(self, position, borders, tilemap):
        self.tilemap = tilemap.tilemap
        self.tilemap_asset = tilemap

        self.position = list(position)
        self.direction = DIRECTIONS[0]
        self.borders = borders
        self.step_history = set()
        self.steps_since_turn = 0

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
