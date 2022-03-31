import pygame
import sys
import time
from sprites import Player
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FRAMERATE


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

        # sprites
        self.player = Player(self.all_sprites)

    def create_bg(self):
        bg_original = pygame.image.load("graphics/other/bg.png").convert()
        scale_factor = WINDOW_HEIGHT / bg_original.get_height()
        w = bg_original.get_width() * scale_factor
        h = bg_original.get_height() * scale_factor
        scaled_bg = pygame.transform.scale(bg_original, (w, h))
        return scaled_bg

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
