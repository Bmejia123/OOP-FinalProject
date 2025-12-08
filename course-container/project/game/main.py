# game/main.py
import os
import pygame
from models.player import Player
from game.ai import ai_take_turn
from game.gui import draw_game, CARD_WIDTH, CARD_HEIGHT, CARD_SPACING, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH, BOARD_BG
from game.sounds import play_card_sound

pygame.init()
if not hasattr(pygame, "volume_settings"):
    pygame.volume_settings = {"music": 0.5, "sfx": 0.5}

pygame.mixer.init()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
PROJECT_DIR = os.path.dirname(BASE_DIR)              
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")


draw_card_sound = pygame.mixer.Sound(
    os.path.join(PROJECT_DIR, "assets", "sounds", "drawCard.mp3")
)

draw_card_sound.set_volume(0.2) 

pygame.font.init()

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# Button function (we can reuse everywhere)
def draw_button(screen, btn, mouse_pos, font, default_color=BLACK, hover_color=(80,80,80)):
    rect = btn["rect"]
    is_hovering = rect.collidepoint(mouse_pos)
    btn["hovered"] = is_hovering

    target_scale = 1.1 if is_hovering else 1.0
    btn["scale"] += (target_scale - btn["scale"]) * 0.2

    scaled_width = int(rect.width * btn["scale"])
    scaled_height = int(rect.height * btn["scale"])
    scaled_rect = pygame.Rect(
        rect.centerx - scaled_width // 2,
        rect.centery - scaled_height // 2,
        scaled_width,
        scaled_height
    )

    color = hover_color if is_hovering else default_color
    pygame.draw.rect(screen, color, scaled_rect)

    label_surf = font.render(btn["label"], True, WHITE)
    label_rect = label_surf.get_rect(center=scaled_rect.center)
    screen.blit(label_surf, label_rect)

    return scaled_rect, is_hovering


# card click handler // play a card
def process_card_click(mouse_pos, players, current_turn):
    player = players[current_turn]
    opponent = players[1 - current_turn]

    is_bottom = (current_turn == 0)
    hand_y = SCREEN_HEIGHT - 120 - CARD_HEIGHT if is_bottom else 120
    num_cards = len(player.hand)
    total_width = num_cards * CARD_WIDTH + (num_cards - 1) * CARD_SPACING
    start_x = (SCREEN_WIDTH - total_width) // 2

    for index, card in enumerate(player.hand):
        card_x = start_x + index * (CARD_WIDTH + CARD_SPACING)
        card_rect = pygame.Rect(card_x, hand_y, CARD_WIDTH, CARD_HEIGHT)
        if card_rect.collidepoint(mouse_pos):
            if player.mana < card.cost:
                return current_turn
            if hasattr(card, "play"):
                if card.card_type == "attack":
                    card.play(opponent, player)
                else:
                    card.play(player, player)
                play_card_sound(card.name)
            player.mana -= card.cost
            player.hand.pop(index)
            return 1 - current_turn
    return current_turn

