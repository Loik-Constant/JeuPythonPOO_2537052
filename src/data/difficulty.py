from dataclasses import dataclass

from game_elements.enemies import Enemy

@dataclass(frozen=True)
class Difficulty:
    """Représente une difficulté de jeu"""
    name: str
    enemies: list[Enemy]