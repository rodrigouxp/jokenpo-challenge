"""Funções de desenho de cada tela. Só desenham -- não mudam estado."""
import pygame
from constants import Character, FONT_NAME, GREEN, RED, WHITE, YELLOW, Move
from game_logic import resolve_round, RoundResult

CHAR_LABELS = {Character.NAKED: "NAKEDMAN", Character.MOTOBOY: "MOTOBOY", Character.FUNKER: "FUNKER"}
MOVE_KEY = {Move.PAPER: 'PAPER', Move.ROCK: 'ROCK', Move.SCISSORS: 'SCISSORS'}


def font(size):
    return pygame.font.SysFont(FONT_NAME, size, False, False)


def draw_main_menu(screen, assets, buttons, state):
    screen.blit(assets.background, (0, 0))

    label = font(14).render(CHAR_LABELS[state.character_selection], True, WHITE)
    x = {"NAKEDMAN": 166, "MOTOBOY": 173, "FUNKER": 178}[CHAR_LABELS[state.character_selection]]
    screen.blit(label, (x, 370))
    if state.character_selection != Character.NAKED:
        screen.blit(font(14).render("<", True, WHITE), (150, 350))
    if state.character_selection != Character.FUNKER:
        screen.blit(font(14).render(">", True, WHITE), (270, 350))

    for name in ("quick", "best", "about", "exit"):
        is_active = getattr(state, "_active_menu_button", None) == name
        img = getattr(assets, name)[1 if is_active else 0]
        screen.blit(img, buttons[name + "_off"].rect.topleft)


def draw_about(screen, assets, back_button):
    screen.fill((0, 0, 0))
    created = font(14).render("-- Created by Rodrigo Formigon, Heavy Games Co. --", True, WHITE)
    version = font(14).render("-- Version 0.3.0 (refactored) --", True, WHITE)
    screen.blit(created, (155, 330))
    screen.blit(version, (280, 360))
    back_button.render(screen)


def _draw_move_row(screen, assets, buttons, your_move, comp_move, ready_pressed):
    screen.blit(assets.ingame, (0, 0))
    buttons["paper"].render(screen)
    buttons["rock"].render(screen)
    buttons["scissors"].render(screen)
    buttons["ready_on" if ready_pressed else "ready_off"].render(screen)

    f = font(16)
    you_label = f.render("YOU: ", True, WHITE)
    screen.blit(you_label, (260, 200))
    if your_move is not None:
        img = assets.moves[MOVE_KEY[your_move]]
        screen.blit(pygame.transform.scale(img, (40, 40)), (310, 188))

    comp_label = f.render(" :COMPUTER" if your_move is not None else "___ :COMPUTER", True, WHITE)
    screen.blit(comp_label, (492, 200) if your_move is not None else (450, 200))
    if comp_move is not None:
        img = assets.moves[MOVE_KEY[comp_move]]
        screen.blit(pygame.transform.scale(img, (40, 40)), (450, 188))


def draw_result_banner(screen, result: RoundResult):
    if result == RoundResult.WIN:
        screen.blit(font(40).render("YOU WON!", True, GREEN), (290, 80))
    elif result == RoundResult.LOSS:
        screen.blit(font(40).render("YOU LOST!", True, RED), (272, 80))
    else:
        screen.blit(font(40).render("DRAW", True, YELLOW), (333, 80))


def draw_quick_game(screen, assets, buttons, state):
    """Rodada única. Retorna True quando a rodada terminou (resultado revelado)."""
    _draw_move_row(screen, assets, buttons, state.your_move, None if not state.ready else state.comp_move,
                   ready_pressed=state.ready)

    if state.ready and state.locked_move is not None:
        result = resolve_round(state.locked_move, state.comp_move)
        draw_result_banner(screen, result)
        screen.blit(font(16).render('Press "space" to main menu', True, WHITE), (249, 150))
        return True
    return False


def draw_best_of_3(screen, assets, buttons, state):
    """Retorna True quando a partida (melhor de 3) acabou."""
    if state.your_score == 2 or state.comp_score == 2:
        _draw_move_row(screen, assets, buttons, state.last_your_move, state.last_comp_move, ready_pressed=True)
        draw_result_banner(screen, RoundResult.WIN if state.your_score == 2 else RoundResult.LOSS)
        screen.blit(font(16).render('Press "space" to main menu', True, WHITE), (249, 150))
        return True

    _draw_move_row(screen, assets, buttons, state.your_move, None if not state.ready else state.comp_move,
                   ready_pressed=state.ready)

    if state.ready and state.locked_move is not None:
        result = resolve_round(state.locked_move, state.comp_move)
        draw_result_banner(screen, result)
        state.last_your_move = state.locked_move
        state.last_comp_move = state.comp_move
        if result == RoundResult.WIN:
            state.your_score += 1
        elif result == RoundResult.LOSS:
            state.comp_score += 1
        return "round_done"
    return False
