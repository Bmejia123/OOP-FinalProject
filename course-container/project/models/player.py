# models/player.py
from models.deck import Deck
import random

MAX_BLOCK = 50  # cap for block

class Player:
    def __init__(self, name):
        self.name = name
        self.max_health = 100
        self.health = self.max_health
        self.max_mana = 100
        self.mana = self.max_mana
        self.deck = Deck()
        self.hand = [self.deck.draw_card() for _ in range(3)]
        self.block = 0

        # status flags / effects
        self.negate_next_damage = False  # forcefield effect card
        self.attack_boost = 0
        self.effects = []  # list of effect dicts
        self.latest_card_drawn = None
        self.skip_turn = False
        self.extra_turns = 0

  #start turn process effects
    def start_turn(self):

        #apply block from vortex style effects
        block_from_effects = sum(
            e.get("value", 0) 
            for e in self.effects 
            if e.get("type") == "block"
        )
        self.block = min(block_from_effects, MAX_BLOCK)

        #dot + regenerate
        for e in self.effects:
            if e.get("type") == "dot":
                self.take_damage(e.get("value", 0))

            elif e.get("type") == "regen":
                self.health = min(self.max_health, self.health + e.get("value", 0))
                print(f"{self.name} regenerates {e['value']} HP. Health: {self.health}")

        #skip turn for (stun card)
        self.skip_turn = any(e.get("type") == "stun" for e in self.effects)

        # extra turns for timeskip
        self.extra_turns = sum(
            e.get("value", 0)
            for e in self.effects
            if e.get("type") == "extra_turn"
        )

        # Decrement turns
        for e in self.effects:
            e["turns"] -= 1

        #we need to handle expired boosts here and remove them when they are over/expired
        expired_boosts = [e for e in self.effects if e["turns"] == 0 and e.get("type") == "boost"]
        for e in expired_boosts:
            self.attack_boost -= e.get("value", 0)
            if self.attack_boost < 0:
                self.attack_boost = 0

        #remove those expired effects here 
        self.effects = [e for e in self.effects if e["turns"] > 0]

   #damage logic for block/reflect/dodge etc
    def take_damage(self, amount, attacker=None):
        import random

        # Forcefield negation
        if getattr(self, "negate_next_damage", False):
            print(f"{self.name}'s ForceField negates the damage!")
            self.negate_next_damage = False
            return

        # Dodge effect
        dodge_effect = next((e for e in self.effects if e.get("type") == "dodge"), None)
        if dodge_effect:
            if random.random() < dodge_effect.get("value", 0):
                print(f"{self.name} dodges the attack!")
                # Remove dodge effect after used
                self.effects = [e for e in self.effects if e is not dodge_effect]
                return

        # Reflect effect
        reflect_effect = next((e for e in self.effects if e.get("type") == "reflect"), None)
        if reflect_effect and attacker:
            print(f"{self.name} reflects the attack back to {attacker.name}!")
            attacker.take_damage(amount)
            # Remove the reflect effect after used
            self.effects = [e for e in self.effects if e is not reflect_effect]
            return

        # Block calculation
        blocked = min(self.block, amount)
        self.block -= blocked
        damage_taken = amount - blocked
        self.health -= damage_taken

        # Ensure health never goes below 0
        self.health = max(self.health, 0)

        print(f"{self.name} takes {damage_taken} damage. Health: {self.health}")




    #block math when we gain block
    def add_block(self, amount):
        self.block = min(self.block + amount, MAX_BLOCK)
        print(f"{self.name} gains {amount} block. Current block: {self.block}")

   #drawing cards
    def draw_card(self):
        card = self.deck.draw_card()
        if card:
            self.hand.append(card)
            self.latest_card_drawn = card
        return card