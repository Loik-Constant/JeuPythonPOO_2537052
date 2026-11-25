import pygame
from pygame import Surface, Rect

from pygame.sprite import Sprite


class GameElement(Sprite):
    """Classe de base représentant un élément géométrique dans l'espace 2D du jeu."""

    def __init__(self, x: float, y: float, size: int, image_file: str, limits: tuple[int, int]):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.image_file = image_file
        self.screen_width, self.screen_height = limits
        self.limits = limits

        self.image, self.rect = self.load_png()
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, surface: Surface) -> None:
        """
        Affiche le carré sur la surface spécifiée.

        :param surface : La surface sur laquel afficher l'entité
        """
        surface.blit(self.image, self.rect)

    def is_touching(self, other: "GameElement") -> bool:
        """
        Détecte si cet élément entre en collision avec un autre élément.

        :param other : L'autre élément
        """
        return self.rect.colliderect(other.rect)

    def restrict_to_screen(self, restrict_x : bool, restrict_y : bool) -> None:
        """
        Maintient l'élément à l'intérieur des bordures de la fenêtre.

        :param restrict_x : Empêche l'élément de sortir de l'écran horizontalement
        :param restrict_y : Empêche l'élément de sortir de l'écran verticalement
        """
        if restrict_x:
            self.x = max(0.0 + self.size / 2, min(float(self.screen_width - self.size / 2), self.x))

        if restrict_y:
            self.y = max(0.0  + self.size / 2, min(float(self.screen_height - self.size / 2), self.y))

        self.rect.center = (int(self.x), int(self.y))

    def destroy_offscreen(self) -> None:
        """Détruit l'élément s'il sort de la fenêtre de jeu."""
        if self.x < 0 - self.size / 2 or self.x > self.screen_width + self.size / 2:
            self.kill()

        if self.y < 0 - self.size / 2 or self.y > self.screen_height + self.size / 2:
            self.kill()

    def load_png(self) -> tuple[Surface, Rect]:
        """Retourne une image et un rectangle selon le fichier .png associé à l'objet"""
        try:
            image = pygame.image.load(self.image_file)
            image = pygame.transform.scale(image, (self.size, self.size))
        except FileNotFoundError:
            image = Surface((self.size, self.size))
        return image, image.get_rect()