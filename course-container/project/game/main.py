# game/main.py
import os
import pygame
from models.player import Player
from game.gui import draw_game, CARD_WIDTH, CARD_HEIGHT, CARD_SPACING, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH, BOARD_BG
from game.sounds import play_card_sound

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
PROJECT_DIR = os.path.dirname(BASE_DIR)              
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")

pygame.init()
pygame.mixer.init()

#initialize mixer and play background music
pygame.mixer.music.load(os.path.join(ASSETS_DIR, "sounds", "gameMusic.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

pygame.font.init()




# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GREEN = (0, 200, 0)
RED = (200, 0, 0)



# helper functions for card clicking
def process_card_click(mouse_pos, players, current_turn):
    player = players[current_turn]
    opponent = players[1 - current_turn]

    is_top = (current_turn == 0)
    hand_y = 120 if is_top else SCREEN_HEIGHT - 120 - CARD_HEIGHT
    num_cards = len(player.hand)
    total_width = num_cards * CARD_WIDTH + (num_cards - 1) * CARD_SPACING
    start_x = (SCREEN_WIDTH - total_width) // 2

    for j, card in enumerate(player.hand):
        card_x = start_x + j * (CARD_WIDTH + CARD_SPACING)
        card_rect = pygame.Rect(card_x, hand_y, CARD_WIDTH, CARD_HEIGHT)

        if card_rect.collidepoint(mouse_pos):
            if player.mana >= card.cost:
                if hasattr(card, "play"):
                    if card.card_type == "attack":
                        card.play(opponent, player)
                    else:
                        card.play(player, player)

                    # Play the corresponding sound
                    play_card_sound(card.name)

                player.mana -= card.cost
                player.hand.pop(j)

                player.mana = min(player.max_mana, player.mana + 15)
                player.start_turn()

                next_turn_index = 1 - current_turn
                next_player = players[next_turn_index]
                next_player.start_turn()

                new_card = next_player.deck.draw_card()
                if new_card:
                    next_player.hand.append(new_card)

                return next_turn_index
            else:
                print(f"{player.name} does not have enough mana to play {card.name}")
                return current_turn
    return current_turn

# main game loop
def run_game(screen):
    clock = pygame.time.Clock()
    players = [Player("Player 1"), Player("Player 2")]
    current_turn = 0

    # drawing starting cards (initially 3)
    STARTING_HAND_SIZE = 3
    for player in players:
        player.hand = [player.deck.draw_card() for _ in range(STARTING_HAND_SIZE)]

    running = True
    winner = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                current_turn = process_card_click(mouse_pos, players, current_turn)

        # check for win conditions
        for player in players:
            if player.health <= 0:
                winner = players[1 - players.index(player)].name
                running = False
                break

        screen.fill(BLACK)
        end_turn_rect = draw_game(screen, players, current_turn)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # Check if clicked End Turn button
                if end_turn_rect.collidepoint(mouse_pos):
                    # regenerate mana for current player before switching
                    player = players[current_turn]
                    player.mana = min(player.max_mana, player.mana + 10)
                    print(f"{player.name} regenerates 10 mana. Current mana: {player.mana}")

                    # switch turn
                    current_turn = 1 - current_turn
                    players[current_turn].start_turn()
                else:
                    # process card click which might also switch turns
                    old_turn = current_turn
                    current_turn = process_card_click(mouse_pos, players, current_turn)
                    if current_turn != old_turn:
                        # if turn switched, regenerate mana for the player who just ended turn
                        ended_player = players[old_turn]
                        ended_player.mana = min(ended_player.max_mana, ended_player.mana + 10)
                        print(f"{ended_player.name} regenerates 10 mana. Current mana: {ended_player.mana}")

    return winner


def show_settings(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT_PATH, 40)
    small_font = pygame.font.Font(FONT_PATH, 24)

    # initial volumes
    music_volume = pygame.mixer.music.get_volume()  # 0.0 - 1.0
    sfx_volume = 0.5  # you can store this globally or in a settings dict

    running = True
    dragging_music = False
    dragging_sfx = False

    while running:
        screen.blit(BOARD_BG, (0, 0))

        title_surf = font.render("Settings", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)

        # Music volume slider
        music_label = small_font.render("Music Volume", True, WHITE)
        music_label_rect = music_label.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(music_label, music_label_rect)

        music_slider_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 230, 300, 20)
        pygame.draw.rect(screen, GRAY, music_slider_rect)
        # handle
        music_handle_x = music_slider_rect.x + int(music_volume * music_slider_rect.width)
        pygame.draw.rect(screen, BLACK, (music_handle_x - 10, music_slider_rect.y - 5, 20, 30))

        # SFX volume slider
        sfx_label = small_font.render("SFX Volume", True, WHITE)
        sfx_label_rect = sfx_label.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(sfx_label, sfx_label_rect)

        sfx_slider_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 330, 300, 20)
        pygame.draw.rect(screen, GRAY, sfx_slider_rect)
        # handle
        sfx_handle_x = sfx_slider_rect.x + int(sfx_volume * sfx_slider_rect.width)
        pygame.draw.rect(screen, BLACK, (sfx_handle_x - 10, sfx_slider_rect.y - 5, 20, 30))

        # Back button
        back_text = small_font.render("Back to Menu", True, WHITE)
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 125, 420, 250, 50)
        pygame.draw.rect(screen, GRAY, back_rect)
        screen.blit(back_text, (back_rect.x + 20, back_rect.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if music_slider_rect.collidepoint(mouse_pos):
                    dragging_music = True
                elif sfx_slider_rect.collidepoint(mouse_pos):
                    dragging_sfx = True
                elif back_rect.collidepoint(mouse_pos):
                    running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_music = False
                dragging_sfx = False

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, _ = event.pos
                if dragging_music:
                    # calculate music volume based on mouse position
                    music_volume = max(0.0, min(1.0, (mouse_x - music_slider_rect.x) / music_slider_rect.width))
                    pygame.mixer.music.set_volume(music_volume)
                if dragging_sfx:
                    sfx_volume = max(0.0, min(1.0, (mouse_x - sfx_slider_rect.x) / sfx_slider_rect.width))
                    # store sfx_volume somewhere to use in play_card_sound()

        clock.tick(60)


# main menu
def show_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Arcane Duel")
    clock = pygame.time.Clock()

    font = pygame.font.Font(FONT_PATH, 40)
    small_font = pygame.font.Font(FONT_PATH, 24)

    running = True
    while running:
        screen.blit(BOARD_BG, (0, 0))  # board background

        title_surf = font.render("Arcane Duel", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surf, title_rect)

        #start game button 
        start_surf = small_font.render("Start Game", True, WHITE)
        start_rect = start_surf.get_rect(center=(SCREEN_WIDTH // 2, 300))
        pygame.draw.rect(screen, BLACK, start_rect.inflate(20, 10))
        screen.blit(start_surf, start_rect)

        #simple settings button
        settings_surf = small_font.render("Settings", True, WHITE)
        settings_rect = settings_surf.get_rect(center=(SCREEN_WIDTH // 2, 360))
        pygame.draw.rect(screen, BLACK, settings_rect.inflate(20, 10))
        screen.blit(settings_surf, settings_rect)

        #quit button
        quit_surf = small_font.render("Quit", True, WHITE)
        quit_rect = quit_surf.get_rect(center=(SCREEN_WIDTH // 2, 420))
        pygame.draw.rect(screen, BLACK, quit_rect.inflate(20, 10))
        screen.blit(quit_surf, quit_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if start_rect.inflate(20, 10).collidepoint(mouse_pos):
                    winner = run_game(screen)
                    show_game_over(screen, winner)

                elif settings_rect.inflate(20, 10).collidepoint(mouse_pos):
                    show_settings(screen)  # open settings screen

                elif quit_rect.inflate(20, 10).collidepoint(mouse_pos):
                    pygame.quit()
                    return

        clock.tick(60)

# game over screen
def show_game_over(screen, winner_name):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 40)
    over_running = True

    while over_running:
        screen.fill(BLACK)
        over_text = font.render(f"{winner_name} Wins!", True, WHITE)
        retry_text = small_font.render("Back to Menu", True, WHITE)

        retry_rect = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 50, 250, 50)
        pygame.draw.rect(screen, GRAY, retry_rect)

        over_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(over_text, over_rect)
        screen.blit(retry_text, (retry_rect.x + 40, retry_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if retry_rect.collidepoint(mouse_pos):
                    over_running = False

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    show_menu()
