# game/sounds.py
import os
import pygame

pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
PROJECT_DIR = os.path.dirname(BASE_DIR)               
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

sound_files = {
    # attack card sounds
    "BlackHole": "spellCast.wav",
    "Bow&Arrow": "arrow.wav",
    "Fireball": "fireExplosion.wav",
    "Lightning": "electricZap.wav",
    "MagicShot": "spellCast.wav",
    "Slash": "swordSwing.wav",
    "SnakeBite": "snakeBite.wav",

    # defense card sounds
    "Dodge": "dodgeSwoosh.wav",
    "ForceField": "magicShield.wav",
    "Reflect": "reflectZap.wav",
    "Shield": "shieldHit.wav",
    "Vortex": "windSwirl.wav",

    # Support cards sounds
    "HealthPotion": "sparkleHeal.wav",
    "ManaPotion": "powerupChime.wav",
    "AtkBoost": "magicSparkle.wav",
    "TimeSkip": "rewindSwoosh.wav",
    "YouthPotion": "potionDrink.wav",
}


sounds = {}
for card_name, file_name in sound_files.items():
    path = os.path.join(SOUNDS_DIR, file_name)
    if os.path.exists(path):
        sounds[card_name] = pygame.mixer.Sound(path)
    else:
        print(f"Warning: Sound file '{file_name}' for card '{card_name}' not found in {SOUNDS_DIR}")

def play_card_sound(card_name):
    sfx_volume = getattr(pygame, "volume_settings", {}).get("sfx", 0.5)

    if card_name in sounds:
        sound = sounds[card_name]
        sound.set_volume(sfx_volume)
        sound.play()
    else:
        print(f"No sound assigned for card '{card_name}'")
