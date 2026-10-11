"""Carrega e centraliza todas as imagens e sons do jogo.

Antes, cada classe/tela dava seu próprio pygame.image.load('data/...').
Isso duplicava carregamento de disco e espalhava os nomes dos arquivos
por todo o código. Aqui carregamos uma vez só e reaproveitamos.
"""
import pygame
from constants import Character


def _load(path, alpha=False, scale2x=False, flip=False):
    img = pygame.image.load(path)
    if alpha:
        img = img.convert_alpha()
    if scale2x:
        img = pygame.transform.scale2x(img)
    if flip:
        img = pygame.transform.flip(img, True, False)
    return img


class Assets:
    def __init__(self):
        # telas
        self.background = _load('data/background.png')
        self.ingame = _load('data/ingame.png')
        self.loading = _load('data/loading.png')

        # jogadas
        self.moves = {
            'PAPER': _load('data/paper.png', alpha=True),
            'ROCK': _load('data/rock.png', alpha=True),
            'SCISSORS': _load('data/scissors.png', alpha=True),
        }

        # botões (off/on)
        self.ready = [_load('data/ready1.png', alpha=True), _load('data/ready2.png', alpha=True)]
        self.quick = [_load('data/quick_off.png', alpha=True), _load('data/quick_on.png', alpha=True)]
        self.best = [_load('data/best_off.png', alpha=True), _load('data/best_on.png', alpha=True)]
        self.about = [_load('data/about_off.png', alpha=True), _load('data/about_on.png', alpha=True)]
        self.exit = [_load('data/exit_off.png', alpha=True), _load('data/exit_on.png', alpha=True)]
        self.back = _load('data/back_on.png')

        # sprites dos personagens: idle1, idle2, paper, rock, scissors
        self.characters = {}
        prefixes = {Character.NAKED: 'naked', Character.MOTOBOY: 'moto', Character.FUNKER: 'funker'}
        suffixes = ['idle_1', 'idle_2', 'paper', 'rock', 'sci']

        for char, prefix in prefixes.items():
            player_frames = [_load(f'data/{prefix}_{s}.png', scale2x=True) for s in suffixes]
            self.characters[char] = player_frames

        # NOTA: no jogo original, os sprites do "Computer" para FUNKER usavam,
        # por engano, os arquivos do MOTOBOY (bug do código antigo). Aqui
        # mantemos a mesma lista de personagens para os dois lados, corrigindo
        # esse bug: o computador agora também mostra os sprites certos do funker.
        self.characters_flipped = {
            char: [_load(f'data/{prefix}_{s}.png', scale2x=True, flip=True) for s in suffixes]
            for char, prefix in prefixes.items()
        }

        # sons
        self.music = pygame.mixer.Sound('data/music.wav')
        self.click_sound = pygame.mixer.Sound('data/click.wav')
