#models/card.py
import os
import random
import pygame

CARD_WIDTH = 120
CARD_HEIGHT = 160

BASE_DIR = os.path.dirname(os.path.abspath(__file__))    
PROJECT_DIR = os.path.dirname(BASE_DIR)                  
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")        


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
    def __init__(self, name, cost, damage, image_path, effect=None, duration=0, chance=None):
        super().__init__(name, cost, "attack", image_path)
        self.damage = damage
        self.effect = effect
        self.duration = duration
        self.chance = chance

    def play(self, target, caster):
        total_damage = self.damage + getattr(caster, "attack_boost", 0)

        #dot effect (Bow&Arrow, Fireball, SnakeBite)
        if self.effect == "dot":
            target.effects.append({"type": "dot", "value": self.damage, "turns": self.duration})
            print(f"{target.name} will take {self.damage} damage for {self.duration} turns!")

        #stun effect(lightning)
        elif self.effect == "stun":
            if self.chance and random.random() < self.chance:
                target.effects.append({"type": "stun", "turns": 1})
                print(f"{target.name} is stunned!")

        #instant damage
        else:
            target.take_damage(total_damage, attacker=caster)


# defenseCard class
class DefenseCard(Card):
    def __init__(self, name, cost, block, image_path, effect=None, duration=0, chance=None):
        super().__init__(name, cost, "defense", image_path)
        self.block = block
        self.effect = effect
        self.duration = duration
        self.chance = chance

    def play(self, target, caster):
        if self.name == "ForceField":
            caster.negate_next_damage = True
            print(f"{caster.name} activates ForceField! Damage negated next hit.")

        elif self.name == "Reflect":
            caster.effects.append({"type": "reflect", "value": "full", "turns": 1})
            print(f"{caster.name} will reflect the next attack!")

        elif self.name == "Dodge":
            caster.effects.append({"type": "dodge", "value": 0.5, "turns": 2})
            print(f"{caster.name} has 50% dodge chance for 2 turns!")

        elif self.name == "Vortex":
            caster.effects.append({"type": "block", "value": self.block, "turns": self.duration})
            print(f"{caster.name} gains {self.block} block over {self.duration} turns.")

        else:
            caster.add_block(self.block)


# support card class
class SupportCard(Card):
    def __init__(self, name, cost, heal=0, boost=0, mana=0, duration=0, image_path=None, extra_turn=False):
        super().__init__(name, cost, "support", image_path)
        self.heal = heal
        self.boost = boost
        self.mana = mana
        self.duration = duration
        self.extra_turn = extra_turn

    def play(self, target, caster):
        if self.heal > 0:
            caster.health = min(caster.max_health, caster.health + self.heal)
            print(f"{caster.name} heals {self.heal} HP.")

        if self.mana > 0:
            caster.mana = min(caster.max_mana, caster.mana + self.mana)
            print(f"{caster.name} regains {self.mana} mana.")

        if self.boost > 0:
            caster.attack_boost = getattr(caster, "attack_boost", 0) + self.boost
            caster.effects.append({"type": "boost", "value": self.boost, "turns": self.duration})
            print(f"{caster.name} gets +{self.boost} attack for {self.duration} turns.")

        if self.extra_turn:
            caster.effects.append({"type": "extra_turn", "value": 1, "turns": 1})
            print(f"{caster.name} will act twice next turn!")
