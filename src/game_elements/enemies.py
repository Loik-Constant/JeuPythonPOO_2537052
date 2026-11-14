import random
import sys
from abc import abstractmethod

import pygame

from game_elements.game_element import GameElement


class Enemy(GameElement):
    """Représente un ennemi pouvant blesser le joueur."""

    def __init__(
            self,
            x: float,
            y: float,
            size: int = 40,
            image: str = 'images/isook.png',
            limits: tuple[int, int] = (800, 600),
            health: int = 3
    ):
        super().__init__(x, y, size, image, limits)
        self.health = health

    def take_damage(self, damage : int) -> None:
        self.health -= damage

        if self.health <= 0:
            self.kill()