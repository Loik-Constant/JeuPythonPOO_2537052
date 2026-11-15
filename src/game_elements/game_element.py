import pygame

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

        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (size, size))

        self.rect = self.image.get_rect()
        self.rect.bottomright = (int(self.x), int(self.y))

    def draw(self, surface: pygame.Surface) -> None:
        """Affiche le carré sur la surface spécifiée."""
        surface.blit(self.image, self.rect)

    def is_touching(self, other: "GameElement") -> bool:
        """Détecte si cet élément entre en collision avec un autre élément."""
        return self.rect.colliderect(other.rect)

    def restrict_to_screen(self) -> None:
        """Maintient l'élément à l'intérieur des bordures de la fenêtre."""
        self.x = max(0.0, min(float(self.screen_width - self.size), self.x))
        self.y = max(0.0, min(float(self.screen_height - self.size), self.y))

        self.rect.topleft = (int(self.x), int(self.y))

    def destroy_offscreen(self) -> None:
        if self.x < 0 - self.size or self.x > self.screen_width + self.size:
            self.kill()

        if self.y < 0 - self.size or self.y > self.screen_height + self.size:
            self.kill()