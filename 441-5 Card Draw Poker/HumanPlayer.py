import datetime


class HumanPlayer:
    def __init__(self, name="İnsan Oyuncu"):
        self.name = name
        self.hand = []

    def __str__(self):
        return self.name

    def show_hand(self):
        print("\nElinizdeki kartlar:")
        for i, card in enumerate(self.hand):
            print(f"{i + 1}. {card['rank']} {card['suit']}")

    def decide_action(self, hand):
        self.hand = hand
        while True:
            self.show_hand()
            action = input("\nHamlenizi seçin (raise/call/fold): ").strip().lower()
            if action in ['raise', 'call', 'fold']: return action
            print("Geçersiz giriş! Lütfen 'raise', 'call' veya 'fold' yazın.")

    def decide_draw(self, hand):
        self.hand = hand
        self.show_hand()
        while True:
            try:
                discard = input("\nDeğiştirmek istediğiniz kart numaralarını girin (örn: 1 3 5): ")
                indices = [int(n) - 1 for n in discard.split()]
                if len(indices) > 4: raise ValueError("En fazla 4 kart değiştirebilirsiniz")
                if any(not (0 <= i < 5) for i in indices): raise ValueError("Geçersiz kart numarası (1-5 arası olmalı)")
                if len(indices) != len(set(indices)): raise ValueError("Aynı kartı birden fazla kez seçemezsiniz")
                return indices
            except ValueError as e:
                print(f"Hata: {e}. Tekrar deneyin.")
            except:
                print("Geçersiz giriş! Örnek format: '1 3 5'")

    def _log_decision(self, stage, action, score=None):
        log_entry = {
            'stage': stage,
            'hand': [f"{c['rank']}-{c['suit']}" for c in self.hand],
            'action': action,
            'timestamp': datetime.now().isoformat()[:19]  # YYYY-MM-DDTHH:MM:SS
        }
        if score is not None:
            log_entry['score'] = str(score)
        self.decisions.append(log_entry)