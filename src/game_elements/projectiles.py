import math
import random

import pygame

from game_elements.game_element import GameElement

class Projectile(GameElement):
    def __init__(
            self,
            x: float,
            y: float,
            size: int = 25,
            image_file: str = 'images/tear.png',
            limits: tuple[int, int] = (1100, 600),
            speed: float = 30.0,
            angle: float = 0,
            damage: int = 0
    ):
        super().__init__(x, y, size, image_file, limits)
        self.speed = speed
        self.angle = angle
        self.damage = damage

        self.image = pygame.transform.rotate(self.image, random.randint(0, 360))

        self.vx = math.cos(math.radians(angle))
        self.vy = math.sin(math.radians(angle))

    def update(self) -> None:
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

        self.destroy_offscreen()
        self.rect.center = (int(self.x), int(self.y))
