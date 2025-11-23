# game/gui.py
import pygame
import os
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

# loading assets
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
BOARD_BG = pygame.image.load(os.path.join(ASSETS_DIR, "board/board.jpg"))
BOARD_BG = pygame.transform.scale(BOARD_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
BACK_CARD_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "Back_Card.png"))
BACK_CARD_IMG = pygame.transform.scale(BACK_CARD_IMG, (120, 160))

#bars
BAR_WIDTH, BAR_HEIGHT = 300, 40
BLACK_BAR = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "statusBars/BlackBar.png")), (BAR_WIDTH, BAR_HEIGHT))
RED_BAR = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "statusBars/RedBar.png")), (BAR_WIDTH, BAR_HEIGHT))
BLUE_BAR = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "statusBars/BlueBar.png")), (BAR_WIDTH, BAR_HEIGHT))
NAMEPLATE_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "statusBars/namePlate.png")), (200, 80))
CARD_WIDTH, CARD_HEIGHT = 120, 160
CARD_SPACING = 20
FONT_PATH = os.path.join(ASSETS_DIR, "etc/font.otf")

def draw_bar(screen, x, y, current_value, max_value, bar_foreground):
    screen.blit(BLACK_BAR, (x, y))
    ratio = current_value / max_value
    filled_width = int(BAR_WIDTH * ratio)
    if filled_width > 0:
        filled_bar = bar_foreground.subsurface((0, 0, filled_width, BAR_HEIGHT))
        screen.blit(filled_bar, (x, y))

def draw_game(screen, players, current_turn):
    screen.blit(BOARD_BG, (0, 0))
    name_font = pygame.font.Font(FONT_PATH, 24)
    card_font = pygame.font.Font(FONT_PATH, 16)
    effect_font = pygame.font.Font(FONT_PATH, 14)

    hovered_card = None
    mouse_pos = pygame.mouse.get_pos()

    for i, player in enumerate(players):
        is_top = (i == 0)
        bar_y_offset = 50 if is_top else SCREEN_HEIGHT - 150

        #drawing health and mana bars on screen
        draw_bar(screen, 50, bar_y_offset, player.health, player.max_health, RED_BAR)
        draw_bar(screen, 50, bar_y_offset + 40, player.mana, player.max_mana, BLUE_BAR)

        #drawing nameplates and player names
        nameplate_x, nameplate_y = 35, bar_y_offset - 60 if is_top else bar_y_offset + 60
        screen.blit(NAMEPLATE_IMG, (nameplate_x, nameplate_y))
        name_text_surf = name_font.render(player.name, True, WHITE)
        name_text_rect = name_text_surf.get_rect(center=(nameplate_x + NAMEPLATE_IMG.get_width() // 2,
                                                         nameplate_y + NAMEPLATE_IMG.get_height() // 2))
        screen.blit(name_text_surf, name_text_rect)

        
        deck_y = bar_y_offset if is_top else bar_y_offset - 20
        screen.blit(BACK_CARD_IMG, (SCREEN_WIDTH - CARD_WIDTH - 50, deck_y))

        #Draw player hand
        num_cards = len(player.hand)
        total_width = num_cards * CARD_WIDTH + (num_cards - 1) * CARD_SPACING
        start_x = (SCREEN_WIDTH - total_width) // 2
        hand_y = 120 if is_top else SCREEN_HEIGHT - 120 - CARD_HEIGHT

        for j, card in enumerate(player.hand):
            card_x = start_x + j * (CARD_WIDTH + CARD_SPACING)
            card_rect = pygame.Rect(card_x, hand_y, CARD_WIDTH, CARD_HEIGHT)
            if i == current_turn:
                pygame.draw.rect(screen, (255, 255, 0), (card_x-2, hand_y-2, CARD_WIDTH+4, CARD_HEIGHT+4), 2)

            screen.blit(card.image, (card_x, hand_y))

            # hover
            if card_rect.collidepoint(mouse_pos):
                hovered_card = card
            name_text_surf = card_font.render(card.name, True, BLACK)
            name_text_rect = name_text_surf.get_rect(center=(card_x + CARD_WIDTH // 2, hand_y + 20))
            screen.blit(name_text_surf, name_text_rect)
            cost_text_surf = card_font.render(f"Cost: {card.cost}", True, BLACK)
            cost_text_rect = cost_text_surf.get_rect(center=(card_x + CARD_WIDTH // 2, hand_y + CARD_HEIGHT - 20))
            screen.blit(cost_text_surf, cost_text_rect)

        effects_y = hand_y - 50
        for effect in getattr(player, "effects", []):
            if effect["type"] == "block":
                txt = f"Block +{effect['value']} ({effect['turns']} turns)"
            elif effect["type"] == "boost":
                txt = f"Atk +{effect['value']} ({effect['turns']} turns)"
            else:
                continue
            effect_surf = effect_font.render(txt, True, (100, 255, 100))
            screen.blit(effect_surf, (start_x, effects_y))
            effects_y -= 20

    turn_text = name_font.render(f"{players[current_turn].name}'s Turn", True, WHITE)
    screen.blit(turn_text, (SCREEN_WIDTH // 2 - turn_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 - turn_text.get_height() // 2))

    if hovered_card:
        zoom_width, zoom_height = CARD_WIDTH * 2, CARD_HEIGHT * 2
        zoom_x = SCREEN_WIDTH // 2 - zoom_width // 2
        zoom_y = SCREEN_HEIGHT // 2 - zoom_height // 2
        zoom_image = pygame.transform.scale(hovered_card.image, (zoom_width, zoom_height))
        pygame.draw.rect(screen, (255, 255, 0), (zoom_x-3, zoom_y-3, zoom_width+6, zoom_height+6), 3)
        screen.blit(zoom_image, (zoom_x, zoom_y))
