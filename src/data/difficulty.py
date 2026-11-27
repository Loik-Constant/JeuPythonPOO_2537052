from dataclasses import dataclass

from game_elements.enemies import Enemy

@dataclass()
class Difficulty:
    """Représente une difficulté de jeu"""
    name: str
    enemies: list[Enemy]
    hi_score: int = 0