from pydoc import plain
import random
from typing import List, Tuple
import pygame
import sys
import time
from sprites import Ball, Block, GameObject, Player, Projectile, Upgrade
from settings import (
    BLOCK_HEIGHT,
    BLOCK_MAP,
    BLOCK_WIDTH,
    GAP_SIZE,
    TOP_OFFSET,
    UPGRADES,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FRAMERATE,
)


class Game:
    def __init__(self):

        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()

        # background
        self.bg = self.create_bg()

        # sprites group
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.upgrade_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()

        # sprites
        self.player = Player([self.all_sprites])
        self.stage_setup()
        self.ball = Ball([self.all_sprites], self.player, self.block_sprites)

        # hearts
        self.heart_surface = pygame.image.load(
            "graphics/other/heart.png"
        ).convert_alpha()

        # projectile
        self.projectile_surf = pygame.image.load(
            "graphics/other/projectile.png"
        ).convert_alpha()
        self.can_shoot = True
        self.shoot_time = 0

        # crt
        self.crt = CRT()

    def laser_timer(self):
        if pygame.time.get_ticks() - self.shoot_time >= 500:
            self.can_shoot = True

    def create_projectile(self):
        for projectile in self.player.laser_rects:
            Projectile(
                [self.all_sprites, self.projectile_sprites],
                projectile.midtop - pygame.math.Vector2(0, 0),
                self.projectile_surf,
            )

    def projectile_collisions(self):
        for projectile in self.projectile_sprites:
            overlap_sprites: List[GameObject] = pygame.sprite.spritecollide(
                projectile, self.block_sprites, False
            )
            if overlap_sprites:
                for sprite in overlap_sprites:
                    sprite.get_damage(1)
                projectile.kill()

    def create_upgrade(self, pos: Tuple[int, int]):
        upgrade_type = random.choice(UPGRADES)
        Upgrade([self.all_sprites, self.upgrade_sprites], upgrade_type, pos)

    def upgrade_collisions(self):
        overlap_sprites: List[Upgrade] = pygame.sprite.spritecollide(
            self.player, self.upgrade_sprites, True
        )
        for sprite in overlap_sprites:
            self.player.upgrade(sprite.upgrade_type)

    def display_hearts(self):
        for i in range(self.player.hearts):
            x = i * (self.heart_surface.get_width() + 2) + 2
            self.display_surface.blit(self.heart_surface, (x, 4))

    def create_bg(self):
        bg_original = pygame.image.load("graphics/other/bg.png").convert()
        scale_factor = WINDOW_HEIGHT / bg_original.get_height()
        w = bg_original.get_width() * scale_factor
        h = bg_original.get_height() * scale_factor
        scaled_bg = pygame.transform.scale(bg_original, (w, h))
        return scaled_bg

    def stage_setup(self):
        for row_index, row in enumerate(BLOCK_MAP):
            y = row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2 + TOP_OFFSET
            for col_index, col in enumerate(row):
                x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                if col != " ":
                    Block(
                        [self.all_sprites, self.block_sprites],
                        col,
                        (x, y),
                        self.create_upgrade,
                    )

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get([pygame.QUIT, pygame.KEYDOWN]):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.can_shoot:
                            self.create_projectile()
                            self.can_shoot = False
                            self.shoot_time = pygame.time.get_ticks()

            if self.player.hearts <= 0:
                pygame.quit()
                sys.exit()

            # draw background
            self.display_surface.blit(self.bg, (0, 0))

            # update the game
            self.all_sprites.update(dt)
            self.upgrade_collisions()
            self.laser_timer()
            self.projectile_collisions()

            # update UI
            self.all_sprites.draw(self.display_surface)
            self.display_hearts()
            self.crt.draw()

            # update window
            pygame.display.update()
            self.clock.tick(FRAMERATE)


class CRT:
    """Simulates old TV"""

    def __init__(self):
        vignette = pygame.image.load("graphics/other/tv.png").convert_alpha()
        self.scaled_vignette = pygame.transform.scale(
            vignette, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        self.scaled_vignette.set_alpha(random.randint(50, 90))
        self.display_surface.blit(self.scaled_vignette, (0, 0))


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
