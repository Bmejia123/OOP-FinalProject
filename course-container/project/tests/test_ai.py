import pytest
from unittest.mock import MagicMock
from game.ai import ai_take_turn

# mock test for ai turn
class MockPlayer:
    def __init__(self, name, health=100, mana=100):
        self.name = name
        self.health = health
        self.max_health = 100
        self.mana = mana
        self.max_mana = 100
        self.effects = []
        self.block = 0
        self.attack_boost = 0
        self.hand = []

    def take_damage(self, amount, attacker=None):
        self.health -= amount


# creating mock cardc
class MockCard:
    def __init__(self, name, cost, card_type, damage=0, heal=0, buff=0):
        self.name = name
        self.cost = cost
        self.card_type = card_type
        self.damage = damage
        self.heal_amount = heal  
        self.buff_value = buff   
        self.play = MagicMock()

    def __repr__(self):
        return f"{self.name} ({self.card_type}, Cost: {self.cost})"


#test cases here
def test_no_playable_cards():
    ai = MockPlayer("AI", mana=0)
    enemy = MockPlayer("Enemy")
    ai.hand = [
        MockCard("Slash", cost=30, card_type="attack", damage=20)
    ]
    assert ai_take_turn(ai, enemy, difficulty="easy") is False


def test_easy_mode_random_card_played():
    ai = MockPlayer("AI", mana=50)
    enemy = MockPlayer("Enemy")

    c1 = MockCard("A", 10, "attack", damage=5)
    c2 = MockCard("B", 20, "attack", damage=10)
    ai.hand = [c1, c2]

    import random
    random.random = lambda: 0.5 

    result = ai_take_turn(ai, enemy, "easy")

    assert result is True
    assert len(ai.hand) == 1 
    assert ai.mana < 50      


def test_medium_mode_prefers_attack_when_enemy_low():
    ai = MockPlayer("AI", mana=50)
    enemy = MockPlayer("Enemy", health=10)

    heal = MockCard("HealSmall", 10, "heal", heal=5)
    weak_attack = MockCard("Fireball", 10, "attack", damage=4)
    strong_attack = MockCard("Slash", 10, "attack", damage=20)

    ai.hand = [heal, weak_attack, strong_attack]

    result = ai_take_turn(ai, enemy, "medium")

    assert result is True
    assert strong_attack not in ai.hand 


def test_medium_mode_prefers_heal_when_ai_low():
    ai = MockPlayer("AI", mana=50, health=20)
    enemy = MockPlayer("Enemy")

    heal = MockCard("HealBig", 10, "heal", heal=20)
    attack = MockCard("Slash", 10, "attack", damage=20)

    ai.hand = [attack, heal]

    result = ai_take_turn(ai, enemy, "medium")

    assert heal not in ai.hand
    assert heal.play.called


def test_hard_mode_killing_blow_priority():
    ai = MockPlayer("AI", mana=50)
    enemy = MockPlayer("Enemy", health=15)

    low_damage = MockCard("Weak", 10, "attack", damage=5)
    killer = MockCard("Finish", 10, "attack", damage=20)

    ai.hand = [low_damage, killer]

    ai_take_turn(ai, enemy, "hard")

    assert killer.play.called
    assert killer not in ai.hand


def test_hard_mode_buff_has_base_value():
    ai = MockPlayer("AI", mana=50)
    enemy = MockPlayer("Enemy")

    buff = MockCard("Buff", 10, "buff", buff=0)
    attack = MockCard("WeakAtk", 10, "attack", damage=1)

    ai.hand = [buff, attack]

    ai_take_turn(ai, enemy, "hard")

    assert buff.play.called
    assert buff not in ai.hand
