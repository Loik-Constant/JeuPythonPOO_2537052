import math
import random
from abc import ABC, abstractmethod

import pygame

from game_elements.game_element import GameElement
from game_elements.projectiles import Projectile


class Enemy(GameElement, ABC):
    """
    Représente un ennemi pouvant blesser le joueur.

    Cette classe est conçu pour être hérité.
    """

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
        """Réduit les points de vie de l'ennemi."""
        self.health -= 1

    def is_dead(self) -> bool:
        """Retourne si l'ennemi est mort ou non."""
        return self.health <= 0

    @abstractmethod
    def copy(self) -> "Enemy":
        """
        Retourne une nouvelle instance de l'ennemi avec les mêmes paramètres lors de l'initialisation.

        Cette méthode doit être redéfinie.
        """
        pass

    @abstractmethod
    def update(self) -> None:
        """
        Met à jour la position de l'ennemi.

        Cette méthode doit être redéfinie.
        """
        pass

    def get_projectiles(self) -> list[Projectile]:
        """
        Retourne les projectiles s'il est temps pour l'ennemi de tirer, sinon, retourne un tableau vide.

        Cette méthode doit être redéfinie si l'ennemi tire des projectiles, sinon, l'implémentation par
        défaut retourne un tableau vide.
        """
        return []

    def get_death_projectiles(self) -> list[Projectile]:
        """
        Retourne les projectiles tirés lors de la mort d'un ennemi.

        Cette méthode doit être redéfinie si l'ennemi tire des projectiles lors de sa mort, sinon,
        l'implémentation par défaut retourne un tableau vide.
        """
        return []


class Charger(Enemy):
    """
    Représente un ennemi qui charge vers l'avant et tire des projectiles derrière lui une fois la
    gauche de l'écran atteinte.
    """

    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            size: int = 50,
            image_file: str = 'images/charger.png',
            limits: tuple[int, int] = (1100, 600),
            health: int = 2,
            speed: int = 10,
            projectile_amount: int = 2,
            projectile_spread: float = 30
    ):
        super().__init__(x, y, size, image_file, limits, health)
        self.speed = speed
        self.projectile_amount = projectile_amount
        self.projectile_spread = projectile_spread

    def copy(self) -> "Charger":
        return Charger(
            self.x,
            self.y,
            self.size,
            self.image_file,
            self.limits,
            self.health,
            self.speed,
            self.projectile_amount,
            self.projectile_spread
        )

    def update(self) -> None:
        self.x -= self.speed

        self.rect.center = (int(self.x), int(self.y))

    def get_projectiles(self) -> list[Projectile]:
        projectiles = []
        if self.x < 0 - self.size / 2:
            self.kill()
            for i in range(self.projectile_amount):
                projectiles.append(Projectile(
                    x=0,
                    y=self.y,
                    angle=((self.projectile_spread / 2) - (self.projectile_spread / max(1, (self.projectile_amount - 1)) * i)),
                    speed=8,
                    size=25,
                    image_file='images/blood.png',
                    limits=self.limits
                ))
        return projectiles


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


class Shooter(Enemy):
    """Représente un ennemi qui se tient vers la droite de l'écran et tire des projectiles"""

    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            size: int = 50,
            image_file: str = 'images/shooter.png',
            limits: tuple[int, int] = (1100, 600),
            health: int = 3,
            speed: int = 5,
            fire_interval: int = 50,
            min_distance: int = 800,
            max_distance: int = 1000
    ):
        super().__init__(x, y, size, image_file, limits, health)
        self.speed = speed
        self.direction = speed * random.choice([-1, 1])

        self.fire_interval = fire_interval
        self.counter = 1

        self.min_distance = min_distance
        self.max_distance = max_distance
        self.end_point = random.randint(self.min_distance, self.max_distance)

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
            self.y += self.speed
            if self.y < 0 + self.size / 2 or self.y > self.screen_height - self.size / 2:
                self.speed *= -1

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
                image_file='images/blood.png',
                limits=self.limits
            ))
        return projectiles


class Exploder(Enemy):
    """Représente un ennemi qui se déplace en vague vers la gauche et explose lorsqu'il meurt"""

    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            size: int = 100,
            image_file: str = 'images/exploder.png',
            limits: tuple[int, int] = (1100, 600),
            health: int = 3,
            speed: int = 5,
            wave_length: int = 100,
            wave_height: int = 5,
            projectile_amount: int = 8,
    ):
        super().__init__(x, y, size, image_file, limits, health)
        self.speed = speed
        self.wave_length = wave_length
        self.wave_height = wave_height
        self.initial_direction = random.choice([-1, 1])

        self.projectile_amount = projectile_amount

    def copy(self) -> "Exploder":
        return Exploder(
            self.x,
            self.y,
            self.size,
            self.image_file,
            self.limits,
            self.health,
            self.speed,
            self.wave_length,
            self.wave_height,
            self.projectile_amount,
        )

    def update(self) -> None:
        self.x -= self.speed
        self.y -= math.sin(self.x / self.wave_length) * self.wave_height * self.initial_direction

        self.destroy_offscreen()
        self.restrict_to_screen(False, True)
        self.rect.center = (
            int(self.x) + random.randint(-5, 5),
            int(self.y) + random.randint(-5, 5)
        )

    def get_death_projectiles(self) -> list[Projectile]:
        projectiles = []
        for i in range(self.projectile_amount):
            projectiles.append(Projectile(
                x=self.x,
                y=self.y,
                angle=i * float(360 / self.projectile_amount),
                speed=8,
                size=40,
                image_file = 'images/spike.png',
                limits=self.limits
            ))
        return projectiles
