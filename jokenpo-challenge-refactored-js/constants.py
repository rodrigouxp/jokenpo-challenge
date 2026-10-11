"""Constantes globais do jogo: cores, tamanhos e enums de estado."""
from enum import Enum, auto

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

FONT_NAME = "Retro Computer"


class Move(Enum):
    """As três jogadas possíveis. O valor numérico define quem ganha de quem:
    cada jogada vence a próxima na sequência (regra circular do jokenpô)."""
    PAPER = 0
    ROCK = 1
    SCISSORS = 2

    def beats(self, other: "Move") -> bool:
        return (self.value - other.value) % 3 == 1


class Character(Enum):
    NAKED = 0
    MOTOBOY = 1
    FUNKER = 2


class Screen(Enum):
    """Qual tela está ativa no momento."""
    MENU_QUICK = auto()
    MENU_BEST = auto()
    MENU_ABOUT = auto()
    MENU_EXIT = auto()
    QUICK_GAME = auto()
    BEST_OF_3 = auto()
    ABOUT = auto()


class RoundResult(Enum):
    WIN = auto()
    LOSS = auto()
    DRAW = auto()
