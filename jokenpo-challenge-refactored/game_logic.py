"""Regras do jogo, isoladas de qualquer coisa relacionada a desenho/pygame.

Isso é o que antes estava espalhado em ~15 blocos if/if/if repetidos
dentro de quick_game() e best_round() no main.py original.
"""
from constants import Move, RoundResult


def resolve_round(your_move: Move, comp_move: Move) -> RoundResult:
    if your_move == comp_move:
        return RoundResult.DRAW
    if your_move.beats(comp_move):
        return RoundResult.WIN
    return RoundResult.LOSS
