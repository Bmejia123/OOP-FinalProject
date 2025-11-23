#models/deck.py
import random
from models.card import AttackCard, DefenseCard, SupportCard

class Deck:
    def __init__(self):
        self.cards = [
            #can add effects here for all the types of cards and files aswell
            AttackCard("Fireball", 20, 15, "attack_cards/FireBall.png"),
            AttackCard("Lightning", 35, 25, "attack_cards/Lightning.png"),
            AttackCard("Slash", 30, 25, "attack_cards/Slash.png"),

            DefenseCard("ForceField", 50, 9999, "defense_cards/ForceField.png"),  # block next damage completely
            DefenseCard("Shield", 10, 15, "defense_cards/Shield.png"),
            DefenseCard("Vortex", 20, 5, "defense_cards/Vortex.png"),  # 5 block for 3 turns

            SupportCard("HealthPotion", 10, heal=5, duration=3, image_path="support_cards/HealthPotion.png"),
            SupportCard("AtkBoost", 25, boost=10, duration=2, image_path="support_cards/AtkBoost.png"),
            SupportCard("ManaPotion", 0, mana=15, image_path="support_cards/ManaPotion.png"),
        ]

        # duplicate each card 3 times (temp until moe cards made)
        self.cards = self.cards * 3  # total 27 cards

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        """Draw the top card from the deck."""
        if self.cards:
            return self.cards.pop(0)
        return None
