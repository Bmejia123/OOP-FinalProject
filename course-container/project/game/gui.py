# game/gui.py
import pygame
import os
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

END_TURN_WIDTH, END_TURN_HEIGHT = 150, 50
CARD_WIDTH, CARD_HEIGHT = 120, 160
CARD_SPACING = 20

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # game/
PROJECT_DIR = os.path.dirname(BASE_DIR)               # project root
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")

#loading assets
BOARD_BG = pygame.image.load(os.path.join(ASSETS_DIR, "board", "board.jpg"))
BOARD_BG = pygame.transform.scale(BOARD_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

BACK_CARD_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "Back_Card.png"))
BACK_CARD_IMG = pygame.transform.scale(BACK_CARD_IMG, (CARD_WIDTH, CARD_HEIGHT))

# Status bars
BAR_WIDTH, BAR_HEIGHT = 300, 40
BLACK_BAR = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS_DIR, "statusBars", "BlackBar.png")), (BAR_WIDTH, BAR_HEIGHT)
)
RED_BAR = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS_DIR, "statusBars", "RedBar.png")), (BAR_WIDTH, BAR_HEIGHT)
)
BLUE_BAR = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS_DIR, "statusBars", "BlueBar.png")), (BAR_WIDTH, BAR_HEIGHT)
)
NAMEPLATE_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS_DIR, "statusBars", "namePlate.png")), (200, 80)
)

#custom font 
FONT_PATH = os.path.join(ASSETS_DIR, "etc", "font.otf")



def draw_bar(screen, x, y, current_value, max_value, bar_foreground):
    screen.blit(BLACK_BAR, (x, y))
    ratio = current_value / max_value
    filled_width = int(BAR_WIDTH * ratio)
    if filled_width > 0:
        filled_bar = bar_foreground.subsurface((0, 0, filled_width, BAR_HEIGHT))
        screen.blit(filled_bar, (x, y))

#helper function to draw exact rect to draw cards
#was made to fix some hitbox card issues
def get_card_rect(index, num_cards, is_bottom, scale=1.0):
    total_width = num_cards * CARD_WIDTH + (num_cards - 1) * CARD_SPACING
    start_x = (SCREEN_WIDTH - total_width) // 2

    base_x = start_x + index * (CARD_WIDTH + CARD_SPACING)
    base_y = SCREEN_HEIGHT - 120 - CARD_HEIGHT if is_bottom else 120

    scaled_w = int(CARD_WIDTH * scale)
    scaled_h = int(CARD_HEIGHT * scale)

    rect = pygame.Rect(
        base_x + (CARD_WIDTH - scaled_w) // 2,
        base_y + (CARD_HEIGHT - scaled_h) // 2,
        scaled_w,
        scaled_h
    )

    return rect


