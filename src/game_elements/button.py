import pygame.transform
from pygame import Surface, Rect
from pygame.font import Font

from game_elements.game_element import GameElement


class Button:
    """Représente un bouton pouvant être cliqué avec la souris."""

    def __init__(
            self,
            x: int,
            y: int,
            size_x: int = 100,
            size_y: int = 50,
            text: str = "unnamed",
            text_color: tuple[int, int, int] = (255,255,255),
            btn_color: tuple[int, int, int] = (40,40,125)
    ):
        self.x = x - size_x / 2
        self.y = y - size_y / 2
        self.size_x = size_x
        self.size_y = size_y
        self.btn_color = btn_color

        self.text = text
        self.text_color = text_color
        self.font = Font(None, int(self.size_x / 4))
        self.surface_text = self.font.render(self.text, True, self.text_color)
        self.rect_text = self.surface_text.get_rect(
            center=(self.x + self.size_x / 2, self.y + + self.size_y / 2)
        )

        self.mouse_pressed_before = False

    def draw(self, surface: Surface) -> None:
        """
        Affiche le bouton sur la surface spécifiée.

        :param surface : La surface sur laquel afficher l'entité
        """
        red, green, blue = self.btn_color
        if self.hovered():
            red = int(red / 100 * 70)
            green = int(green / 100 * 70)
            blue = int(blue / 100 * 70)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                red = int(red / 100 * 70)
                green = int(green / 100 * 70)
                blue = int(blue / 100 * 70)

        pygame.draw.rect(surface,
                         (red, green, blue),
                         Rect((self.x, self.y), (self.size_x, self.size_y)),
                         border_radius=5
                         )
        surface.blit(self.surface_text, self.rect_text)

    def clicked(self) -> bool:
        """
        Détermine si le bouton a été cliqué par la souris

        :return: True si la souris à fait un click gauche sur le bouton
        """
        mouse_pressed = pygame.mouse.get_pressed(num_buttons=3)[0]
        if self.hovered():
            if (mouse_pressed == False and
                self.mouse_pressed_before):
                return True
        self.mouse_pressed_before = mouse_pressed
        return False

    def hovered(self) -> bool:
        """
        Détermine si la souris est sur le bouton

        :return: True si la souris est sur le bouton
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (self.x < mouse_x < self.x + self.size_x and
            self.y < mouse_y < self.y + self.size_y):
            return True
        return False
