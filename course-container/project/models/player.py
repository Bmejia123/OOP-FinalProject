#models/player.py
from models.deck import Deck

MAX_BLOCK = 50  #cap for block

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
        self.negate_next_damage = False  # forcefield effect
        self.attack_boost = 0
        self.effects = []  # multitun effects here
        self.latest_card_drawn = None  #track the most recently drawn card

    def start_turn(self):
        block_from_effects = sum(e["value"] for e in self.effects if e["type"] == "block")
        self.block = min(block_from_effects, MAX_BLOCK)

        for e in self.effects:
            e["turns"] -= 1
        self.effects = [e for e in self.effects if e["turns"] > 0]

    def take_damage(self, amount):
        if self.negate_next_damage:
            print(f"{self.name}'s ForceField negates the damage!")
            self.negate_next_damage = False
            return

        damage_taken = max(0, amount - self.block)
        self.block = max(0, self.block - amount)
        self.health -= damage_taken
        print(f"{self.name} takes {damage_taken} damage. Health: {self.health}")

    def add_block(self, amount):
        self.block = min(self.block + amount, MAX_BLOCK)
        print(f"{self.name} gains {amount} block. Current block: {self.block}")

    def draw_card(self):
        card = self.deck.draw_card()
        if card:
            self.hand.append(card)
            self.latest_card_drawn = card  # mark it asdrawn the latest 
        return card  # <-- return the card, not self

