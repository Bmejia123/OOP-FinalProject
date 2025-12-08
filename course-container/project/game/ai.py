import random

def ai_take_turn(ai_player, opponent, difficulty):


    #Very simple ai implemenation
    #3 ai tiers easy, medium, hard
    #easy : random mostly
    #medium : picks good cards with simple properties
    #hard: makes some stronger and more strategic choices considering damage and all properties

    playable_cards = [c for c in ai_player.hand if c.cost <= ai_player.mana]
    if not playable_cards:
        return False

    card_to_play = None

    if difficulty == "easy":
        if random.random() < 0.25:
            return False
        card_to_play = random.choice(playable_cards)

    elif difficulty == "medium":
        #heuristic scoring: attack on low enemy HP, heal if self low, buffs otherwise
        best_score = -float('inf')
        for c in playable_cards:
            score = 0
            if c.card_type == "attack":
                score = getattr(c, "damage", 0)
                if opponent.health <= 20:  # try finishing move
                    score += 10
            elif c.card_type == "heal":
                score = getattr(c, "heal_amount", 0)
                if ai_player.health <= 30:
                    score += 10
            elif c.card_type == "buff":
                score = getattr(c, "buff_value", 0)
            if score > best_score:
                best_score = score
                card_to_play = c

    elif difficulty == "hard":
        #considers attack, heal, and buffs intelligently
        best_score = -float('inf')
        for c in playable_cards:
            score = 0
            if c.card_type == "attack":
                score = getattr(c, "damage", 0)
                if opponent.health <= getattr(c, "damage", 0):
                    score += 20  #priotizses that the killing blow is done
            elif c.card_type == "heal":
                score = getattr(c, "heal_amount", 0)
                if ai_player.health <= 50:
                    score += 15  # prioritize healing when low
            elif c.card_type == "buff":
                score = getattr(c, "buff_value", 0)
                score += 5  # buffs always slightly valuable
            if score > best_score:
                best_score = score
                card_to_play = c

    # Playing the card 
    if card_to_play and hasattr(card_to_play, "play"):
        if card_to_play.card_type == "attack":
            card_to_play.play(opponent, ai_player)
        else:
            card_to_play.play(ai_player, ai_player)

        ai_player.mana -= card_to_play.cost
        ai_player.hand.remove(card_to_play)
        return True

    return False
