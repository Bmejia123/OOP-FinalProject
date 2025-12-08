import pytest
from models.player import Player
from game.ai import ai_take_turn
from models.card import AttackCard, SupportCard

def test_overkill_damage_does_not_go_negative():
    player = Player("Test")
    player.take_damage(player.health + 50)
    assert player.health == 0  #halth should never go below 0

def test_zero_damage_and_zero_heal():
    player = Player("Test")
    initial_health = player.health
    player.take_damage(0)
    assert player.health == initial_health

    player.health -= 20
    card = SupportCard("ZeroHeal", cost=0, heal=0, boost=0, duration=1, image_path="Back_Card.png")
    card.play(player, player)
    assert player.health == 80  #if heal = 0 dont increase player health

def test_effects_over_multiple_turns():
    player = Player("Test")
    player.effects.append({"type": "dot", "value": 10, "turns": 3})
    initial_health = player.health
    for _ in range(3):
        player.start_turn()
    #dot should apply for 3 turns
    assert player.health == initial_health - 30
    assert len(player.effects) == 0 

def test_ai_vs_player_edge_case():
    ai = Player("AI")
    enemy = Player("Enemy")
    enemy.health = 5 
    ai.mana = 50
    from models.card import AttackCard
    killer_card = AttackCard("Killer", cost=10, damage=10, image_path="Back_Card.png")
    ai.hand = [killer_card]
    result = ai_take_turn(ai, enemy, "hard")
    assert killer_card not in ai.hand
    assert enemy.health <= 0
    assert result is True


def test_multiple_effects_and_ai_interaction():
    player = Player("Test")
    enemy = Player("Enemy")
    player.effects.append({"type": "dot", "value": 5, "turns": 2})
    player.attack_boost = 5
    enemy_attack = 10
    player.take_damage(enemy_attack, enemy)
    assert player.health <= 95 
    player.start_turn()
    assert player.health <= 90
