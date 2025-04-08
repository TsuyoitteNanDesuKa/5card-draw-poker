import random
import time
import json
from collections import defaultdict
from datetime import datetime
from Deck import Deck, evaluate_hand
from MCTSAgent import MCTSAgent
from RuleBasedAgent import RuleBasedAgent
from MinimaxAgent import MinimaxAgent


class AIPokerSimulation:
    def __init__(self, iterations=50000):
        self.deck = Deck()
        self.agents = [
            RuleBasedAgent(name="RuleBased"),
            MinimaxAgent(name="Minimax"),
            MCTSAgent(name="MCTS")
        ]

        for player in self.agents:
            if hasattr(player, 'set_deck'):
                player.set_deck(self.deck)  # Kritik ekleme!

        self.iterations = iterations
        self.results = {
            'total_games': 0,
            'wins': defaultdict(int),
            'hand_strengths': defaultdict(int),
            'execution_time': 0,
            'move_times': defaultdict(list)
        }

    def _deal_hands(self):
        """Tüm ajanlara 5 kart dağıt"""
        for agent in self.agents:
            agent.hand = self.deck.draw(5)
            agent.folded = False

    def _betting_round(self):
        """Otomatik bahis turu"""
        active_agents = [a for a in self.agents if not a.folded]

        for agent in active_agents:
            start_time = time.time()
            action = agent.decide_draw(agent.hand)
            decision_time = time.time() - start_time

            self.results['move_times'][str(agent)].append(decision_time)

            if action == "fold":
                agent.folded = True

    def _draw_round(self):
        """Kart değiştirme turu"""
        for agent in self.agents:
            if not agent.folded:
                discard_indices = agent.decide_draw(agent.hand)
                new_cards = self.deck.draw(len(discard_indices))
                agent.hand = [card for i, card in enumerate(agent.hand)
                              if i not in discard_indices] + new_cards

    def _evaluate_round(self):
        """Kazananı belirle ve istatistikleri kaydet"""
        active_agents = [a for a in self.agents if not a.folded]
        if not active_agents:
            return None

        # El değerlendirmelerini yap
        evaluations = []
        for agent in active_agents:
            score = evaluate_hand(agent.hand)
            self.results['hand_strengths'][score[0]] += 1
            evaluations.append((agent, score))

        # En yüksek skorlu ajanı bul
        evaluations.sort(key=lambda x: x[1], reverse=True)
        winner = evaluations[0][0]

        return winner

    def _reset_round(self):
        """Yeni oyun için durumu sıfırla"""
        self.deck = Deck()
        for agent in self.agents:
            agent.hand = []
            agent.folded = False

    def run(self):
        """Ana simülasyon döngüsü"""
        start_time = time.time()

        for i in range(self.iterations):
            self._reset_round()
            self._deal_hands()

            # 1. Bahis turu
            self._betting_round()

            # Kart değiştirme
            self._draw_round()

            # 2. Bahis turu
            self._betting_round()

            # Kazananı belirle
            winner = self._evaluate_round()
            if winner:
                self.results['wins'][str(winner)] += 1
            self.results['total_games'] += 1

            # İlerleme raporu
            if (i + 1) % 100 == 0:
                print(f"Tamamlanan oyun: {i + 1}/{self.iterations}")

        self.results['execution_time'] = time.time() - start_time
        self._analyze_results()
        self._save_results()

    def _analyze_results(self):
        """Ek istatistikleri hesapla"""
        # Ortalama hamle süreleri
        for agent in self.agents:
            times = self.results['move_times'][str(agent)]
            if times:
                avg_time = sum(times) / len(times)
                self.results['move_times'][str(agent)] = avg_time

    def _save_results(self):
        """Sonuçları JSON'a kaydet"""
        filename = f"ai_poker_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Sonuçlar {filename} dosyasına kaydedildi.")

    def print_stats(self):
        """İstatistikleri göster"""
        print("\n=== DETAYLI İSTATİSTİKLER ===")
        print(f"Toplam Oyun: {self.results['total_games']}")
        print(f"Toplam Süre: {self.results['execution_time']:.2f}s")

        print("\n KAZANMA DAĞILIMI:")
        for agent in self.agents:
            wins = self.results['wins'].get(str(agent), 0)
            win_rate = (wins / self.results['total_games']) * 100
            print(f"{str(agent):<15}: {wins} ({win_rate:.1f}%)")

        print("\n ORTALAMA HAMLE SÜRELERİ (ms):")
        for agent in self.agents:
            time = self.results['move_times'].get(str(agent), 0) * 1000
            print(f"{str(agent):<15}: {time:.2f}ms")

        print("\n EL GÜCÜ DAĞILIMI:")
        hand_types = {
            9: "Royal Flush", 8: "Straight Flush", 7: "Four of a Kind",
            6: "Full House", 5: "Flush", 4: "Straight",
            3: "Three of a Kind", 2: "Two Pair", 1: "One Pair", 0: "High Card"
        }
        for score, count in self.results['hand_strengths'].items():
            print(f"{hand_types.get(score, 'Unknown'):<15}: {count}")


# Örnek Kullanım
if __name__ == "__main__":
    print("⚡ AI Poker Simülasyonu Başlıyor...")
    sim = AIPokerSimulation(iterations=50000)
    sim.run()
    sim.print_stats()