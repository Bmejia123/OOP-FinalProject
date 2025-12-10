# Python Fantasy Card Game

Team Members: Bernardo, Marshall

Project Description

This card game will be played as a 2 person turned based game using various attack and defend spell cards. All cards are put into a deck which the player can draw from and play one card per turn. A simple health bar system to keep track of the appropriate damage being dealt as well as some sort of mana system to limit what cards can played depending on the cost of them. Also instead of a console game, this will use pygame as a GUI to make it more appealing and interactive. Classes will be the stand point behind this using them for each type of card combined with getters and setters creates modularity when creating new instances. The game will track off of base line numbers rather than percentages, for example if each player had 500 health and you play a defend card to block 50 damage and your opponent plays a attack card for 150 damage your overall health by the start of next turn will be 400.

How to Run

Open terminal/command prompt and navigate to the project folder:

cd C:\Users\berna\Desktop\oop-finalproject\OOP-FinalProject\course-container\project


Run the game:

python -m game.main


Launches the game window via Pygame.

Navigate menus and play the game using the interface.

Run all tests:

python -m pytest tests


Executes unit tests and property-based tests (Hypothesis)

Confirms correctness of player mechanics, AI logic, and edge cases

All 35 tests should pass


Design patterns:

Strategy Pattern
Each card type (Attack, Defense, Support) defines its own play behavior
allows the game to add new card types without modifying existing code
Makes card actions flexible and easy to extend


Factory Method Pattern
make_attack(), make_defense(), make_support() create cards from templates
Centralizes object creation so decks are built consistently and safely
Makes it easy to tweak or balance cards without rewriting logic


State Pattern
Player status effects (stun, poison, regen, block) modify behavior based on current state.
Effects persist across turns and update automatically
Keeps turn logic clean by letting each state control its own rules

File structure:
project/
├── assets/          # images, audio, and other media files used in the game
├── docs/            # Documentation including UML diagrams, design docs, and slides
├── game/            # Main game logic and graphics
├── models/          # Classes and modules representing game entities (Player, Card, Deck, etc.)
├── tests/           # Unit tests and property based tests (Hypothesis)
├── utils/    


Gameplay screenshots and other screenshots are saved in the docs/ folder.

Team Contributions
This is an estimate and not 100%
We each did a bit over everything
Bernardo: Focused more on game loop, graphics, and etc(game.py, gui.py, sounds.py etc, worked on the class files when asked for help by Marshall)
Marshall: Focused on assets, classes, etc.
