import math

from game_elements.game_element import GameElement

class Projectile(GameElement):
    def __init__(
            self,
            x: float,
            y: float,
            size: int = 25,
            image: str = 'images/isook.png',
            limits: tuple[int, int] = (1100, 600),
            speed: float = 5.0,
            angle: float = 0,
            damage: int = 0
    ):
        super().__init__(x, y, size, image, limits)
        self.vitesse = speed
        self.damage = damage

        self.vx = math.cos(math.radians(angle))
        self.vy = math.sin(math.radians(angle))


    def update(self) -> None:
        self.x += self.vx * self.vitesse
        self.y += self.vy * self.vitesse

        self.destroy_offscreen()
        self.rect.topleft = (int(self.x), int(self.y))
