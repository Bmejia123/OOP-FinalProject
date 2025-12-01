# models/deck.py
import random
from models.card import AttackCard, DefenseCard, SupportCard

class Deck:
    def __init__(self):
        self.cards = [
            #here we can add more cards etc
            # attacks cards
            AttackCard("BlackHole", 40, 30, "attack_cards/BlackHole.png"),
            AttackCard("Bow&Arrow", 30, 10, "attack_cards/Bow&Arrow.png", effect="dot", duration=3),
            AttackCard("Fireball", 20, 5, "attack_cards/Fireball.png", effect="dot", duration=3),
            AttackCard("Lightning", 30, 15, "attack_cards/Lightning.png", effect="stun", chance=0.5),
            AttackCard("MagicShot", 65, 50, "attack_cards/MagicShot.png"),
            AttackCard("Slash", 30, 25, "attack_cards/Slash.png"),
            AttackCard("SnakeBite", 45, 10, "attack_cards/SnakeBite.png", effect="dot", duration=3),

            # defense cards
            DefenseCard("Dodge", 25, 20, image_path="defense_cards/Dodge.png", effect="dodge", duration=2, chance=0.5),
            DefenseCard("ForceField", 50, 40, image_path="defense_cards/ForceField.png"),
            DefenseCard("Reflect", 65, 50, image_path="defense_cards/Reflect.png"),
            DefenseCard("Shield", 10, 15, "defense_cards/Shield.png"),
            DefenseCard("Vortex", 20, 10, "defense_cards/Vortex.png", duration=3),

            # support
            SupportCard("HealthPotion", 10, heal=5, duration=3, image_path="support_cards/HealthPotion.png"),
            SupportCard("ManaPotion", 0, mana=15, image_path="support_cards/ManaPotion.png"),
            SupportCard("AtkBoost", 25, boost=10, duration=2, image_path="support_cards/AtkBoost.png"),
            SupportCard("TimeSkip", 35, image_path="support_cards/TimeSkip.png", extra_turn=True),
            SupportCard("YouthPotion", 30, heal=25, mana=5, duration=3, image_path="support_cards/YouthPotion.png")
        ]

        # duplicate each card 3 times to fill deck (adjust as needed)
        self.cards = self.cards * 3  # total 48 cards

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        """Draw the top card from the deck."""
        if self.cards:
            return self.cards.pop(0)
        return None
