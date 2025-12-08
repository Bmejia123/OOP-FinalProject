import pytest
from models.card import AttackCard, DefenseCard, SupportCard

class MockTarget:
    def __init__(self, name="Target", health=100, max_health=100):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.effects = []
        self.block = 0
        self.attack_boost = 0
    
    def take_damage(self, amount, attacker=None):
        self.health -= amount
    
    def add_block(self, amount):
        self.block += amount


def test_attack_card_instant_damage():
    target = MockTarget()
    card = AttackCard("Slash", cost=10, damage=20, image_path="Back_Card.png")
    card.play(target, caster=MockTarget())
    assert target.health == 80

def test_attack_card_dot_effect():
    target = MockTarget()
    card = AttackCard("Fireball", cost=10, damage=5, image_path="Back_Card.png", effect="dot", duration=2)
    card.play(target, caster=MockTarget())
    assert any(e['type'] == "dot" for e in target.effects)

def test_defense_card_block():
    caster = MockTarget()
    card = DefenseCard("Shield", cost=5, block=15, image_path="Back_Card.png")
    card.play(caster, caster)
    assert caster.block == 15

def test_support_card_heal_and_boost():
    caster = MockTarget()
    caster.health = 50
    card = SupportCard("HealthPotion", cost=5, heal=30, boost=5, duration=2, image_path="Back_Card.png")
    card.play(caster, caster)
    assert caster.health == 80
    assert caster.attack_boost == 5
