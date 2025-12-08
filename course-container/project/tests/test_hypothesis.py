# tests/test_hypothesis.py
import pytest
import pygame
from unittest.mock import MagicMock, patch
from hypothesis import given, strategies as st

from models.player import Player
from game.ai import ai_take_turn
from models.card import AttackCard, SupportCard

#test Player.take_damage() make sure damage never goes bellow 0 
@given(st.integers(min_value=0, max_value=200))
def test_take_damage_never_negative(damage):
    player = Player("Test")
    initial_health = player.health
    player.take_damage(damage)
    assert 0 <= player.health <= initial_health

# test start_turn applies DOT effects correctly
@given(st.integers(min_value=0, max_value=50))
def test_start_turn_effects_apply_dot(damage):
    player = Player("Test")
    player.effects.append({"type": "dot", "value": damage, "turns": 1})
    initial_health = player.health
    player.start_turn()
    assert player.health <= initial_health
    #dot effect should be removed after finished
    assert len(player.effects) == 0

#test AttackCard damage within bounds
@given(st.integers(min_value=0, max_value=50))
def test_attack_card_damage_bounds(damage):
    target = Player("Target")
    caster = Player("Caster")
    dummy_surface = pygame.Surface((100, 150))  #mocking image/surface
    with patch("pygame.image.load", return_value=dummy_surface):
        card = AttackCard("Strike", cost=5, damage=damage, image_path="")
    card.play(target, caster=caster)
    expected_health = max(0, target.max_health - damage)
    assert target.health == expected_health

#test support card damage within bounds
@given(st.integers(min_value=0, max_value=100), st.integers(min_value=0, max_value=50))
def test_support_card_heal_within_bounds(current_health, heal_amount):
    caster = Player("Caster")
    caster.health = current_health
    dummy_surface = pygame.Surface((100, 150))
    with patch("pygame.image.load", return_value=dummy_surface):
        card = SupportCard("Potion", cost=5, heal=heal_amount, boost=0, duration=1, image_path="")
    card.play(caster, caster)
    assert 0 <= caster.health <= caster.max_health

# test ai make sure it always returns boolean true/false
@given(st.integers(min_value=0, max_value=100), st.integers(min_value=0, max_value=100))
def test_ai_turn_returns_boolean(ai_mana, enemy_health):
    class MockCard:
        def __init__(self, name="Card", cost=5, card_type="attack", damage=10):
            self.name = name
            self.cost = cost
            self.card_type = card_type
            self.damage = damage
            self.play = MagicMock()

    class MockAI(Player):
        def __init__(self):
            super().__init__("AI")
            self.mana = ai_mana
            self.hand = [MockCard()]

    class MockEnemy(Player):
        def __init__(self):
            super().__init__("Enemy")
            self.health = enemy_health

    ai = MockAI()
    enemy = MockEnemy()
    result = ai_take_turn(ai, enemy, "easy")
    assert isinstance(result, bool)