# in game menu from game itself // basically pause menu
def in_game_menu(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT_PATH, 36)
    small_font = pygame.font.Font(FONT_PATH, 24)

    buttons = [
        {"label": "Settings", "rect": pygame.Rect(SCREEN_WIDTH//2-100, 200, 200, 60), "action": "settings", "scale":1.0, "hovered": False},
        {"label": "Main Menu", "rect": pygame.Rect(SCREEN_WIDTH//2-100, 300, 200, 60), "action": "main_menu", "scale":1.0, "hovered": False},
        {"label": "Cancel", "rect": pygame.Rect(SCREEN_WIDTH//2-100, 400, 200, 60), "action": None, "scale":1.0, "hovered": False},
    ]

    running = True
    while running:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        title_surf = font.render("Game Menu", True, WHITE)
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH//2, 100)))

        for btn in buttons:
            draw_button(screen, btn, mouse_pos, small_font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        return btn["action"]

        clock.tick(60)


# main game loop 
def run_game(screen, ai_difficulty="easy"):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join(ASSETS_DIR, "sounds", "fantasyMainMusic.mp3"))
    pygame.mixer.music.set_volume(pygame.volume_settings["music"])
    pygame.mixer.music.play(-1)

    CARD_DRAW_DURATION = 300  
    CARD_WIDTH, CARD_HEIGHT = 80, 120 

    clock = pygame.time.Clock()
    players = [Player("Player 1"), Player("AI")]
    current_turn = 0
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

    
    card_back_image = None
    try:
        original_image = pygame.image.load('assets/Back_Card.png').convert_alpha()
        card_back_image = pygame.transform.scale(original_image, (CARD_WIDTH, CARD_HEIGHT))
    except pygame.error:
        pass

    for p in players:
        p.hand = [p.deck.draw_card() for _ in range(3)]

    player_can_end_turn = True
    end_turn_scale = 1.0
    running = True
    winner = None

    last_played_card = [None, None]

    # time for ai / timer for ai's turn
    ai_turn_wait_time = 600
    ai_turn_start_time = None

    # animation queue (so its not cluttery)
    animation_queue = []

    card_animation = {"active": False, "card": None, "start_pos": (0, 0), "end_pos": (0, 0), "start_time": 0, "callback": None}

    # lots of helper functions
    def draw_single_card_at_pos(surface, card_back_img, x, y, card=None):
        rect = pygame.Rect(x - CARD_WIDTH // 2, y - CARD_HEIGHT // 2, CARD_WIDTH, CARD_HEIGHT)
        if card and hasattr(card, "image") and card.image:
            img = pygame.transform.scale(card.image, (CARD_WIDTH, CARD_HEIGHT))
            surface.blit(img, rect.topleft)
        elif card_back_img:
            surface.blit(card_back_img, rect.topleft)
        else:
            pygame.draw.rect(surface, (150, 0, 0), rect, border_radius=5)
            pygame.draw.rect(surface, (0, 0, 0), rect, 2, border_radius=5)
            if card:
                font = pygame.font.Font(FONT_PATH, 16)
                text_surf = font.render(card.name, True, (255, 255, 255))
                surface.blit(text_surf, text_surf.get_rect(center=rect.center))

    def start_animation(card, start_pos, end_pos, callback=None):
        card_animation["active"] = True
        card_animation["card"] = card
        card_animation["start_pos"] = start_pos
        card_animation["end_pos"] = end_pos
        card_animation["start_time"] = pygame.time.get_ticks()
        card_animation["callback"] = callback

    def draw_card_for_player(player, switch_turn=False):
        MAX_HAND_SIZE = 5
        if len(player.hand) >= MAX_HAND_SIZE:
            return False

        card = player.deck.draw_card()
        if card:
            draw_card_sound.play()

            def on_complete():
                player.hand.append(card)
                if switch_turn:
                    nonlocal current_turn, player_can_end_turn
                    current_turn = 1 - current_turn
                    if current_turn == 0:
                        players[0].start_turn()
                        player_can_end_turn = True

            animation_queue.append(lambda: start_animation(
                card,
                (SCREEN_WIDTH - 100, SCREEN_HEIGHT / 2),
                (SCREEN_WIDTH / 2, SCREEN_HEIGHT - CARD_HEIGHT if players.index(player) == 0 else CARD_HEIGHT),
                on_complete
            ))
            return True

        return False


    def play_card_animation(card, target_index):
        if target_index == 0:
            start_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120 - CARD_HEIGHT)
            end_pos = (200, SCREEN_HEIGHT - 250)
        else:
            start_pos = (SCREEN_WIDTH // 2, 120)
            end_pos = (200, 200)

        def on_complete():
            last_played_card[target_index] = card

        animation_queue.append(lambda: start_animation(card, start_pos, end_pos, on_complete))

    def ai_play(ai, opponent):
        playable = [c for c in ai.hand if c.cost <= ai.mana]
        if not playable:
            return False
        import random
        if ai_difficulty == "easy":
            if random.random() < 0.25:
                return False
            card = random.choice(playable)
        elif ai_difficulty == "medium":
            card = min(playable, key=lambda c: c.cost)
        else:
            card = max(playable, key=lambda c: getattr(c, "damage", 0))

        if card.card_type == "attack":
            card.play(opponent, ai)
        else:
            card.play(ai, ai)
        ai.mana -= card.cost
        ai.hand.remove(card)
        play_card_animation(card, 1)
        return True

    def process_card_click(mouse_pos, players, current_turn):
        from game.gui import get_card_rect
        player = players[current_turn]
        opponent = players[1 - current_turn]
        is_bottom = (current_turn == 0)
        num_cards = len(player.hand)

        for index, card in enumerate(player.hand):
            if not hasattr(card, "scale"):
                card.scale = 1.0
            rect = get_card_rect(index, num_cards, is_bottom, card.scale)
            if rect.collidepoint(mouse_pos):
                if player.mana < card.cost:
                    return current_turn
                if hasattr(card, "play"):
                    if card.card_type == "attack":
                        card.play(opponent, player)
                    else:
                        card.play(player, player)
                play_card_sound(card.name)
                player.mana -= card.cost
                player.hand.pop(index)
                play_card_animation(card, 0)
                return 1 - current_turn
        return current_turn

    # main loop
    while running:
        screen.fill(BLACK)
        end_turn_rect = draw_game(screen, players, current_turn)
        mouse_pos = pygame.mouse.get_pos()

        #animation queue
        if not card_animation["active"] and animation_queue:
            animation_queue.pop(0)()

        # animating current card 
        if card_animation["active"]:
            elapsed = pygame.time.get_ticks() - card_animation["start_time"]
            progress = min(1.0, elapsed / CARD_DRAW_DURATION)
            start_x, start_y = card_animation["start_pos"]
            end_x, end_y = card_animation["end_pos"]
            current_x = start_x + (end_x - start_x) * progress
            current_y = start_y + (end_y - start_y) * progress
            draw_single_card_at_pos(screen, card_back_image, current_x, current_y, card_animation["card"])
            if progress >= 1.0:
                if card_animation["callback"]:
                    card_animation["callback"]()
                card_animation["active"] = False
                card_animation["card"] = None

        # last card played piles shown on screen (2 piles)
        for i, card in enumerate(last_played_card):
            if card:
                x, y = (200, SCREEN_HEIGHT - 250) if i == 0 else (200, 200)
                draw_single_card_at_pos(screen, card_back_image, x, y, card)

        #End turn
        if current_turn == 0 and not card_animation["active"]:
            end_turn_btn = {"rect": end_turn_rect, "scale": end_turn_scale, "hovered": False, "label": "End Turn"}
            scaled_rect, hovering = draw_button(screen, end_turn_btn, mouse_pos, pygame.font.Font(FONT_PATH, 24))
            end_turn_scale = end_turn_btn["scale"]

        #menu btn
        menu_btn_rect = pygame.Rect((SCREEN_WIDTH - 140) // 2, 20, 140, 40)
        menu_btn = {"rect": menu_btn_rect, "scale": 1.0, "hovered": False, "label": "Menu"}
        draw_button(screen, menu_btn, mouse_pos, pygame.font.Font(FONT_PATH, 24))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if card_animation["active"]:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = event.pos
                player = players[0]

                # Check if clicked End Turn button
                if current_turn == 0 and end_turn_rect.collidepoint(mouse_clicked) and player_can_end_turn:
                    # regenerate mana for current player before switching (can switch here)
                    player.mana = min(player.max_mana, player.mana + 15)
                    if not draw_card_for_player(player, switch_turn=True):
                        current_turn = 1
                    player_can_end_turn = False
                    continue

               #check if clicked menu btns
                if menu_btn_rect.collidepoint(mouse_clicked):
                    choice = in_game_menu(screen)
                    if choice == "settings":
                        show_settings(screen, from_game=True)
                    elif choice == "main_menu":
                        pygame.mixer.music.stop()
                        return None
                    continue


                # process card click which might also switch turns
                new_turn = process_card_click(mouse_clicked, players, current_turn)
                if new_turn != current_turn:
                    player.mana = min(player.max_mana, player.mana + 15)
                    if not draw_card_for_player(player, switch_turn=True):
                        current_turn = 1
                    player_can_end_turn = False

        # AI Turn CODE
        if current_turn == 1 and not card_animation["active"]:
            ai = players[1]
            player = players[0]
            if ai_turn_start_time is None:
                ai_turn_start_time = pygame.time.get_ticks()
                ai.start_turn()
                ai.mana = min(ai.max_mana, ai.mana + 15)
            else:
                elapsed = pygame.time.get_ticks() - ai_turn_start_time
                if elapsed >= ai_turn_wait_time:
                    ai_play(ai, player)
                    if not draw_card_for_player(ai, switch_turn=True):
                        current_turn = 0
                        player.start_turn()
                        player_can_end_turn = True
                    ai_turn_start_time = None

        # checking win conditions
        for p in players:
            if p.health <= 0:
                winner = players[1 - players.index(p)].name
                running = False

        clock.tick(60)

    return winner





def show_settings(screen, from_game=False):
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT_PATH, 40)
    small_font = pygame.font.Font(FONT_PATH, 24)

    if not hasattr(pygame, "volume_settings"):
        pygame.volume_settings = {"music": pygame.mixer.music.get_volume(), "sfx": 0.5}

    # initial volumes
    music_volume = pygame.volume_settings["music"] # based on volume settings
    sfx_volume = pygame.volume_settings["sfx"] # based on volume settings

    back_label = "Back to Game" if from_game else "Back to Menu"
    buttons = [
        {"label": back_label, "rect": pygame.Rect(SCREEN_WIDTH // 2 - 125, 420, 250, 50),
         "action": "back", "scale": 1.0, "hovered": False}
    ]

    sliders = {
        "music": {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 150, 230, 300, 20), "handle_scale": 1.0},
        "sfx": {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 150, 330, 300, 20), "handle_scale": 1.0}
    }

    dragging_music = dragging_sfx = False
    running = True

    while running:
        screen.blit(BOARD_BG, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        title_surf = font.render("Settings", True, WHITE)
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100)))

        # Music volume slider
        for key, slider in sliders.items():
            rect = slider["rect"]
            is_hovered = rect.collidepoint(mouse_pos)
            color = GRAY if is_hovered else (50, 50, 50)
            pygame.draw.rect(screen, color, rect)

            volume = music_volume if key == "music" else sfx_volume
            handle_x = rect.x + int(volume * rect.width)

            target_scale = 1.5 if is_hovered else 1.0
            slider["handle_scale"] += (target_scale - slider["handle_scale"]) * 0.2
            handle_width = int(20 * slider["handle_scale"])
            handle_height = int(30 * slider["handle_scale"])
            handle_rect = pygame.Rect(
                handle_x - handle_width // 2,
                rect.y - (handle_height - rect.height) // 2,
                handle_width,
                handle_height
            )
            pygame.draw.rect(screen, BLACK, handle_rect)

        music_label = small_font.render("Music Volume", True, WHITE)
        screen.blit(music_label, music_label.get_rect(center=(SCREEN_WIDTH // 2, 200)))
        sfx_label = small_font.render("SFX Volume", True, WHITE)
        screen.blit(sfx_label, sfx_label.get_rect(center=(SCREEN_WIDTH // 2, 300)))

        # more btns
        for btn in buttons:
            draw_button(screen, btn, mouse_pos, small_font, default_color=BLACK, hover_color=GRAY)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sliders["music"]["rect"].collidepoint(mouse_pos):
                    dragging_music = True
                elif sliders["sfx"]["rect"].collidepoint(mouse_pos):
                    dragging_sfx = True
                else:
                    for btn in buttons:
                        if btn["rect"].collidepoint(mouse_pos) and btn["action"] == "back":
                            running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_music = dragging_sfx = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, _ = event.pos
                if dragging_music:
                    music_volume = max(0.0, min(1.0, (mouse_x - sliders["music"]["rect"].x) / sliders["music"]["rect"].width))
                    pygame.mixer.music.set_volume(music_volume)
                    pygame.volume_settings["music"] = music_volume
                if dragging_sfx:
                    sfx_volume = max(0.0, min(1.0, (mouse_x - sliders["sfx"]["rect"].x) / sliders["sfx"]["rect"].width))
                    pygame.volume_settings["sfx"] = sfx_volume

        clock.tick(60)



# difficulty settings menu
def show_difficulty_menu(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT_PATH, 32)
    small_font = pygame.font.Font(FONT_PATH, 24)

    buttons = [
        {"label": "Easy", "rect": pygame.Rect(SCREEN_WIDTH // 2 - 100, 200, 200, 60), "value": "easy", "scale": 1.0, "hovered": False},
        {"label": "Medium", "rect": pygame.Rect(SCREEN_WIDTH // 2 - 100, 300, 200, 60), "value": "medium", "scale": 1.0, "hovered": False},
        {"label": "Hard", "rect": pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 60), "value": "hard", "scale": 1.0, "hovered": False},
        {"label": "Back", "rect": pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 60), "value": None, "scale": 1.0, "hovered": False}
    ]

    running = True
    while running:
        screen.blit(BOARD_BG, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        title_surf = font.render("Select AI Difficulty", True, WHITE)
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH//2, 100)))

        for btn in buttons:
            draw_button(screen, btn, mouse_pos, small_font, default_color=BLACK, hover_color=GRAY)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                for btn in buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        return btn["value"]

# game over screen
def show_game_over(screen, winner_name):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 40)

    buttons = [
        {"label": "Back to Menu", "rect": pygame.Rect(SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 + 50, 250, 50),
         "action": "back", "scale": 1.0, "hovered": False}
    ]

    running = True
    while running:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        winner_surf = font.render(f"{winner_name} Wins!", True, WHITE)
        screen.blit(winner_surf, winner_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3)))

        for btn in buttons:
            draw_button(screen, btn, mouse_pos, small_font, default_color=GRAY, hover_color=(80,80,80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                return
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                for btn in buttons:
                    if btn["rect"].collidepoint(mouse_pos) and btn["action"]=="back":
                        running=False

# main menu 
def show_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Arcane Duel")
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT_PATH, 40)
    small_font = pygame.font.Font(FONT_PATH, 24)

    buttons = [
        {"label": "Start Game", "rect": pygame.Rect(SCREEN_WIDTH//2-100, 300, 200, 60), "action":"start", "scale":1.0, "hovered":False},
        {"label": "Settings", "rect": pygame.Rect(SCREEN_WIDTH//2-100, 360, 200, 60), "action":"settings", "scale":1.0, "hovered":False},
        {"label": "Quit", "rect": pygame.Rect(SCREEN_WIDTH//2-100, 420, 200, 60), "action":"quit", "scale":1.0, "hovered":False}
    ]

    while True:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.join(ASSETS_DIR, "sounds", "gameMusic.mp3"))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

        screen.blit(BOARD_BG, (0,0)) # board background
        mouse_pos = pygame.mouse.get_pos()

        title_surf = font.render("Arcane Duel", True, WHITE)
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH//2, 150)))

        # draw buttons
        for btn in buttons:
            draw_button(screen, btn, mouse_pos, small_font, default_color=BLACK, hover_color=GRAY)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        if btn["action"]=="start":
                            difficulty = show_difficulty_menu(screen)
                            if difficulty:
                                pygame.mixer.music.stop()
                                result = run_game(screen, ai_difficulty=difficulty)
                                if result == "main_menu":
                                    break  # go back to menu loop
                                else:
                                    show_game_over(screen, result)
                        elif btn["action"]=="settings":
                            show_settings(screen, from_game=False)
                        elif btn["action"]=="quit":
                            pygame.quit()
                            return



if __name__=="__main__":
    show_menu()
