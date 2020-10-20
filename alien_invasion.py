import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats


class AlienInvasion:
    # Класс для управления ресурасами
    def __init__(self):
        # Иницилизирует игру и создает игровые ресурсы
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self._create_fleet()
        # Создание экземпляра для хранения игровой статистики
        self.stats = GameStats(self)
        self.screen = pygame.display.set_mode((1400, 800))

        pygame.display.set_caption("Alien Invasion")

        # Назначение цвета фона
        self.bg_color = (230, 230, 230)

    def run_game(self):
        # Запуск осноговного цикла игры
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_aliens()

            self._update_screen()

            #         Удаление снарядов, вышедших за край экрана
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            # print(len(self.bullets))

    # Отслеживание события клавиатуры и мыши
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

            #             Переместить корабль вправо
            self.ship.rect.x += 1

        # При каждом проходе цикла перерисовается экран

        self.screen.fill(self.bg_color)

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        #     Проверка коллизий "прищелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #   Проверить, добрались ли пришельцы до нижнего края экрана
        self._check_alliens_bottom()

    def _ship_hit(self):
        """Обрабатывает столкновение коробля с прищельцами"""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left
            self.stats.ships_left -= 1
        #     Очистка списков прищельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
        #     Создание нового флота и размещения коробля в центре
            self._create_fleet()
            self.ship.center_ship()
        #     Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_alliens_bottom(self):
        """Проверяет, добрались ли прищельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for allien in self.aliens.sprites():
            if allien.rect.bottom >= screen_rect.bottom:
                #             Происходит то же, что и при столкновении с кораблем
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 3 * alien_height - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_bullets(self):
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Отоброжение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
