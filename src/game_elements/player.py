from game_elements.game_element import GameElement

import pygame

from game_elements.projectiles import Projectile


class Player(GameElement):
    """Représente le carré contrôlé par l'utilisateur au clavier."""

    def __init__(
            self,
            x: int,
            y: int,
            size: int = 50,
            image_file: str = 'images/isook.png',
            limits: tuple[int, int] = (1100, 600),
            speed: float = 30.0,
            fire_interval: int = 10
    ):
        super().__init__(x, y, size, image_file, limits)
        self.speed = speed
        self.fire_interval = fire_interval
        self.counter = 1

    def update(self) -> None:
        """Met à jour la position du joueur en fonction de la position de la souris."""
        mouse_x, mouse_y = pygame.mouse.get_pos()

        direction = pygame.math.Vector2(mouse_x - self.x, mouse_y - self.y)
        if direction.length() > 0:
            direction = direction.normalize()

        if self.x <= mouse_x:
            self.x += min(direction.x * self.speed, mouse_x - self.x)
        else:
            self.x += max(direction.x * self.speed, mouse_x - self.x)

        if self.y <= mouse_y:
            self.y += min(direction.y * self.speed, mouse_y - self.y)
        else:
            self.y += max(direction.y * self.speed, mouse_y - self.y)

        self.restrict_to_screen(True, True)
        self.rect.center = (int(self.x), int(self.y))

        self.counter += 1

    def get_projectiles(self) -> list[Projectile]:
        """Retourne un projectile s'il est temps pour le joueur de tirer, sinon, ne retourne rien"""
        projectiles = []
        if self.counter % self.fire_interval == 0:
            projectiles.append(Projectile(
                x = self.x,
                y = self.y,
                speed=30,
                angle = 0
            ))
        return projectiles