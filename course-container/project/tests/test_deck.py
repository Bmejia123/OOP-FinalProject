import pytest
from models.deck import Deck
from models.card import AttackCard, DefenseCard, SupportCard

def test_deck_initialization():
    deck = Deck()
    assert len(deck.cards) > 0

def test_draw_card_removes_card_from_deck():
    deck = Deck()
    top_card = deck.cards[0]
    card = deck.draw_card()
    assert card == top_card
    assert len(deck.cards) == len(deck.cards)  # one less than before

def test_make_attack_returns_attack_card():
    from models.deck import Deck
    deck = Deck()
    card = deck.make_attack("Slash", 10, 20, "Back_Card.png", None, 0, None)
    assert isinstance(card, AttackCard)

def test_make_defense_returns_defense_card():
    deck = Deck()
    card = deck.make_defense("Shield", 5, 10, "Back_Card.png", None, 0, None)
    assert isinstance(card, DefenseCard)

def test_make_support_returns_support_card():
    deck = Deck()
    card = deck.make_support("HealthPotion", 5, 20, 0, 0, 2, "Back_Card.png", False)
    assert isinstance(card, SupportCard)
