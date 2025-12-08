import pytest
from models.player import Player, MAX_BLOCK

def test_take_damage_with_block():
    player = Player("Test")
    player.block = 20
    player.take_damage(25)
    assert player.health == 95
    assert player.block == 0  # 20 blocked, 5 taken

def test_forcefield_negates_damage():
    player = Player("Test")
    player.negate_next_damage = True
    player.take_damage(50)
    assert player.health == 100
    assert not player.negate_next_damage

def test_add_block_capped():
    player = Player("Test")
    player.add_block(MAX_BLOCK + 10)
    assert player.block == MAX_BLOCK

def test_start_turn_dot_and_expired_boost():
    player = Player("Test")
    player.effects.append({"type": "dot", "value": 10, "turns": 1})
    player.effects.append({"type": "boost", "value": 5, "turns": 1})
    player.attack_boost = 5
    player.start_turn()
    #dot applied
    assert player.health == 90
    # boost expired
    assert player.attack_boost == 0
    # effects removed
    assert len(player.effects) == 0 


def test_draw_card_adds_to_hand():
    player = Player("Test")
    initial_hand = len(player.hand)
    player.draw_card()
    assert len(player.hand) == initial_hand + 1
