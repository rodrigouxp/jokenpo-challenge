"""Elementos visuais: botões e personagens animados."""
import pygame
from constants import Move

MOVE_TO_FRAME = {Move.PAPER: 2, Move.ROCK: 3, Move.SCISSORS: 4}


class Button:
    def __init__(self, image, position):
        self.image = image
        self.rect = image.get_rect(topleft=position)

    def render(self, screen):
        screen.blit(self.image, self.rect)


class AnimatedCharacter(pygame.sprite.Sprite):
    """Personagem animado (idle piscando entre 2 frames, ou parado numa
    jogada específica quando o resultado da rodada é revelado).

    Substitui as antigas classes Player e Computer, que duplicavam quase
    todo o código -- a única diferença real entre elas era usar sprites
    espelhados (flip) para o computador.
    """

    def __init__(self, frames, pos_x, pos_y):
        super().__init__()
        self.frames = frames  # [idle1, idle2, paper, rock, scissors]
        self.current_frame = 0.0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

    def set_character(self, frames):
        """Troca o conjunto de sprites (ex.: ao mudar de personagem no menu)."""
        self.frames = frames

    def update_idle(self):
        """Anima o idle (piscando entre os frames 0 e 1)."""
        self.current_frame += 0.2
        if self.current_frame >= 2:
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

    def show_move(self, move: Move):
        """Mostra o frame estático da jogada revelada."""
        self.image = self.frames[MOVE_TO_FRAME[move]]
