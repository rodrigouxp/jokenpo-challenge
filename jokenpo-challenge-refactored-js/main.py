"""JOKENPO CHALLENGE - versao refatorada.

Estrutura:
  constants.py  - cores, enums (Move, Character, Screen)
  assets.py     - carregamento de imagens/sons
  sprites.py    - Button e AnimatedCharacter
  game_logic.py - regra pura de quem ganha (sem pygame)
  state.py      - GameState: todo o estado mutavel, num so lugar
  screens.py    - funcoes de desenho de cada tela
  main.py       - este arquivo: loop principal e eventos
"""
import os
import sys

import pygame

from constants import Character, Move, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, Screen, WHITE
from assets import Assets
from sprites import Button, AnimatedCharacter
from state import GameState
import screens

# permite rodar tanto via `python main.py` quanto empacotado com PyInstaller
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


def build_buttons(assets):
    b = {}
    b["quick_off"] = Button(assets.quick[0], (305, 300))
    b["best_off"] = Button(assets.best[0], (305, 325))
    b["about_off"] = Button(assets.about[0], (305, 350))
    b["exit_off"] = Button(assets.exit[0], (305, 375))
    b["back"] = Button(assets.back, (305, 420))

    b["paper"] = Button(assets.moves['PAPER'], (120, 440))
    b["rock"] = Button(assets.moves['ROCK'], (350, 450))
    b["scissors"] = Button(assets.moves['SCISSORS'], (580, 440))

    b["ready_off"] = Button(pygame.transform.scale(assets.ready[0], (70, 30)), (366, 400))
    b["ready_on"] = Button(pygame.transform.scale(assets.ready[1], (70, 30)), (366, 400))
    return b


