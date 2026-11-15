import random
import sys
from abc import abstractmethod

import pygame

from game_elements.game_element import GameElement


class Enemy(GameElement):
    """Représente un ennemi pouvant blesser le joueur."""

    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            size: int = 40,
            image_file: str = 'images/isook.png',
            limits: tuple[int, int] = (1100, 600),
            health: int = 3
    ):
        super().__init__(x, y, size, image_file, limits)
        self.health = health

    def copy(self) -> "Enemy":
        """Retourne une copie de l'ennemi"""
        return Enemy(
            self.x,
            self.y,
            self.size,
            self.image_file,
            self.limits,
            self.health
        )

    def take_damage(self) -> None:
        """Réduit les points de vie de l'ennemi"""
        self.health -= 1

        if self.health <= 0:
            self.kill()

    def update(self):
        """Met à jour la position de l'ennemi'."""
        self.rect.topleft = (int(self.x), int(self.y))