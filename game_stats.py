class GameStats():
    """ Отслеживание статистики для игры Alien Invasion"""

    def __init__(self, ai_game):
        """Иницилизирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Игра Alien Invasion запускается в активном состоянии
        self.game_active = True

    def reset_stats(self):
        """Иницилизирует статистику, изменяющую в ходе игры"""
        self.ships_left = self.settings.ship_limit
