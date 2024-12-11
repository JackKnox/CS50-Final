import pygame
import math

from scripts.utils import load_image

def sign(num):
    if num < 0:
        return -1
    elif num > 0:
        return 1
    else:
        return 0

class GameObject:
    def __init__(self, room, pos, primary=False):
        self.room = room
        self.pos = list(pos)
        self.rot = 0
        self.primary = primary
        self.frame_movement = [0, 0]

        self.set_sprite(load_image("car.png"))
        self.room.objects.append(self)

    def update(self, delta) -> None:
        pass

    def rect(self, x=0, y=0) -> pygame.Rect:
        rotated_spr = pygame.transform.rotate(self.spr, -(math.degrees(self.rot) + 90))
        rotated_rect = rotated_spr.get_rect(center=(self.pos[0]+x, self.pos[1]+y))
        return rotated_rect
    
    def render(self, surf, offset) -> None:
        rotated_spr = pygame.transform.rotate(self.spr, -(math.degrees(self.rot) + 90))
        rotated_rect = rotated_spr.get_rect(center=(self.pos[0] - offset[0], self.pos[1] - offset[1]))
        surf.blit(rotated_spr, rotated_rect.topleft)

    def process_events(self, event) -> None:
        pass

    def set_sprite(self, img) -> None:
        self.spr = img
        self.width = img.get_width()
        self.height = img.get_height()

class Car(GameObject):
    def __init__(self, room, pos, primary=False):
        super().__init__(room, pos, primary)

        self.wheel_base = 70
        self.steering_angle = 30
        self.engine_power = 600
        self.friction = -20     
        self.drag = -0.02       
        self.braking = -400     
        self.max_speed_reverse = 150
        self.slip_speed = 100
        self.traction_fast = 1
        self.traction_slow = 3

        self.steer_direction = 0
        
        self.acceleration = [0, 0]
        self.velocity = [0, 0]

        self.spr = load_image("car.png")

    def update(self, tilemap, delta) -> None:
        self.acceleration = [0, 0]
        self.frame_movement = [0, 0]
        self.get_input()
        self.apply_friction(delta)
        self.calculate_steering(delta)
        
        self.move_and_slide(tilemap, delta)

        super().update(delta)

    def apply_friction(self, delta) -> None:
        if self.acceleration == [0, 0] and math.hypot(*self.velocity) < 50:
            self.velocity = [0, 0]
        else:
            friction_force = [v * self.friction * delta for v in self.velocity]
            velocity_magnitude = math.hypot(*self.velocity)
            drag_force = [v * velocity_magnitude * self.drag * delta for v in self.velocity]
            self.acceleration[0] += drag_force[0] + friction_force[0]
            self.acceleration[1] += drag_force[1] + friction_force[1]
    
    def get_input(self) -> None:
        keys = pygame.key.get_pressed()
        
        turn = 0
        if keys[pygame.K_a]:
            turn -= 1
        if keys[pygame.K_d]:
            turn += 1
        
        self.steer_direction = math.radians(turn * self.steering_angle)

        if keys[pygame.K_w]:
            self.acceleration[0] = math.cos(self.rot) * self.engine_power
            self.acceleration[1] = math.sin(self.rot) * self.engine_power
        if keys[pygame.K_s]:
            self.acceleration[0] = math.cos(self.rot) * self.braking
            self.acceleration[1] = math.sin(self.rot) * self.braking
    
    def calculate_steering(self, delta) -> None:
        rear_wheel = [
            self.pos[0] - math.cos(self.rot) * self.wheel_base / 2.0,
            self.pos[1] - math.sin(self.rot) * self.wheel_base / 2.0
        ]
        front_wheel = [
            self.pos[0] + math.cos(self.rot) * self.wheel_base / 2.0,
            self.pos[1] + math.sin(self.rot) * self.wheel_base / 2.0
        ]
        
        rear_wheel[0] += self.velocity[0] * delta
        rear_wheel[1] += self.velocity[1] * delta
        
        front_velocity = [
            self.velocity[0] * math.cos(self.steer_direction) - self.velocity[1] * math.sin(self.steer_direction),
            self.velocity[0] * math.sin(self.steer_direction) + self.velocity[1] * math.cos(self.steer_direction)
        ]
        front_wheel[0] += front_velocity[0] * delta
        front_wheel[1] += front_velocity[1] * delta

        new_heading = [
            front_wheel[0] - rear_wheel[0],
            front_wheel[1] - rear_wheel[1]
        ]
        magnitude = math.hypot(*new_heading)
        if magnitude > 0:
            new_heading = [new_heading[0] / magnitude, new_heading[1] / magnitude]
        
        traction = self.traction_slow if math.hypot(*self.velocity) <= self.slip_speed else self.traction_fast
        dot_product = (new_heading[0] * self.velocity[0] + new_heading[1] * self.velocity[1]) / (math.hypot(*self.velocity) or 1)

        if dot_product > 0:
            self.velocity[0] += (new_heading[0] - self.velocity[0]) * traction * delta
            self.velocity[1] += (new_heading[1] - self.velocity[1]) * traction * delta
        elif dot_product < 0:
            speed = min(math.hypot(*self.velocity), self.max_speed_reverse)
            self.velocity = [-new_heading[0] * speed, -new_heading[1] * speed]
        
        self.rot = math.atan2(new_heading[1], new_heading[0])
    
    def move_and_slide(self, tilemap, delta) -> None:
        self.velocity[0] += self.acceleration[0] * delta
        self.velocity[1] += self.acceleration[1] * delta
        self.frame_movement[0] += self.velocity[0] * delta
        self.frame_movement[1] += self.velocity[1] * delta

        move_vector = [self.frame_movement[0], self.frame_movement[1]]
        move_magnitude = math.hypot(*move_vector)

        if move_magnitude > 0:
            move_direction = [move_vector[0] / move_magnitude, move_vector[1] / move_magnitude]
        else:
            move_direction = [0, 0]

        steps = round(move_magnitude)
        for _ in range(steps):
            step_x = move_direction[0]
            step_y = move_direction[1]
            if not self.check_collision(tilemap, step_x, step_y):
                self.pos[0] += step_x
                self.pos[1] += step_y
            else:
                self.velocity[0] = 0
                self.velocity[1] = 0
                break

        self.frame_movement = [0, 0]

    def check_collision(self, tilemap, offset_x, offset_y) -> None:
        rect = self.rect(offset_x, offset_y)
        for tile in tilemap.physics_rects_around(self.pos):
            if rect.colliderect(tile):
                return True
        return False
