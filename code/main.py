import pygame
import sys
import time
from sprites import Ball, Block, Player
from settings import (
    BLOCK_HEIGHT,
    BLOCK_MAP,
    BLOCK_WIDTH,
    GAP_SIZE,
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

        # sprites
        self.player = Player([self.all_sprites])
        self.stage_setup()
        self.ball = Ball([self.all_sprites], self.player, self.block_sprites)


    def create_bg(self):
        bg_original = pygame.image.load("graphics/other/bg.png").convert()
        scale_factor = WINDOW_HEIGHT / bg_original.get_height()
        w = bg_original.get_width() * scale_factor
        h = bg_original.get_height() * scale_factor
        scaled_bg = pygame.transform.scale(bg_original, (w, h))
        return scaled_bg

    def stage_setup(self):
        for row_index, row in enumerate(BLOCK_MAP):
            y = row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
            for col_index, col in enumerate(row):
                x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                if col != " ":
                    Block([self.all_sprites, self.block_sprites], col, (x, y))

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get([pygame.QUIT]):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # update the game
            self.all_sprites.update(dt)

            self.display_surface.blit(self.bg, (0, 0))
            self.all_sprites.draw(self.display_surface)
            # game logic
            pygame.display.update()
            self.clock.tick(FRAMERATE)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
