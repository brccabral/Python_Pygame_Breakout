import random
from typing import Callable, List, Tuple
import pygame
from surface_maker import SurfaceMaker
from settings import (
    BLOCK_HEIGHT,
    BLOCK_WIDTH,
    COLOR_LEGEND,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)


class GameObject(pygame.sprite.Sprite):
    def __init__(self, groups: List[pygame.sprite.Group]):
        super().__init__(groups)
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.old_rect = self.rect.copy()
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2()
        self.speed = 0

    def input(self):
        pass

    def get_damage(self, amount: int):
        pass


class Player(GameObject):
    def __init__(self, groups: List[pygame.sprite.Group]):
        super().__init__(groups)

        # setup
        self.image = SurfaceMaker.get_surf(
            "player", (WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20)
        )
        self.hearts = 3

        # position
        self.rect = self.image.get_rect(
            midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20)
        )
        self.old_rect = self.rect.copy()
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

    def upgrade(self, upgrade_type: str):
        if upgrade_type == "speed":
            self.speed += 50
        elif upgrade_type == "laser":
            pass
        elif upgrade_type == "heart":
            self.hearts += 1
        elif upgrade_type == "size":
            new_width = self.rect.width * 1.1
            self.image = SurfaceMaker.get_surf("player", (new_width, self.rect.height))
            self.rect = self.image.get_rect(center=self.rect.center)
            self.pos.x = self.rect.x

    def screen_constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        self.pos.x = self.rect.x

    def update(self, dt: float):
        self.input()

        # copy rect before move it
        self.old_rect = self.rect.copy()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.screen_constraint()


class Ball(GameObject):
    def __init__(
        self,
        groups: List[pygame.sprite.Group],
        player: Player,
        blocks: pygame.sprite.Group,
    ):
        super().__init__(groups)

        # collisions
        self.player = player
        self.blocks = blocks

        # setup
        self.image = pygame.image.load("graphics/other/ball.png").convert_alpha()

        # position
        self.rect = self.image.get_rect(midbottom=self.player.rect.midbottom)
        self.old_rect = self.rect.copy()
        self.direction = pygame.math.Vector2((random.choice((1, -1)), -1))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 400

        # active
        self.active = False

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.midbottom == self.player.rect.midtop:
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
            elif self.rect.top >= WINDOW_HEIGHT:
                self.active = False
                self.direction.y = -1
                self.player.hearts -= 1

    def collision(self, direction: str):

        # find overlapping objects
        overlap_sprites: List[GameObject] = pygame.sprite.spritecollide(
            self, self.blocks, False
        )
        if self.rect.colliderect(self.player.rect):
            overlap_sprites.append(self.player)

        if overlap_sprites:
            if direction == "horizontal":
                for sprite in overlap_sprites:
                    if (
                        self.rect.right >= sprite.rect.left
                        and self.old_rect.right <= sprite.old_rect.left
                    ):
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        sprite.get_damage(1)
                        break
                    elif (
                        self.rect.left <= sprite.rect.right
                        and self.old_rect.left >= sprite.old_rect.right
                    ):
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        sprite.get_damage(1)
                        break
            elif direction == "vertical":
                for sprite in overlap_sprites:
                    if (
                        self.rect.bottom >= sprite.rect.top
                        and self.old_rect.bottom <= sprite.old_rect.top
                    ):
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                        sprite.get_damage(1)
                        break
                    elif (
                        self.rect.top <= sprite.rect.bottom
                        and self.old_rect.top >= sprite.old_rect.bottom
                    ):
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                        sprite.get_damage(1)
                        break

    def update(self, dt: float):
        self.input()

        if self.active:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            # copy rect before move it
            self.old_rect = self.rect.copy()

            # horizontal collistions
            self.pos.x += self.direction.x * self.speed * dt
            self.rect.x = self.pos.x
            self.collision("horizontal")
            self.window_collision("horizontal")

            # vertical collistion
            self.pos.y += self.direction.y * self.speed * dt
            self.rect.y = self.pos.y
            self.collision("vertical")
            self.window_collision("vertical")
        else:
            # whenever the ball becomes inactive, it comes back to the player
            self.rect.midbottom = self.player.rect.midtop
            self.pos = pygame.math.Vector2(self.rect.topleft)


class Block(GameObject):
    def __init__(
        self,
        groups: List[pygame.sprite.Group],
        block_type: str,
        pos: Tuple[int, int],
        create_upgrade: Callable[[Tuple[int, int]], None],
    ):
        super().__init__(groups)

        # setup
        self.image = SurfaceMaker.get_surf(
            COLOR_LEGEND[block_type], (BLOCK_WIDTH, BLOCK_HEIGHT)
        )
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()

        # damage information
        self.health = int(block_type)

        # upgrade
        self.create_upgrade = create_upgrade

    def get_damage(self, amount: int):
        self.health -= amount
        if self.health > 0:
            # update the image
            self.image = SurfaceMaker.get_surf(
                COLOR_LEGEND[str(self.health)], (BLOCK_WIDTH, BLOCK_HEIGHT)
            )
        else:
            if random.randint(0, 10) < 3:
                self.create_upgrade(self.rect.center)
            self.kill()


class Upgrade(pygame.sprite.Sprite):
    def __init__(
        self, groups: List[pygame.sprite.Group], upgrade_type: str, pos: Tuple[int, int]
    ):
        super().__init__(groups)

        self.upgrade_type = upgrade_type
        self.image = pygame.image.load(
            f"graphics/upgrades/{self.upgrade_type}.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(midtop=pos)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300

    def update(self, dt: float):
        self.pos.y += self.speed * dt
        self.rect.y = round(self.pos.y)

        if self.rect.top > WINDOW_HEIGHT + 100:
            self.kill()
