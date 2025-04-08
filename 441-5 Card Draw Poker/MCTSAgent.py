import datetime
import random
from collections import defaultdict
from itertools import combinations

from Deck import Deck, evaluate_hand


class MCTSAgent:
    def __init__(self, name="MCTS", number_of_simulation = 10):
        self.name = name
        self.hand = []
        self.decisions = []
        self.deck = None
        self.number_of_simulation = number_of_simulation


    def set_deck(self, deck):
        self.deck = deck

    def __str__(self):
        return self.name

    def decide_draw(self, hand):
        self.hand = hand.copy()
        current_score_tuple = evaluate_hand(hand)  # This returns a tuple
        current_score = current_score_tuple[0]  # We use the first element for comparison

        # If we already have a very strong hand, don't discard anything
        if current_score >= 7:  # Adjust threshold based on your scoring system
            return []

        # Generate all possible discard combinations (0-3 cards)
        discard_options = []
        for discard_size in range(0, min(3, len(hand)) + 1):
            discard_options.extend(combinations(range(len(hand)), discard_size))

        # Evaluate each discard option through simulation
        option_scores = defaultdict(list)

        for option in discard_options:
            for _ in range(self.number_of_simulation):
                # Simulate drawing new cards
                simulated_hand = hand.copy()

                # Remove discarded cards
                for index in sorted(option, reverse=True):
                    simulated_hand.pop(index)

                # Draw new cards
                num_to_draw = len(option)
                new_cards = self.deck.draw(num_to_draw) if num_to_draw > 0 else []
                simulated_hand.extend(new_cards)

                # Evaluate the new hand and get the score (first element of tuple)
                score_tuple = evaluate_hand(simulated_hand)
                score = score_tuple[0]
                option_scores[option].append(score)

        # Calculate average improvement for each option
        option_improvements = {}
        for option, scores in option_scores.items():
            avg_score = sum(scores) / len(scores)
            option_improvements[option] = avg_score - current_score

        # Find the option with maximum average improvement
        if option_improvements:  # Check if we have any options
            best_option = max(option_improvements.items(), key=lambda x: x[1])[0]

            # Only discard if improvement is significant
            if option_improvements[best_option] > 0.5:  # Adjust threshold as needed
                return list(best_option)

        return []

    def decide_action(self, hand):
        self.hand = hand
        score = evaluate_hand(hand)

        # Simülasyon tabanlı karar
        if not hasattr(self, 'action_stats'):
            self.action_stats = defaultdict(int)

        # 100 simülasyon yap
        for _ in range(self.number_of_simulation):
            simulated_result = self._simulate_round(hand)
            self.action_stats[simulated_result] += 1

        # En başarılı aksiyonu seç
        action = max(self.action_stats.items(), key=lambda x: x[1])[0]

        # Exploration (%10 rastgele hareket)
        if random.random() < 0.1:
            action = random.choice(["raise", "call", "fold"])

        return action

    def _simulate_round(self, hand):
        """Rastgele oyun sonucu simüle eder"""
        possible_actions = ["raise", "call", "fold"]
        return random.choice(possible_actions)  # Basitleştirilmiş simülasyon

