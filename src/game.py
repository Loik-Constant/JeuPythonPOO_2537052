import json
import random
import sys

import pygame
from pygame.font import Font

from pygame.sprite import Group

from data.difficulty import Difficulty
from data.hi_score import HiScore, HiScoreHandler
from game_elements.button import Button
from game_elements.enemies import Enemy, Charger, Bouncer, Shooter, Exploder
from game_elements.game_element import GameElement
from game_elements.player import Player


class Game:
    """Moteur principal orchestrant la boucle de jeu, les entités et l'affichage."""

    BACKGROUND_COLOR = (60, 60, 60)
    TEXT_COLOR = (255, 255, 255)
    GAMEOVER_COLOR = (230, 50, 50)

    PLAYER_HEALTH = 3

    MAX_ENEMY_INTERVAL = 100
    MIN_ENEMY_INTERVAL = 30
    SPAWN_INCREASE_INTERVAL = 150

    HI_SCORE_FILE = "hi_scores.json"
    DIFFICULTY_LIST = [
        Difficulty(
            "Easy",
            [
                Charger(
                    speed=7,
                    projectile_amount=1,
                    projectile_spread=0
                ),
                Bouncer(
                    speed=4,
                    health=3,
                    angle_deviation=30
                ),
                Shooter(
                    fire_interval=75,
                    speed=4
                ),
                Exploder(
                    speed=4,
                    wave_height=3,
                    projectile_amount=6
                ),
            ]
        ),
        Difficulty(
            "Normal",
            [
                Charger(),
                Bouncer(),
                Shooter(),
                Exploder(),
            ]
        ),
        Difficulty(
            "Hard",
            [
                Charger(
                    speed=13,
                    projectile_amount=3,
                    projectile_spread=45
                ),
                Bouncer(
                    speed=6,
                    health=6,
                    angle_deviation=60
                ),
                Shooter(
                    fire_interval=35,
                    speed=6
                ),
                Exploder(
                    wave_height=7,
                    wave_length=75,
                    projectile_amount=12
                ),
            ]
        ),
        Difficulty(
            "Impossible",
            [
                Charger(
                    speed=15,
                    projectile_amount=6,
                    projectile_spread=75
                ),
                Bouncer(
                    speed=8,
                    health=8,
                    angle_deviation=75
                ),
                Shooter(
                    fire_interval=25,
                    speed=7
                ),
                Exploder(
                    wave_height=12,
                    wave_length=75,
                    projectile_amount=16
                ),
            ]
        )
    ]

    def __init__(self, width: int = 1100, height: int = 600, fps: int = 60):
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("pew pew game")
        self.clock = pygame.time.Clock()

        # Polices
        self.font_title = Font(None, 64)
        self.font_subtitle = Font(None, 32)

        # Gestion d'apparition d'ennemis
        self.difficulty = Difficulty("Default", [])

        self.counter = 1
        self.enemy_interval = self.MAX_ENEMY_INTERVAL

        # Meilleurs scores
        self.hi_score_handler = HiScoreHandler(self.HI_SCORE_FILE)
        self.load_hi_scores()

        # Entités
        limits = (self.width, self.height)
        self.player = Player(
            x=self.width // 4,
            y=self.height // 2,
            size=50,
            limits=limits,
            health=self.PLAYER_HEALTH
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
                x=int((self.width / len(self.DIFFICULTY_LIST) * i) + (self.width / len(self.DIFFICULTY_LIST) / 2)),
                y=self.height // 2 + 50,
                text=str(self.DIFFICULTY_LIST[i].name)
            ) for i in range(len(self.DIFFICULTY_LIST))
        ]

        self.restart_button = Button(
            x=self.width // 2,
            y=self.height - 50,
            text="Try again"
        )

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
        """Met à jour l'état logique de l'application."""
        if self.level_select:
            self.update_level_select()
        elif self.game_over:
            self.update_game_over()
        else:
            self.update_game()


    def update_game(self):
        """Met à jour l'état logique de la partie."""

        # Apparition des ennemis
        self.counter += 1

        if self.counter % self.SPAWN_INCREASE_INTERVAL == 0:
            if self.enemy_interval > self.MIN_ENEMY_INTERVAL:
                self.enemy_interval -= 1

        if self.counter % self.enemy_interval == 0:
            if len(self.difficulty.enemies) > 0:
                new_enemy = self.difficulty.enemies[random.randint(0, len(self.difficulty.enemies) - 1)].copy()
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
            if self.difficulty.hi_score < self.counter:
                self.difficulty.hi_score = self.counter
                self.save_hi_scores()
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

    def update_level_select(self):
        """Met à jour l'état logique du menu de sélection de sifficulté."""

        for i in range(len(self.DIFFICULTY_LIST)):
            if self.difficulty_buttons[i].clicked():
                self.difficulty = self.DIFFICULTY_LIST[i]
                self.level_select = False

    def update_game_over(self):
        """Met à jour l'état logique du menu de fin de partie."""

        if self.restart_button.clicked():
            self.level_select = True
            self.game_over = False
            self.reset_game_state()

    def reset_game_state(self) -> None:
        self.player.x = self.width // 4
        self.player.y = self.height // 2
        self.player.health = self.PLAYER_HEALTH
        self.player.invincibility_timer = 0

        self.counter = 0
        self.enemy_interval = self.MAX_ENEMY_INTERVAL

        self.player_projectiles.empty()
        self.enemies.empty()
        self.enemy_projectiles.empty()

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

        self.restart_button.draw(self.window)

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
        surface_title = self.font_title.render(f"Choose a difficulty", True, self.TEXT_COLOR)
        rect_title = surface_title.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.window.blit(surface_title, rect_title)

        for i in range(len(self.difficulty_buttons)):
            self.difficulty_buttons[i].draw(self.window)
            if self.difficulty_buttons[i].hovered():
                surface_title = self.font_subtitle.render(f"Hi-score : {self.DIFFICULTY_LIST[i].hi_score}", True, self.TEXT_COLOR)
                rect_title = surface_title.get_rect(center=(self.width // 2, self.height // 2 - 50))
                self.window.blit(surface_title, rect_title)

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

    def save_hi_scores(self):
        self.hi_score_handler.save(
            [
                HiScore(difficulty.name, difficulty.hi_score)
                for difficulty in self.DIFFICULTY_LIST
            ]
        )

    def load_hi_scores(self):
        hi_scores = self.hi_score_handler.load()
        for difficulty in self.DIFFICULTY_LIST:
            for hi_score in hi_scores:
                if difficulty.name == hi_score.difficulty_name:
                    difficulty.hi_score = hi_score.score

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