class App:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('JOKENPO CHALLENGE')

        self.assets = Assets()
        self.buttons = build_buttons(self.assets)
        self.state = GameState()

        self.player_sprite = AnimatedCharacter(
            self.assets.characters[self.state.character_selection], 260, 260)
        self.comp_sprite = AnimatedCharacter(
            self.assets.characters_flipped[self.state.comp_selection], 458, 260)
        self.menu_char_sprite = AnimatedCharacter(
            self.assets.characters[self.state.character_selection], 178, 262)

        self._round_just_ended = False

    # ---------------------------------------------------------------- menu
    def _hovered_menu_button(self, pos):
        for name in ("quick_off", "best_off", "about_off", "exit_off"):
            if self.buttons[name].rect.collidepoint(pos):
                return name.replace("_off", "")
        return None

    def handle_events(self):
        state = self.state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION and state.screen in (
                    Screen.MENU_QUICK, Screen.MENU_BEST, Screen.MENU_ABOUT, Screen.MENU_EXIT):
                setattr(state, "_active_menu_button", self._hovered_menu_button(event.pos))

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mousedown(event)

    def _handle_keydown(self, event):
        state = self.state
        in_menu = state.screen in (Screen.MENU_QUICK, Screen.MENU_BEST, Screen.MENU_ABOUT, Screen.MENU_EXIT)

        if event.key == pygame.K_ESCAPE and in_menu:
            sys.exit()

        elif state.screen in (Screen.QUICK_GAME, Screen.BEST_OF_3):
            if event.key == pygame.K_SPACE:
                if not state.ready:
                    state.confirm_ready()
                elif state.game_over:
                    self._go_to_menu(Screen.MENU_QUICK)

        elif in_menu:
            order = [Screen.MENU_QUICK, Screen.MENU_BEST, Screen.MENU_ABOUT, Screen.MENU_EXIT]
            idx = order.index(state.screen)
            if event.key == pygame.K_DOWN:
                state.screen = order[min(len(order) - 1, idx + 1)]
            elif event.key == pygame.K_UP:
                state.screen = order[max(0, idx - 1)]
            elif event.key == pygame.K_RIGHT:
                state.cycle_character(+1)
            elif event.key == pygame.K_LEFT:
                state.cycle_character(-1)
            elif event.key == pygame.K_RETURN:
                self._confirm_menu_selection()

    def _handle_mousedown(self, event):
        state = self.state
        if state.screen in (Screen.MENU_QUICK, Screen.MENU_BEST, Screen.MENU_ABOUT, Screen.MENU_EXIT):
            hovered = self._hovered_menu_button(event.pos)
            if hovered == "quick":
                state.screen = Screen.MENU_QUICK
            elif hovered == "best":
                state.screen = Screen.MENU_BEST
            elif hovered == "about":
                state.screen = Screen.MENU_ABOUT
            elif hovered == "exit":
                state.screen = Screen.MENU_EXIT
            if self.buttons["quick_off"].rect.collidepoint(event.pos) or \
               self.buttons["best_off"].rect.collidepoint(event.pos) or \
               self.buttons["about_off"].rect.collidepoint(event.pos) or \
               self.buttons["exit_off"].rect.collidepoint(event.pos):
                self._confirm_menu_selection()

        elif state.screen in (Screen.QUICK_GAME, Screen.BEST_OF_3) and not state.ready:
            if self.buttons["paper"].rect.collidepoint(event.pos):
                self.assets.click_sound.play()
                state.choose(Move.PAPER)
            elif self.buttons["rock"].rect.collidepoint(event.pos):
                self.assets.click_sound.play()
                state.choose(Move.ROCK)
            elif self.buttons["scissors"].rect.collidepoint(event.pos):
                self.assets.click_sound.play()
                state.choose(Move.SCISSORS)
            elif self.buttons["ready_off"].rect.collidepoint(event.pos):
                state.confirm_ready()

        elif state.screen == Screen.ABOUT:
            if self.buttons["back"].rect.collidepoint(event.pos):
                state.screen = Screen.MENU_ABOUT

    def _confirm_menu_selection(self):
        state = self.state
        if state.screen == Screen.MENU_QUICK:
            state.start_new_match(Screen.QUICK_GAME)
            self.comp_sprite.set_character(self.assets.characters_flipped[state.comp_selection])
        elif state.screen == Screen.MENU_BEST:
            state.start_new_match(Screen.BEST_OF_3)
            self.comp_sprite.set_character(self.assets.characters_flipped[state.comp_selection])
        elif state.screen == Screen.MENU_ABOUT:
            state.screen = Screen.ABOUT
        elif state.screen == Screen.MENU_EXIT:
            sys.exit()

    def _go_to_menu(self, menu_screen):
        state = self.state
        state.in_game = False
        state.game_over = False
        state.screen = menu_screen

    # -------------------------------------------------------------- desenho
    def draw(self):
        state = self.state
        assets, buttons, screen = self.assets, self.buttons, self.screen

        if state.screen in (Screen.MENU_QUICK, Screen.MENU_BEST, Screen.MENU_ABOUT, Screen.MENU_EXIT):
            screens.draw_main_menu(screen, assets, buttons, state)
            self.menu_char_sprite.frames = assets.characters[state.character_selection]
            self.menu_char_sprite.update_idle()
            screen.blit(self.menu_char_sprite.image, self.menu_char_sprite.rect)

        elif state.screen == Screen.ABOUT:
            screens.draw_about(screen, assets, buttons["back"])

        elif state.screen == Screen.QUICK_GAME:
            self.player_sprite.frames = assets.characters[state.character_selection]
            self.comp_sprite.frames = assets.characters_flipped[state.comp_selection]

            round_over = screens.draw_quick_game(screen, assets, buttons, state)
            if round_over:
                state.game_over = True
                self.player_sprite.show_move(state.locked_move)
                self.comp_sprite.show_move(state.comp_move)
            else:
                self.player_sprite.update_idle()
                self.comp_sprite.update_idle()
            screen.blit(self.player_sprite.image, self.player_sprite.rect)
            screen.blit(self.comp_sprite.image, self.comp_sprite.rect)

        elif state.screen == Screen.BEST_OF_3:
            self.player_sprite.frames = assets.characters[state.character_selection]
            self.comp_sprite.frames = assets.characters_flipped[state.comp_selection]

            outcome = screens.draw_best_of_3(screen, assets, buttons, state)
            if outcome == "round_done":
                self.player_sprite.show_move(state.locked_move)
                self.comp_sprite.show_move(state.comp_move)
                state.start_new_round()  # placar mantido, nova rodada
            elif outcome is True:
                state.game_over = True
                self.player_sprite.show_move(state.last_your_move)
                self.comp_sprite.show_move(state.last_comp_move)
            else:
                self.player_sprite.update_idle()
                self.comp_sprite.update_idle()
            screen.blit(self.player_sprite.image, self.player_sprite.rect)
            screen.blit(self.comp_sprite.image, self.comp_sprite.rect)

    # ------------------------------------------------------------------ run
    def run(self):
        self.screen.blit(self.assets.loading, (0, 0))
        pygame.display.update()
        pygame.time.wait(500)
        self.assets.music.set_volume(0.3)

        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.draw()
            pygame.display.update()


if __name__ == "__main__":
    App().run()
