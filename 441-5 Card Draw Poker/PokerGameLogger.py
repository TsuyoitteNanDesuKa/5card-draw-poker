import datetime
import json


class PokerLogger:
    def __init__(self):
        self.session_log = {
            'metadata': {
                'start_time': datetime.now().isoformat(),
                'player_types': {}
            },
            'games': []
        }

    def log_game(self, game_data):
        self.session_log['games'].append(game_data)

    def save_log(self, filename=None):
        if not filename:
            filename = f"poker_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w') as f:
            json.dump(self.session_log, f, indent=2)

        print(f"Log saved to {filename}")
        return filename