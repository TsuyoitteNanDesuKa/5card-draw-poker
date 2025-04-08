import random


class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        self.reset()

    def build(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def draw(self, n):
        if len(self.cards) < n:
            self.reset()  # Deste tükendiğinde otomatik reset
            #print("Deste yeniden karıldı!")  # Debug için
        return [self.cards.pop() for _ in range(min(n, len(self.cards)))]

    def reset(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
        random.shuffle(self.cards)


def evaluate_hand(hand):
        rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                      '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        suits = [card['suit'] for card in hand]
        ranks = sorted([rank_order[card['rank']] for card in hand], reverse=True)

        def is_flush():
            return len(set(suits)) == 1

        def is_straight():
            return (len(set(ranks)) == 5 and (max(ranks) - min(ranks) == 4)) or (ranks == [14, 5, 4, 3, 2])

        if ranks == [14, 5, 4, 3, 2]: ranks = [5, 4, 3, 2, 1]

        if is_flush() and is_straight():
            return (9, max(ranks)) if max(ranks) == 14 else (8, max(ranks))
        elif any(ranks.count(r) == 4 for r in set(ranks)):
            return (7, [r for r in set(ranks) if ranks.count(r) == 4][0])
        elif len(set(ranks)) == 2 and 3 in [ranks.count(r) for r in set(ranks)]:
            return (6, max(ranks))
        elif is_flush():
            return (5, ranks)
        elif is_straight():
            return (4, max(ranks))
        elif any(ranks.count(r) == 3 for r in set(ranks)):
            return (3, max([r for r in set(ranks) if ranks.count(r) == 3]))
        elif sum(ranks.count(r) == 2 for r in set(ranks)) == 2:
            return (2, sorted([r for r in set(ranks) if ranks.count(r) == 2], reverse=True))
        elif any(ranks.count(r) == 2 for r in set(ranks)):
            return (1, max([r for r in set(ranks) if ranks.count(r) == 2]))
        else:
            return (0, ranks)