import random
import sys
import pygame

from pygame.sprite import Group
from game_elements.enemies import Enemy, Charger, Bouncer, Shooter, Exploder
from game_elements.player import Player


class Game:
    """Moteur principal orchestrant la boucle de jeu, les entités et l'affichage."""

    BACKGROUND_COLOR = (30, 60, 30)
    TEXT_COLOR = (255, 255, 255)
    GAMEOVER_COLOR = (230, 50, 50)

    ENEMY_TYPES = [
        Charger(),
        Bouncer(),
        Shooter(),
        Exploder(),
    ]

    def __init__(self, width: int = 1100, height: int = 600, fps: int = 60):
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("pew pew game")
        self.clock = pygame.time.Clock()

        self.counter = 1
        self.enemy_interval = 85

        # Polices
        self.font_title = pygame.font.Font(None, 64)
        self.font_subtitle = pygame.font.Font(None, 32)

        # Entités
        limits = (self.width, self.height)
        self.player = Player(
            x=(self.width - 50) // 4,
            y=(self.height - 50) // 2,
            size=50,
            limits=limits,
        )
        self.player_projectiles = Group()
        self.enemies = Group()
        self.enemy_projectiles = Group()

        # État du jeu
        self.running = True
        self.game_over = False

    def handle_events(self) -> None:
        """Traite les événements de la file Pygame."""
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                self.running = False
            elif events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self) -> None:
        """Met à jour l'état logique de la partie."""
        if self.game_over:
            return

        # Mouvement et tire du joueur
        self.player.update()
        for projectile in self.player.get_projectiles():
            projectile.add(self.player_projectiles)
        self.player_projectiles.update()

        # Mouvement et tire des ennemis
        self.enemies.update()
        for enemy in self.enemies:
            if isinstance(enemy, Enemy):
                for projectile in enemy.get_projectiles():
                    projectile.add(self.enemy_projectiles)
        self.enemy_projectiles.update()

        # Collision du joueur avec les ennemis/projectiles
        for enemy in self.enemies:
            if self.player.is_touching(enemy):
                self.game_over = True

        for enemy_projectile in self.enemy_projectiles:
            if self.player.is_touching(enemy_projectile):
                self.game_over = True

        # Collision des ennemis avec les projectiles du joueur
        hit_enemies = pygame.sprite.groupcollide(self.enemies, self.player_projectiles, False, True)
        for enemy in hit_enemies:
            if isinstance(enemy, Enemy):
                enemy.take_damage()
                if enemy.health <= 0:
                    for projectile in enemy.get_death_projectiles():
                        projectile.add(self.enemy_projectiles)

        # Apparition des ennemis
        self.counter += 1
        if self.counter % self.enemy_interval == 0:
            new_enemy = self.ENEMY_TYPES[random.randint(0, len(self.ENEMY_TYPES) - 1)].copy()
            new_enemy.x = 1100 - new_enemy.size / 2
            new_enemy.y = random.randint(0 + int(new_enemy.size / 2), 600 - int(new_enemy.size / 2))
            new_enemy.add(self.enemies)

    def draw_game_over(self) -> None:
        """Affiche les messages de fin de partie à l'écran."""
        surface_titre = self.font_title.render("GAME OVER", True, self.GAMEOVER_COLOR)
        rect_titre = surface_titre.get_rect(center=(self.width // 2, self.height // 2 - 30))
        self.window.blit(surface_titre, rect_titre)

        surface_instruction = self.font_subtitle.render(
            "Appuyez sur ESC pour quitter", True, self.TEXT_COLOR
        )
        rect_instruction = surface_instruction.get_rect(center=(self.width // 2, self.height // 2 + 30))
        self.window.blit(surface_instruction, rect_instruction)

    def draw(self) -> None:
        """Effectue le rendu graphique complet d'une trame."""
        self.window.fill(self.BACKGROUND_COLOR)

        # Dessin des entités
        self.player.draw(self.window)
        self.player_projectiles.draw(self.window)
        self.enemies.draw(self.window)
        self.enemy_projectiles.draw(self.window)

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def begin(self) -> None:
        """Lance et maintient la boucle principale du jeu."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.begin()