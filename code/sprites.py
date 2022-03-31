from typing import List
import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self, groups: List[pygame.sprite.Group]):
        super().__init__(groups)

        # setup
        self.image = pygame.Surface((WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20))
        self.image.fill("red")

        # position
        self.rect = self.image.get_rect(
            midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20)
        )
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self, dt: float):
        self.input()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
