import pygame
import os

os.chdir('../sprites')
pygame.init()
screen = pygame.display.set_mode((800, 640))


def load_image(name, colorkey=None):
    fullname = name
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

SCALE_D = 3


class Surface:
    def __init__(self, x, y, width, height, color=(0, 0, 0)):
        self.x, self.y, self.width, self.height = x * SCALE_D, y * SCALE_D, width * SCALE_D, height * SCALE_D
        self.left = self.x
        self.right = self.x + self.width
        self.up = self.y
        self.down = self.y + self.height
        self.color = pygame.Color(color)

    def draw(self, screen, SCR_X, SCR_Y):
        self.rect = pygame.Rect((self.x - SCR_X), (self.y - SCR_Y), self.width, self.height)
        pygame.draw.rect(screen, self.color, self.rect, 0)

# class Tube(Surface):
#
class Ground(pygame.sprite.Sprite):
    image = load_image('ground.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Ground.image
        self.rect = self.image.get_rect().move(x, y)
        print(self.rect)
        self.rect.x = x
        self.rect.y = y



#
# class GoldenBlock
#

