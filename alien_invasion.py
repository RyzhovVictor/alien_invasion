import sys
import pygame


class AlienInvasion:
    # Класс для управления ресурасами
    def __init__(self):
        # Иницилизирует игру и создает игровые ресурсы
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")
        # Назначение цвета фона
        self.bg_color = (230, 230, 230)

    def run_game(self):
        # Запуск осноговного цикла игры
        while True:
            # Отслеживание события клавиатуры и мыши
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # При каждом проходе цикла перерисовается экран
            self.screen.fill(self.bg_color)

            # Отоброжение последнего прорисованного экрана
            pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