def draw_end_turn_button(screen):
    font = pygame.font.Font(FONT_PATH, 24)
    rect = pygame.Rect(SCREEN_WIDTH - END_TURN_WIDTH - 50, SCREEN_HEIGHT // 2 - END_TURN_HEIGHT // 2, END_TURN_WIDTH, END_TURN_HEIGHT)
    pygame.draw.rect(screen, (50, 50, 50), rect)
    text_surf = font.render("End Turn", True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    return rect  # return the rect so we can check clicks

def draw_game(screen, players, current_turn):
    screen.blit(BOARD_BG, (0, 0))
    name_font = pygame.font.Font(FONT_PATH, 24)
    card_font = pygame.font.Font(FONT_PATH, 16)
    effect_font = pygame.font.Font(FONT_PATH, 14)
    value_font = pygame.font.Font(FONT_PATH, 20)  # font for numeric values

    hovered_card = None
    mouse_pos = pygame.mouse.get_pos()

    for i, player in enumerate(players):
        is_bottom = (i == 0)
        bar_y_offset = SCREEN_HEIGHT - 150 if is_bottom else 50

        #drawing health and mana bars on screen
        draw_bar(screen, 50, bar_y_offset, player.health, player.max_health, RED_BAR)
        health_text = value_font.render(f"{player.health}/{player.max_health}", True, WHITE)
        screen.blit(health_text, (50 + BAR_WIDTH + 10, bar_y_offset + (BAR_HEIGHT - health_text.get_height()) // 2))

        #drawing nameplates and player names
        draw_bar(screen, 50, bar_y_offset + 40, player.mana, player.max_mana, BLUE_BAR)
        mana_text = value_font.render(f"{player.mana}/{player.max_mana}", True, WHITE)
        screen.blit(mana_text, (50 + BAR_WIDTH + 10, bar_y_offset + 40 + (BAR_HEIGHT - mana_text.get_height()) // 2))

        #drawing nameplates and player names
        nameplate_x, nameplate_y = 35, bar_y_offset + 60 if is_bottom else bar_y_offset - 60
        screen.blit(NAMEPLATE_IMG, (nameplate_x, nameplate_y))
        name_text_surf = name_font.render(player.name, True, WHITE)
        name_text_rect = name_text_surf.get_rect(center=(nameplate_x + NAMEPLATE_IMG.get_width() // 2,
                                                         nameplate_y + NAMEPLATE_IMG.get_height() // 2))
        screen.blit(name_text_surf, name_text_rect)

        # deck itself
        deck_y = bar_y_offset - 20 if is_bottom else bar_y_offset
        screen.blit(BACK_CARD_IMG, (SCREEN_WIDTH - CARD_WIDTH - 50, deck_y))

        #Draw player hand
        num_cards = len(player.hand)
        total_width = num_cards * CARD_WIDTH + (num_cards - 1) * CARD_SPACING
        start_x = (SCREEN_WIDTH - total_width) // 2
        hand_y = SCREEN_HEIGHT - 120 - CARD_HEIGHT if is_bottom else 120

       

        for j, card in enumerate(player.hand):
            if not hasattr(card, "scale"):
                card.scale = 1.0

            #hover
            hover_rect = get_card_rect(j, num_cards, is_bottom, 1.2)
            is_hovering = hover_rect.collidepoint(mouse_pos)

            #smooth animation scale
            target_scale = 1.2 if is_hovering else 1.0
            card.scale += (target_scale - card.scale) * 0.18

            # REAL rect used for drawing (used to fix bug)
            rect = get_card_rect(j, num_cards, is_bottom, card.scale)

            img = pygame.transform.scale(card.image, (rect.width, rect.height))
            screen.blit(img, rect.topleft)

            # hover glow
            if i == current_turn:
                pygame.draw.rect(screen, (255, 255, 0),
                                (rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4), 2)

            # name and cost labels
            name_surf = card_font.render(card.name, True, BLACK)
            screen.blit(name_surf, name_surf.get_rect(center=(rect.centerx, rect.y + 20)))

            cost_surf = card_font.render(f"Cost: {card.cost}", True, BLACK)
            screen.blit(cost_surf, cost_surf.get_rect(center=(rect.centerx, rect.bottom - 20)))

            if is_hovering:
                hovered_card = card


        #Effects above hand to see active effects
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

    # indicator to see whos turn it is
    turn_text = name_font.render(f"{players[current_turn].name}'s Turn", True, WHITE)
    screen.blit(turn_text, (SCREEN_WIDTH // 2 - turn_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 - turn_text.get_height() // 2))

    #hoverd card
    if hovered_card:
        if not hasattr(hovered_card, "zoom_scale"):
            hovered_card.zoom_scale = 1.0

        target_zoom = 2.0
        hovered_card.zoom_scale += (target_zoom - hovered_card.zoom_scale) * 0.2

        zoom_width = int(CARD_WIDTH * hovered_card.zoom_scale)
        zoom_height = int(CARD_HEIGHT * hovered_card.zoom_scale)
        zoom_x = SCREEN_WIDTH // 2 - zoom_width // 2
        zoom_y = SCREEN_HEIGHT // 2 - zoom_height // 2

        zoom_image = pygame.transform.scale(hovered_card.image, (zoom_width, zoom_height))
        pygame.draw.rect(screen, (255, 255, 0), (zoom_x-3, zoom_y-3, zoom_width+6, zoom_height+6), 3)
        screen.blit(zoom_image, (zoom_x, zoom_y))
    else:
        # reset size/pos if no hover event
        for player in players:
            for card in player.hand:
                if hasattr(card, "zoom_scale"):
                    card.zoom_scale += (1.0 - card.zoom_scale) * 0.2

    end_turn_rect = draw_end_turn_button(screen)
    return end_turn_rect
