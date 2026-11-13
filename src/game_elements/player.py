import math

from game_elements.game_element import GameElement

import pygame

class Player(GameElement):
    """Représente le carré contrôlé par l'utilisateur au clavier."""

    def __init__(
            self,
            x: float,
            y: float,
            taille: int = 50,
            couleur: tuple[int, int, int] = (70, 130, 180),
            limites: tuple[int, int] = (800, 600),
            vitesse: float = 30.0,
    ):
        super().__init__(x, y, taille, couleur, limites)
        self.vitesse = vitesse

    def mise_a_jour(self) -> None:
        """Met à jour la position du joueur en fonction des touches pressées."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= self.size / 2
        mouse_y -= self.size / 2

        direction = pygame.math.Vector2(mouse_x - self.x, mouse_y - self.y)
        if direction.length() > 0:
            direction = direction.normalize()

        if self.x <= mouse_x:
            self.x += min(direction.x * self.vitesse, mouse_x - self.x)
        else:
            self.x += max(direction.x * self.vitesse, mouse_x - self.x)

        if self.y <= mouse_y:
            self.y += min(direction.y * self.vitesse, mouse_y - self.y)
        else:
            self.y += max(direction.y * self.vitesse, mouse_y - self.y)

        self.restreindre_a_ecran()