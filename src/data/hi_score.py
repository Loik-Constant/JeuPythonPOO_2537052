from dataclasses import dataclass
import json

@dataclass()
class HiScore:
    """Représente le meilleur score d'une difficulté"""
    difficulty_name: str
    score: int = 0

class PersonEncoder(json.JSONEncoder):
    """Encodage JSON personnalisé pour les objets HiScore"""

    def default(self, o):
        if isinstance(o, HiScore):
            return {
                '__type__': 'HiScore',
                'difficulty_name': o.difficulty_name,
                'score': o.score
            }

        # Laisser la classe de base gérer les autres types
        return super().default(o)


def hi_score_decoder(dct):
    """Décodage JSON personnalisé pour les objets HiScore"""
    if '__type__' in dct and dct['__type__'] == 'HiScore':
        return HiScore(
            difficulty_name=dct['difficulty_name'],
            score=dct['score']
        )
    return dct

class HiScoreHandler:
    """Gestionnaire pour le chargement et la sauvegarde des meilleurs scores."""
    def __init__(self, file_name):
        self.file_name = file_name

    def load(self) -> list[HiScore]:
        """Retourne la liste des meilleurs scores contenus dans le fichier .json du gestionnaire."""
        with open(self.file_name, 'r', encoding='utf-8') as file:
            return json.load(file, object_hook=hi_score_decoder)

    def save(self, hi_scores: list[HiScore]) -> None:
        """
        Enregistre la liste des meilleurs scores dans le fichier .json du gesstionnaire.

        :param hi_scores: La liste de score à enregistrer
        """
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(hi_scores, file, cls=PersonEncoder, indent=4)