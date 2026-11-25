import math
import random
import sys

import pygame
from pygame.font import Font

from pygame.sprite import Group

from game_elements.button import Button
from game_elements.enemies import Enemy, Charger, Bouncer, Shooter, Exploder
from game_elements.game_element import GameElement
from game_elements.player import Player


class Game:
    """Moteur principal orchestrant la boucle de jeu, les entités et l'affichage."""

    BACKGROUND_COLOR = (30, 60, 30)
    TEXT_COLOR = (255, 255, 255)
    GAMEOVER_COLOR = (230, 50, 50)


    ENEMY_LISTS = [
        {
            "name": "Easy",
            "enemies": [
                Charger(),
                Bouncer(),
                Shooter(),
                Exploder(
                    projectile_amount=4
                ),
            ]
        },
        {
            "name": "Normal",
            "enemies": [
                Charger(),
                Bouncer(),
                Shooter(),
                Exploder(),
            ]
        },
        {
            "name": "Hard",
            "enemies": [
                Charger(),
                Bouncer(),
                Shooter(),
                Exploder(),
            ]
        }
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
        self.enemy_interval = 75

        # Polices
        self.font_title = Font(None, 64)
        self.font_subtitle = Font(None, 32)

        # Difficulté et types d'ennemis
        self.difficulty = 0
        self.enemy_types = self.ENEMY_LISTS[0]["enemies"]

        # Entités
        limits = (self.width, self.height)
        self.player = Player(
            x=(self.width - 50) // 4,
            y=(self.height - 50) // 2,
            size=50,
            limits=limits
        )
        self.player_projectiles = Group()
        self.enemies = Group()
        self.enemy_projectiles = Group()

        # Chargement des icônes pour l'interface
        self.health_icon = GameElement(
            x=0,
            y=0,
            size=40,
            image_file="images/heart_icon.png",
            limits = limits
        )

        self.timer_icon = GameElement(
            x=0,
            y=0,
            size=40,
            image_file="images/timer_icon.png",
            limits=limits
        )

        # Boutons
        self.difficulty_buttons = [
            Button(
                x=int((self.width / len(self.ENEMY_LISTS) * i) + (self.width / len(self.ENEMY_LISTS) / 2)),
                y=self.height // 2 + 50,
                text=str(self.ENEMY_LISTS[i]["name"]),
                btn_color=(32,25,255)
            ) for i in range(len(self.ENEMY_LISTS))
        ]

        # État du jeu
        self.running = True
        self.level_select = True
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
        if self.level_select:
            for i in range(len(self.ENEMY_LISTS)):
                if self.difficulty_buttons[i].clicked():
                    self.difficulty = i
                    self.enemy_types = self.ENEMY_LISTS[i]["enemies"]
                    self.level_select = False
            return
        elif self.game_over:
            return

        # Apparition des ennemis
        self.counter += 1
        if self.counter % self.enemy_interval == 0:
            if len(self.enemy_types) > 0:
                new_enemy = self.enemy_types[random.randint(0, len(self.enemy_types) - 1)].copy()
                new_enemy.x = self.width + new_enemy.size / 2
                new_enemy.y = random.randint(0 + int(new_enemy.size / 2), self.height - int(new_enemy.size / 2))
                new_enemy.limits = self.width, self.height
                new_enemy.screen_width, new_enemy.screen_height = new_enemy.limits
                new_enemy.add(self.enemies)

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
                self.player.take_damage()
                self.draw_ui()

        for enemy_projectile in self.enemy_projectiles:
            if self.player.is_touching(enemy_projectile):
                self.player.take_damage()
                self.draw_ui()

        if self.player.is_dead():
            self.game_over = True

        # Collision des ennemis avec les projectiles du joueur
        hit_enemies = pygame.sprite.groupcollide(self.enemies, self.player_projectiles, False, True)
        for enemy in hit_enemies:
            if isinstance(enemy, Enemy):
                enemy.take_damage()
                if enemy.is_dead():
                    enemy.kill()
                    for projectile in enemy.get_death_projectiles():
                        projectile.add(self.enemy_projectiles)

    def draw_game_over(self) -> None:
        """Affiche les messages de fin de partie à l'écran."""
        surface_game_over = self.font_title.render("GAME OVER", True, self.GAMEOVER_COLOR)
        rect_game_over = surface_game_over.get_rect(center=(self.width // 2, self.height // 2 - 30))
        self.window.blit(surface_game_over, rect_game_over)

        surface_score = self.font_subtitle.render(
            f"Score: {self.counter}", True, self.TEXT_COLOR
        )
        rect_score = surface_score.get_rect(center=(self.width // 2, self.height // 2 + 30))
        self.window.blit(surface_score, rect_score)

    def draw_ui(self) -> None:
        """Affiche les points de vies du joueur et le temps de survie du joueur"""
        surface_health = self.font_title.render(f"x{str(self.player.health)}", True, self.TEXT_COLOR)
        rect_health = surface_health.get_rect(midleft=(self.width // 2, self.height - 30))
        self.window.blit(surface_health, rect_health)

        self.health_icon.rect.midright = (self.width // 2, self.height - 30)
        self.health_icon.draw(self.window)

        surface_timer = self.font_title.render(str(self.counter), True, self.TEXT_COLOR)
        rect_timer = surface_timer.get_rect(midleft=(self.width // 2, 30))
        self.window.blit(surface_timer, rect_timer)

        self.timer_icon.rect.midright = (self.width // 2, 30)
        self.timer_icon.draw(self.window)

    def draw_level_select(self) -> None:
        """Affiche les points de vies du joueur et le temps de survie du joueur"""
        surface_health = self.font_title.render("Choisissez une difficulté", True, self.TEXT_COLOR)
        rect_health = surface_health.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.window.blit(surface_health, rect_health)

        for button in self.difficulty_buttons:
            button.draw(self.window)

    def draw(self) -> None:
        """Effectue le rendu graphique complet d'une trame."""
        self.window.fill(self.BACKGROUND_COLOR)

        if self.level_select:
            self.draw_level_select()
        elif self.game_over:
            self.draw_game_over()
        else:
            self.player.draw(self.window)
            self.player_projectiles.draw(self.window)
            self.enemies.draw(self.window)
            self.enemy_projectiles.draw(self.window)

            self.draw_ui()

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