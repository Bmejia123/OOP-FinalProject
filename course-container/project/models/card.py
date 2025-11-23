#models/card.py
import pygame
import os

CARD_WIDTH = 120
CARD_HEIGHT = 160

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

class Card:
    def __init__(self, name, cost, card_type, image_path=None):
        self.name = name
        self.cost = cost
        self.card_type = card_type

        if image_path is None:
            image_path = "Back_Card.png"

        full_path = os.path.join(ASSETS_DIR, image_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Card image not found: {full_path}")

        self.image = pygame.image.load(full_path)
        self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))

    def __repr__(self):
        return f"{self.name} ({self.card_type}, Cost: {self.cost})"

# attackCard class
class AttackCard(Card):
    def __init__(self, name, cost, damage, image_path):
        super().__init__(name, cost, "attack", image_path)
        self.damage = damage

    def play(self, target, caster):
        total_damage = self.damage + getattr(caster, "attack_boost", 0)
        target.take_damage(total_damage)

# defenseCard class
class DefenseCard(Card):
    def __init__(self, name, cost, block, image_path):
        super().__init__(name, cost, "defense", image_path)
        self.block = block

    def play(self, target, caster):
        if self.name == "ForceField":
            caster.negate_next_damage = True
            print(f"{caster.name} activates ForceField! Next damage will be negated.")
        elif self.name == "Vortex":
            caster.effects.append({"type": "block", "value": self.block, "turns": 3})
            print(f"{caster.name} gains {self.block} block for 3 turns (Vortex).")
        else:
            caster.add_block(self.block)

# support card class
class SupportCard(Card):
    def __init__(self, name, cost, heal=0, boost=0, mana=0, duration=0, image_path=None):
        super().__init__(name, cost, "support", image_path)
        self.heal = heal
        self.boost = boost
        self.mana = mana
        self.duration = duration

    def play(self, target, caster):
        if self.heal > 0:
            caster.health = min(caster.max_health, caster.health + self.heal)
            print(f"{caster.name} heals {self.heal} HP. Health: {caster.health}")
        if self.mana > 0:
            caster.mana = min(caster.max_mana, caster.mana + self.mana)
            print(f"{caster.name} regains {self.mana} mana. Mana: {caster.mana}")
        if self.boost > 0:
            caster.attack_boost = getattr(caster, "attack_boost", 0) + self.boost
            caster.effects.append({"type": "boost", "value": self.boost, "turns": self.duration})
            print(f"{caster.name} gains +{self.boost} attack for {self.duration} turns.")
