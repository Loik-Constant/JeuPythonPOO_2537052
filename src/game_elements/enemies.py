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
            taille: int = 40,
            image: str = 'images/isook.png',
            limites: tuple[int, int] = (800, 600),
            health: int = 0
    ):
        super().__init__(x, y, taille, image, limites)
        self.health = health

    def take_damage(self, damage : int) -> None:
        self.health -= damage

        if self.health <= 0:
            self.kill()




