import math
import random
from abc import ABC, abstractmethod

from game_elements.game_element import GameElement
from game_elements.projectiles import Projectile


class Enemy(GameElement, ABC):
    """Représente un ennemi pouvant blesser le joueur. Cette classe doit être héritée."""

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

    def take_damage(self) -> None:
        """Réduit les points de vie de l'ennemi"""
        self.health -= 1

        if self.health <= 0:
            self.kill()

    @abstractmethod
    def copy(self):
        """Retourne une copie de l'ennemi"""
        pass

    @abstractmethod
    def update(self) -> None:
        """Met à jour la position de l'ennemi."""
        pass

    @abstractmethod
    def get_projectiles(self) -> Projectile | None:
        """Retourne un projectile s'il est temps pour l'ennemi de tirer, sinon, ne retourne rien"""
        pass


class Charger(Enemy):
    """Représente un ennemi qui charge vers l'avant"""

    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            size: int = 50,
            image_file: str = 'images/isook.png',
            limits: tuple[int, int] = (1100, 600),
            health: int = 3,
            speed: int = 10
    ):
        super().__init__(x, y, size, image_file, limits, health)
        self.speed = speed

    def copy(self) -> "Charger":
        return Charger(
            self.x,
            self.y,
            self.size,
            self.image_file,
            self.limits,
            self.health
        )

    def update(self) -> None:
        self.x -= self.speed
        self.destroy_offscreen()

        self.rect.topleft = (int(self.x), int(self.y))

    def get_projectiles(self) -> Projectile | None:
        pass


class Bouncer(Enemy):
    """Représente un ennemi qui rebondie sur les rebords de l'écran"""

    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            size: int = 50,
            image_file: str = 'images/isook.png',
            limits: tuple[int, int] = (1100, 600),
            health: int = 5,
            speed: int = 5,
            angle: int = random.randint(135, 225)
    ):
        super().__init__(x, y, size, image_file, limits, health)
        self.speed = speed
        self.angle = angle

        self.vx = math.cos(math.radians(angle))
        self.vy = math.sin(math.radians(angle))

    def copy(self) -> "Bouncer":
        return Bouncer(
            self.x,
            self.y,
            self.size,
            self.image_file,
            self.limits,
            self.health,
            self.speed,
            random.randint(135, 225)
        )

    def update(self) -> None:
        if self.x < 0 or self.x > self.screen_width - self.size:
            self.vx *= -1

        if self.y < 0 or self.y > self.screen_height - self.size:
            self.vy *= -1

        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

        self.rect.topleft = (int(self.x), int(self.y))

    def get_projectiles(self) -> Projectile | None:
        pass