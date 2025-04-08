from Deck import Deck, evaluate_hand
from HumanPlayer import HumanPlayer
from RuleBasedAgent import RuleBasedAgent
from MinimaxAgent import MinimaxAgent
from MCTSAgent import MCTSAgent


class PlayGame:
    def __init__(self):
        self.deck = Deck()
        self.players = [
            HumanPlayer(),
            RuleBasedAgent(),
            MinimaxAgent(),
            MCTSAgent()
        ]

        for player in self.players:
            if hasattr(player, 'set_deck'):
                player.set_deck(self.deck)

        self.folded = []

    def start_game(self):
        print("\n--- Yeni Oyun Başlıyor ---")
        self.deal_hands()
        self.betting_round()
        self.draw_round()
        self.betting_round()
        self.showdown()

    def deal_hands(self):
        for player in self.players:
            player.hand = self.deck.draw(5)

    def betting_round(self):
        print("\n--- Bahis Turu ---")
        for player in self.players:
            if player not in self.folded:
                action = player.decide_action(player.hand)
                print(f"{player}: {action}")
                if action == "fold": self.folded.append(player)

    def draw_round(self):
        print("\n--- Kart Değiştirme Turu ---")
        for player in self.players:
            if player not in self.folded:
                discard = player.decide_draw(player.hand)
                new_cards = self.deck.draw(len(discard))
                player.hand = [card for i, card in enumerate(player.hand) if i not in discard] + new_cards

    def showdown(self):
        print("\n--- Sonuçlar ---")
        active_players = [p for p in self.players if p not in self.folded]
        if not active_players:
            print("Tüm oyuncular fold etti!")
            return

        scores = [(p, evaluate_hand(p.hand)) for p in active_players]
        scores.sort(key=lambda x: x[1], reverse=True)

        for p, s in scores:
            print(f"{p}: {s}")

        print(f"\n🏆 Kazanan: {scores[0][0]} | El Tipi: {self.hand_name(scores[0][1][0])}")

    def hand_name(self, score):
        names = {
            9: "Royal Flush", 8: "Straight Flush", 7: "Four of a Kind",
            6: "Full House", 5: "Flush", 4: "Straight", 3: "Three of a Kind",
            2: "Two Pair", 1: "One Pair", 0: "High Card"
        }
        return names.get(score, "Bilinmeyen")


if __name__ == "__main__":
    game = PlayGame()
    game.start_game()