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
    def __init__(self, name, cost, damage, image_path, effect=None):   # effect=None is new
        super().__init__(name, cost, "attack", image_path)
        self.damage = damage
        #self.effect = effect 

    def play(self, target, caster):
        """
        if self.name == "Bow&Arrow":
            target.effects.append({"type": "dot", "value": self.damage, "turns": 3})
            print(f"{target.name} will take {self.damage} damage for 3 turns!")
        if self.name == "SnakeBite":
            target.effects.append({"type": "dot", "value": self.damage, "turns": 3})
            print(f"{target.name} will take {self.damage} damage for 3 turns!")
        if self.name == "Fireball":
            target.effects.append({"type": "dot", "value": self.damage, "turns": 3})
            print(f"{target.name} will take {self.damage} damage for 3 turns!") 
            
        if self.effect == "stun":
            self.apply_stun(target)
    def apply_stun(self, target):
        import random
        if random.random() < 0.5:
            target.effects.append({"type": "stun", "turns": 1, "value": None})
            print(f"{target.name} is stunned and will skip their next turn!")
        """
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
        """
        elif self.name == "Reflect":
            caster.effects.append({"type": "reflect", "value": "full", "turns": 1})
            print(f"{caster.name} will reflect the next attack!") 
        elif self.name == "Dodge":
            caster.effects.append({"type": "dodge", "value": 0.5, "turns": 2})
            print(f"{caster.name} has a 50% chance to dodge for 2 turns!")
        """
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
        """
        if self.name == "YouthPotion":
            caster.health = min(caster.max_health, caster.health + 25)
            print(f"{caster.name} heals 25 HP!")
            caster.effects.append({"type": "regen", "value": 5, "turns": 3})
            print(f"{caster.name} will regenerate 5 HP for 3 turns.")
        elif self.name == "TimeSkip":
            caster.effects.append({"type": "extra_turn", "value": 1, "turns": 1})
            print(f"{caster.name} will act twice on their next turn!")
        """
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
