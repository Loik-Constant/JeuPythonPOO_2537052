import math
import random
from abc import ABC, abstractmethod

import pygame

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
    def get_projectiles(self) -> list[Projectile]:
        """Retourne les projectiles s'il est temps pour l'ennemi de tirer, sinon, ne retourne rien"""
        pass

    @abstractmethod
    def get_death_projectiles(self) -> list[Projectile]:
        """Retourne les projectiles tirés lors de la mort d'un ennemi"""
        pass


class Charger(Enemy):
    """Représente un ennemi qui charge vers l'avant"""

    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            size: int = 50,
            image_file: str = 'images/charger.png',
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

    def get_projectiles(self) -> list[Projectile]:
        return []

    def get_death_projectiles(self) -> list[Projectile]:
        return []


class Bouncer(Enemy):
    """Représente un ennemi qui rebondie sur les rebords de l'écran"""

    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            size: int = 50,
            image_file: str = 'images/bouncer.png',
            limits: tuple[int, int] = (1100, 600),
            health: int = 5,
            speed: int = 5,
            rotation_interval: int = 5
    ):
        super().__init__(x, y, size, image_file, limits, health)
        self.speed = speed
        self.angle = 135 + (random.randint(0, 1) * 90)

        self.vx = math.cos(math.radians(self.angle))
        self.vy = math.sin(math.radians(self.angle))

        self.counter = 1
        self.rotation_interval = rotation_interval

    def copy(self) -> "Bouncer":
        return Bouncer(
            self.x,
            self.y,
            self.size,
            self.image_file,
            self.limits,
            self.health,
            self.speed,
        )

    def update(self) -> None:
        if self.x < 0 or self.x > self.screen_width - self.size:
            self.vx *= -1

        if self.y < 0 or self.y > self.screen_height - self.size:
            self.vy *= -1

        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

        if self.counter % self.rotation_interval == 0:
            self.image = pygame.transform.rotate(self.image, 90)

        self.counter += 1

        self.rect.topleft = (int(self.x), int(self.y))



    def get_projectiles(self) -> list[Projectile]:
        return []

    def get_death_projectiles(self) -> list[Projectile]:
        return []


class Shooter(Enemy):
    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            size: int = 50,
            image_file: str = 'images/isook.png',
            limits: tuple[int, int] = (1100, 600),
            health: int = 3,
            speed: int = 5,
            fire_interval: int = 75
    ):
        super().__init__(x, y, size, image_file, limits, health)
        self.speed = speed
        self.vy = speed

        self.fire_interval = fire_interval
        self.counter = 1

        limits_x, limits_y = self.limits
        self.end_point = limits_x - random.randint(100, 300)



    def copy(self) -> "Shooter":
        return Shooter(
            self.x,
            self.y,
            self.size,
            self.image_file,
            self.limits,
            self.health,
            self.speed,
        )

    def update(self) -> None:
        if self.x > self.end_point:
            self.x -= self.speed
        else:
            self.y += self.vy
            if self.y < 0 or self.y > self.screen_height - self.size:
                self.vy *= -1

            self.counter += 1

        self.rect.topleft = (int(self.x), int(self.y))

    def get_projectiles(self) -> list[Projectile]:
        projectiles = []
        if self.counter % self.fire_interval == 0:
            projectiles.append(Projectile(
                x=self.x + self.size / 4,
                y=self.y + self.size / 4,
                speed=10,
                angle=180,
                image_file='images/blood.png'
            ))
        return projectiles

    def get_death_projectiles(self) -> list[Projectile]:
        return []


class Exploder(Enemy):
    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            size: int = 100,
            image_file: str = 'images/exploder.png',
            limits: tuple[int, int] = (1100, 600),
            health: int = 3,
            speed: int = 5,
    ):
        super().__init__(x, y, size, image_file, limits, health)
        self.speed = speed
        self.counter = 1

    def copy(self) -> "Exploder":
        return Exploder(
            self.x,
            self.y,
            self.size,
            self.image_file,
            self.limits,
            self.health,
            self.speed,
        )

    def update(self) -> None:
        self.counter += 1

        self.x -= self.speed
        self.y -= math.sin(self.counter / 20) * self.speed

        self.destroy_offscreen()
        self.restrict_to_screen(False, True)
        self.rect.topleft = (int(self.x) + random.randint(-5, 5), int(self.y) + random.randint(-5, 5))

    def get_projectiles(self) -> list[Projectile]:
        return []

    def get_death_projectiles(self) -> list[Projectile]:
        projectiles = []
        if self.health <= 0:
            for x in range(8):
                projectiles.append(Projectile(
                    x=self.x + self.size / 4,
                    y=self.y + self.size / 4,
                    angle=x * 45,
                    speed=5,
                    size=40,
                    image_file = 'images/blood.png',
                ))
        return projectiles
