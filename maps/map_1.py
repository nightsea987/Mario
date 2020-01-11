import pygame
from Surface import Surface
from Surface import Ground

BLOCK_WIDTH, BLOCK_HEIGHT = 16, 16
TUBE_WIDTH = 32

ground2 = Surface(1136, 208, 1375 - 1136, 239 - 208, "brown")
ground3 = Surface(1424, 208, 2447 - 1424, 239 - 208, "brown")
ground4 = Surface(2480, 208, 3583 - 2480, 239 - 208, "brown")

blocks = [
    Surface(256, 144, BLOCK_WIDTH, BLOCK_HEIGHT, "brown"),
    Surface(320, 144, BLOCK_WIDTH, BLOCK_HEIGHT, "brown"),
    Surface(336, 144, BLOCK_WIDTH, BLOCK_HEIGHT, "yellow"),
    Surface(352, 144, BLOCK_WIDTH, BLOCK_HEIGHT, "brown"),
    Surface(368, 144, BLOCK_WIDTH, BLOCK_HEIGHT, "yellow"),
    Surface(384, 144, BLOCK_WIDTH, BLOCK_HEIGHT, "brown"),
    Surface(352, 80, BLOCK_WIDTH, BLOCK_HEIGHT, "yellow"),
]

tubes = [
    Surface(448, 175, TUBE_WIDTH, 100, "green")
]


surfaces = [ground2, ground3, ground4] + blocks + tubes
