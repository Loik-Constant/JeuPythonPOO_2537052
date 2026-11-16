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
            self.health,
            self.speed
        )

    def update(self) -> None:
        self.x -= self.speed

        self.destroy_offscreen()
        self.rect.center = (int(self.x), int(self.y))

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
            size: int = 65,
            image_file: str = 'images/bouncer.png',
            limits: tuple[int, int] = (1100, 600),
            health: int = 5,
            speed: int = 5,
            angle_deviation = 45,
            rotation_interval: int = 5
    ):
        super().__init__(x, y, size, image_file, limits, health)
        self.speed = speed
        self.angle_deviation = angle_deviation
        self.initial_angle = 180 + random.choice([-self.angle_deviation, self.angle_deviation])

        self.vx = math.cos(math.radians(self.initial_angle))
        self.vy = math.sin(math.radians(self.initial_angle))

        self.rotation_interval = rotation_interval
        self.counter = 1

    def copy(self) -> "Bouncer":
        return Bouncer(
            self.x,
            self.y,
            self.size,
            self.image_file,
            self.limits,
            self.health,
            self.speed,
            self.angle_deviation,
            self.rotation_interval
        )

    def update(self) -> None:
        if self.x < 0 + self.size / 2:
            self.vx *= -1

        if self.y < 0 + self.size / 2 or self.y > self.screen_height - self.size / 2:
            self.vy *= -1

        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

        if self.counter % self.rotation_interval == 0:
            self.image = pygame.transform.rotate(self.image, 90)

        self.counter += 1

        self.destroy_offscreen()
        self.rect.center = (int(self.x), int(self.y))

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
            image_file: str = 'images/shooter.png',
            limits: tuple[int, int] = (1100, 600),
            health: int = 3,
            speed: int = 5,
            fire_interval: int = 75,
            min_distance: int = 800,
            max_distance: int = 1000
    ):
        super().__init__(x, y, size, image_file, limits, health)
        self.speed = speed
        self.vy = speed * random.choice([-1, 1])

        self.fire_interval = fire_interval
        self.counter = 1

        self.min_distance = min_distance
        self.max_distance = max_distance
        self.end_point = random.randint(min_distance, max_distance)

    def copy(self) -> "Shooter":
        return Shooter(
            self.x,
            self.y,
            self.size,
            self.image_file,
            self.limits,
            self.health,
            self.speed,
            self.fire_interval,
            self.min_distance,
            self.max_distance
        )

    def update(self) -> None:
        if self.x > self.end_point:
            self.x -= self.speed
        else:
            self.y += self.vy
            if self.y < 0 + self.size / 2 or self.y > self.screen_height - self.size / 2:
                self.vy *= -1

            self.counter += 1

        self.rect.center = (int(self.x), int(self.y))

    def get_projectiles(self) -> list[Projectile]:
        projectiles = []
        if self.counter % self.fire_interval == 0:
            projectiles.append(Projectile(
                x=self.x,
                y=self.y,
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
            projectile_amount: int = 8,
            shake_intensity: int = 5
    ):
        super().__init__(x, y, size, image_file, limits, health)
        self.speed = speed
        self.initial_direction = random.choice([-1, 1])

        self.projectile_amount = projectile_amount
        self.shake_intensity = shake_intensity

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
        self.y -= math.sin(self.counter / 20) * self.speed * self.initial_direction

        self.destroy_offscreen()
        self.restrict_to_screen(False, True)
        self.rect.center = (
            int(self.x) + random.randint(-self.shake_intensity, self.shake_intensity),
            int(self.y) + random.randint(-self.shake_intensity, self.shake_intensity)
        )

    def get_projectiles(self) -> list[Projectile]:
        return []

    def get_death_projectiles(self) -> list[Projectile]:
        projectiles = []
        for i in range(self.projectile_amount):
            projectiles.append(Projectile(
                x=self.x,
                y=self.y,
                angle=i * int(360 / self.projectile_amount),
                speed=8,
                size=40,
                image_file = 'images/spike.png',
            ))
        return projectiles
