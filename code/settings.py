import pygame, sys
from pygame.math import Vector2 as vector

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 4

# Layers
Z_LAYERS = {
    'bg_back': 0,
    'bg_mid': 1,
    'bg_front': 2,
    'bg_details': 3,
    'main': 4,
    'fg': 5,
}