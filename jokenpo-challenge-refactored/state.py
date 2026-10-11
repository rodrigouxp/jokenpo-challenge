"""Estado mutável do jogo, num único lugar.

No código original, coisas como choice, ready, comp, yourScore etc. eram
variáveis globais soltas, manipuladas com `global` dentro de várias
funções espalhadas pelo arquivo. Aqui elas viram atributos de um único
objeto, passado explicitamente para quem precisa -- muito mais fácil de
rastrear "quem mexeu no quê".
"""
from random import choice as random_choice
from constants import Character, Move, Screen


class GameState:
    def __init__(self):
        self.screen = Screen.MENU_QUICK
        self.character_selection = Character.NAKED
        self.comp_selection = Character.NAKED

        self.in_game = False
        self.ready = False
        self.game_over = False

        self.your_move: Move | None = None
        self.comp_move: Move | None = None
        self._locked_move: Move | None = None

        self.your_score = 0
        self.comp_score = 0

        self.last_your_move: Move | None = None
        self.last_comp_move: Move | None = None

    # ---- navegação do menu ----
    def cycle_character(self, direction: int):
        """direction: +1 (direita) ou -1 (esquerda)."""
        members = list(Character)
        idx = members.index(self.character_selection)
        idx = max(0, min(len(members) - 1, idx + direction))
        self.character_selection = members[idx]

    # ---- transições de partida ----
    def start_new_match(self, target_screen: Screen):
        self.your_move = None
        self.comp_move = random_choice(list(Move))
        self.comp_selection = random_choice(list(Character))
        self._locked_move = None
        self.ready = False
        self.in_game = True
        self.game_over = False
        self.your_score = 0
        self.comp_score = 0
        self.screen = target_screen

    def start_new_round(self):
        """Reinicia apenas a rodada (mantém placar), usado no melhor de 3."""
        self.your_move = None
        self.comp_move = random_choice(list(Move))
        self.comp_selection = random_choice(list(Character))
        self._locked_move = None
        self.ready = False

    def choose(self, move: Move):
        self.your_move = move

    def confirm_ready(self):
        if self.your_move is not None:
            self.ready = True
            self._locked_move = self.your_move

    @property
    def locked_move(self) -> Move | None:
        return self._locked_move
