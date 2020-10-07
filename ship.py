import pygame


class Ship():
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        #  Сохранение вещественной координаты центра коробля
        self.x = float(self.rect.x)

        #     Флаг перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #     Обновляет позицию корабля с учетом флага
        # Обновляется атрибут х, а не rect

        if self.moving_right:
            self.rect.x += 1
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.rect.x -= 1
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
    #     Обновление атрибута rect на основании self.x
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)
