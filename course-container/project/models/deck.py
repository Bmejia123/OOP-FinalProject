# models/deck.py
import random
from models.card import AttackCard, DefenseCard, SupportCard

class Deck:
    def __init__(self):
        #here we can add more cards etc
        # attacks cards
        self.attack_templates = [
            ("BlackHole", 40, 30, "attack_cards/BlackHole.png", None, 0, None),
            ("Bow&Arrow", 30, 10, "attack_cards/Bow&Arrow.png", "dot", 3, None),
            ("Fireball", 20, 5, "attack_cards/Fireball.png", "dot", 3, None),
            ("Lightning", 30, 15, "attack_cards/Lightning.png", "stun", 0, 0.5),
            ("MagicShot", 65, 50, "attack_cards/MagicShot.png", None, 0, None),
            ("Slash", 30, 25, "attack_cards/Slash.png", None, 0, None),
            ("SnakeBite", 45, 10, "attack_cards/SnakeBite.png", "dot", 3, None)
        ]

        # defense cards
        self.defense_templates = [
            ("Dodge", 25, 20, "defense_cards/Dodge.png", "dodge", 2, 0.5),
            ("ForceField", 50, 40, "defense_cards/ForceField.png", None, 0, None),
            ("Reflect", 65, 50, "defense_cards/Reflect.png", None, 0, None),
            ("Shield", 10, 15, "defense_cards/Shield.png", None, 0, None),
            ("Vortex", 20, 10, "defense_cards/Vortex.png", None, 3, None)
        ]
        # support
        self.support_templates = [
            ("HealthPotion", 10, 5, 0, 0, 3, "support_cards/HealthPotion.png", False),
            ("ManaPotion", 0, 0, 0, 15, 0, "support_cards/ManaPotion.png", False),
            ("AtkBoost", 25, 0, 10, 0, 2, "support_cards/AtkBoost.png", False),
            ("TimeSkip", 35, 0, 0, 0, 0, "support_cards/TimeSkip.png", True),
            ("YouthPotion", 30, 25, 0, 5, 3, "support_cards/YouthPotion.png", False)
        ]

        #building deck with new instances for each card
        self.cards = []

        #30 attacking cards // can change
        for _ in range(4):  # 7 * 4 = 28
            for tpl in self.attack_templates:
                self.cards.append(self.make_attack(*tpl))

        #2 more
        self.cards.append(self.make_attack(*self.attack_templates[0]))
        self.cards.append(self.make_attack(*self.attack_templates[1]))

        # 9 random defense cards
        for tpl in random.choices(self.defense_templates, k=9):
            self.cards.append(self.make_defense(*tpl))

        # 9 random support cards
        for tpl in random.choices(self.support_templates, k=9):
            self.cards.append(self.make_support(*tpl))

        self.shuffle()

    #new card constructors
    def make_attack(self, name, cost, damage, img, effect, duration, chance):
        return AttackCard(name, cost, damage, img, effect, duration, chance)

    def make_defense(self, name, cost, block, img, effect, duration, chance):
        return DefenseCard(name, cost, block, img, effect, duration, chance)

    def make_support(self, name, cost, heal, boost, mana, duration, img, extra_turn):
        return SupportCard(name, cost, heal, boost, mana, duration, img, extra_turn)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if self.cards:
            return self.cards.pop(0)
        return None
