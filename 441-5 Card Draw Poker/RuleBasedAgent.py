import datetime

from Deck import evaluate_hand
import random


class RuleBasedAgent:
    def __init__(self, name="RuleBased", discard_threshold = 7):
        self.name = name
        self.hand = []
        self.decisions = []
        self.discard_threshold = discard_threshold
        self.deck = None  # Oyun başında set edilecek
        self.conservative_mode = False

    def __str__(self):
        return self.name

    def set_deck(self, deck):
        """Deste referansını ayarlar"""
        self.deck = deck

    def decide_draw(self, hand):
        self.hand = hand
        score = evaluate_hand(hand)

        if score[0] >= self.discard_threshold: #skor thresholddan yuksekse discard yapma
            discard = []
        else:
            discard = random.sample(range(5), 2)


        new_cards = self.deck.draw(len(discard)) if discard else []
        return discard

    def decide_action(self, hand):
        self.hand = hand
        score = evaluate_hand(hand)

        # Katı kurallara dayalı strateji
        if score[0] >= 8:  # Straight Flush veya daha iyisi
            action = "raise"
        elif score[0] >= 5:  # Flush veya daha iyisi
            action = "call" if self.chips > 100 else "fold"  # Chip durumuna göre
        elif score[0] >= 2 and len([c for c in hand if c['rank'] in ['J', 'Q', 'K', 'A']]) >= 2:
            action = "call"  # Yüksek kartlarla sınırlı call
        else:
            action = "fold"

        return action