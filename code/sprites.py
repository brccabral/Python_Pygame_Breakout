import random
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

    def screen_constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        self.pos.x = self.rect.x

    def update(self, dt: float):
        self.input()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.screen_constraint()


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups: List[pygame.sprite.Group], player: pygame.sprite.Sprite):
        super().__init__(groups)

        # collisions
        self.player = player

        # setup
        self.image = pygame.image.load("graphics/other/ball.png").convert_alpha()

        # position
        self.rect = self.image.get_rect(midbottom=self.player.rect.midbottom)
        self.direction = pygame.math.Vector2((random.choice((1, -1)), -1))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 400

        # active
        self.active = False

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.active = True

    def window_collision(self, direction: str):
        if direction == "horizontal":
            if self.rect.left <= 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1
            elif self.rect.right >= WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
                self.pos.x = self.rect.x
                self.direction.x *= -1
        if direction == "vertical":
            if self.rect.top <= 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1
            elif self.rect.bottom >= WINDOW_HEIGHT:
                self.active = False
                self.direction.y = -1

    def collision(self):
        pass

    def update(self, dt: float):
        self.input()

        if self.active:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.pos.x += self.direction.x * self.speed * dt
            self.rect.x = self.pos.x
            self.window_collision("horizontal")

            self.pos.y += self.direction.y * self.speed * dt
            self.rect.y = self.pos.y
            self.window_collision("vertical")
        else:
            # whenever the ball becomes inactive, it comes back to the player
            self.rect.midbottom = self.player.rect.midtop
            self.pos = pygame.math.Vector2(self.rect.topleft)
