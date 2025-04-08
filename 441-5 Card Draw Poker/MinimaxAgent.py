import datetime

from Deck import evaluate_hand
import random


class MinimaxAgent:
    def __init__(self, name="Minimax", raise_threshold = 5, call_threshold = 2,base_discard=3, divisor=3, search_depth = 5):
        self.base_discard = base_discard  # 3 yerine
        self.divisor = divisor  # 3 yerine):
        self.name = name
        self.hand = []
        self.decisions = []
        self.deck = None
        self.raise_threshold = raise_threshold
        self.call_threshold = call_threshold
        self.search_depth = search_depth

    def set_deck(self, deck):
        self.deck = deck

    def __str__(self):
        return self.name


    # def decide_action(self, hand):
    #     self.hand = hand
    #     score = evaluate_hand(hand)
    #
    #     if score[0] >= self.raise_threshold:
    #         action = "raise"
    #     elif score[0] >= self.call_threshold:
    #         action = "call"
    #     else:
    #         action = "fold"
    #
    #     return action

    def decide_action(self, hand):
        self.hand = hand
        score = evaluate_hand(hand)

        # Derinlikli analiz
        if self.search_depth > 0:
            best_action = self._minimax_search(hand, self.search_depth)
            return best_action

        # Fallback stratejisi
        if score[0] >= 6:  # Full House+
            return "raise"
        elif score[0] >= 3:  # Three of a Kind+
            return "call" if self.opponent_aggression < 0.7 else "fold"
        else:
            return "fold"

    def _minimax_search(self, hand, depth):
        """Recursive minimax araması"""
        # Basitleştirilmiş implementasyon
        if depth == 0 or len(hand) == 0:
            return "call"  # Varsayılan aksiyon

        # Burada gerçek minimax implementasyonu olmalı
        return random.choice(["raise", "call", "fold"])

    def decide_draw(self, hand):
        # self.hand = hand
        # score = evaluate_hand(hand)
        #
        # to_discard = self.base_discard - score[0] // self.divisor
        #
        # discard = random.sample(range(5), min(max(0, to_discard), 4))
        #
        # new_cards = self.deck.draw(len(discard))
        #
        # return discard
        score = evaluate_hand(hand)[0]
        if score >= 7:  # Çok güçlü eller
            return random.sample(range(5), 1)  # 1 kart ata (flush/straight arayışı)
        elif score >= 4:
            return random.sample(range(5), 2)  # Orta ellerde 2 kart
        else:
            return random.sample(range(5), 3)  # Zayıf ellerde maksimum discard
