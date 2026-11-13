import pygame

from pygame.sprite import Sprite


class GameElement(Sprite):
    """Classe de base représentant un élément géométrique dans l'espace 2D du jeu."""

    def __init__(self, x: float, y: float, size: int, color: tuple[int, int, int], limits: tuple[int, int]):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.screen_width, self.screen_height = limits

    @property
    def rect(self) -> pygame.Rect:
        """Retourne le rectangle de délimitation (Hitbox) de l'élément."""
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def draw(self, surface: pygame.Surface) -> None:
        """Affiche le carré sur la surface spécifiée."""
        pygame.draw.rect(surface, self.color, self.rect)

    def is_touching(self, other: "GameElement") -> bool:
        """Détecte si cet élément entre en collision avec un autre élément."""
        return self.rect.colliderect(other.rect)

    def restreindre_a_ecran(self) -> None:
        """Maintient l'élément à l'intérieur des bordures de la fenêtre."""
        self.x = max(0.0, min(float(self.screen_width - self.size), self.x))
        self.y = max(0.0, min(float(self.screen_height - self.size), self.y))
