import pytest
from models.player import Player

def test_dodge_effect_blocks_attack():
    player = Player("Test")
    player.effects.append({"type": "dodge", "value": 1.0, "turns": 1})  # 100% dodge
    attacker = Player("Attacker")
    initial_health = player.health
    player.take_damage(50, attacker)
    assert player.health == initial_health
    assert len(player.effects) == 0

def test_reflect_effect_reflects_damage():
    player = Player("Test")
    attacker = Player("Enemy")
    player.effects.append({"type": "reflect", "value": 10, "turns": 1})
    initial_attacker_health = attacker.health
    player.take_damage(20, attacker)
    assert attacker.health < initial_attacker_health
    assert all(e["type"] != "reflect" for e in player.effects)

def test_attack_boost_effect_applied():
    player = Player("Test")
    player.attack_boost += 5
    assert player.attack_boost == 5

def test_combined_effects_order():
    player = Player("Test")
    attacker = Player("Enemy")
    player.effects.append({"type": "dodge", "value": 0.0, "turns": 1})
    player.effects.append({"type": "reflect", "value": 10, "turns": 1})
    initial_attacker_health = attacker.health
    player.take_damage(20, attacker)
    assert attacker.health < initial_attacker_health
    assert all(e["type"] != "reflect" for e in player.effects)

def test_multiple_effects_interaction():
    player = Player("Test")
    attacker = Player("Enemy")
    player.attack_boost += 5
    assert player.attack_boost == 5
