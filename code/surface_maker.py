import os
from typing import Dict, Tuple
import pygame


class SurfaceMaker:
    # import all the graphics
    # create one surface with the graphics with any size
    # return that image to the blocks or the player

    @staticmethod
    def get_surf(block_type: str, size: Tuple[int, int]):
        block_folder = os.path.join("graphics", "blocks", block_type)
        assets: Dict[str, pygame.Surface] = {}
        for info in os.walk(block_folder):
            for image_name in info[2]:
                image_path = os.path.join(block_folder, image_name)
                surface = pygame.image.load(image_path).convert_alpha()
                assets[image_name.split(".")[0]] = surface

        image = pygame.Surface(size)
        image.set_colorkey("black")

        # top
        image.blit(assets["topleft"], (0, 0))
        image.blit(assets["topright"], (size[0] - assets["topright"].get_width(), 0))
        top_width = (
            size[0] - assets["topleft"].get_width() - assets["topright"].get_width()
        )
        scaled_top_surf = pygame.transform.scale(
            assets["top"], (top_width, assets["top"].get_height())
        )
        image.blit(scaled_top_surf, (assets["topleft"].get_width(), 0))

        # bottom
        image.blit(
            assets["bottomleft"], (0, size[1] - assets["bottomleft"].get_height())
        )
        image.blit(
            assets["bottomright"],
            (
                size[0] - assets["bottomright"].get_width(),
                size[1] - assets["bottomleft"].get_height(),
            ),
        )
        bottom_width = (
            size[0]
            - assets["bottomleft"].get_width()
            - assets["bottomright"].get_width()
        )
        scaled_bottom_surf = pygame.transform.scale(
            assets["bottom"], (bottom_width, assets["bottom"].get_height())
        )
        image.blit(
            scaled_bottom_surf,
            (
                assets["bottomleft"].get_width(),
                size[1] - assets["bottomleft"].get_height(),
            ),
        )

        # left
        left_height = (
            size[1] - assets["topleft"].get_height() - assets["bottomleft"].get_height()
        )
        scaled_left_surf = pygame.transform.scale(
            assets["left"], (assets["left"].get_width(), left_height)
        )
        image.blit(
            scaled_left_surf,
            (
                0,
                assets["topleft"].get_height(),
            ),
        )

        # right
        right_height = (
            size[1]
            - assets["topright"].get_height()
            - assets["bottomright"].get_height()
        )
        scaled_right_surf = pygame.transform.scale(
            assets["right"], (assets["right"].get_width(), right_height)
        )
        image.blit(
            scaled_right_surf,
            (
                size[0] - assets["right"].get_width(),
                assets["topright"].get_height(),
            ),
        )

        # center
        center_width = top_width
        center_height = left_height
        scaled_center_surf = pygame.transform.scale(
            assets["center"], (center_width, center_height)
        )
        image.blit(
            scaled_center_surf,
            (
                assets["left"].get_width(),
                assets["topleft"].get_height(),
            ),
        )

        return image
