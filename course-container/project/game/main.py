# game/main.py
import pygame
from models.player import Player
from game.gui import draw_game, CARD_WIDTH, CARD_HEIGHT, CARD_SPACING, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH, BOARD_BG

pygame.init()
#initialize mixer and play background music
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/gameMusic.mp3")
pygame.mixer.music.set_volume(0.5)  # music volume
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

    # drawing starting cards can change here (initilly 3)
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
        draw_game(screen, players, current_turn)
        pygame.display.flip()
        clock.tick(60)

    return winner

# main menu
def show_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Card Battle Game")
    clock = pygame.time.Clock()

    font = pygame.font.Font(FONT_PATH, 40)
    small_font = pygame.font.Font(FONT_PATH, 24)

    running = True
    while running:
        screen.blit(BOARD_BG, (0, 0))  # can change backgound here


        title_surf = font.render("Card Battle Game", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surf, title_rect)

        # start button
        start_surf = small_font.render("Start Game", True, WHITE)
        start_rect = start_surf.get_rect(center=(SCREEN_WIDTH // 2, 300))
        pygame.draw.rect(screen, (0, 0, 0), start_rect.inflate(20, 10))
        screen.blit(start_surf, start_rect)

        # quit button
        quit_surf = small_font.render("Quit", True, WHITE)
        quit_rect = quit_surf.get_rect(center=(SCREEN_WIDTH // 2, 400))
        pygame.draw.rect(screen, (0, 0, 0), quit_rect.inflate(20, 10))
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
        pygame.draw.rect(screen, GREEN, retry_rect)

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
