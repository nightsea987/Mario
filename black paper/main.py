import pygame
import os
import pyganim
os.chdir('../sprites')

pygame.init()
pygame.mixer.init()

size = WIDTH, HEIGHT = 800, 630
TILE_WIDTH, TILE_HEIGHT = 16, 16

screen = pygame.display.set_mode(size)


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


def load_level(filename):
    filename = "../maps/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, ' '), level_map))


class Mario(pygame.sprite.Sprite):
    images = {
        "Mario": load_image('small_mario_stand.png', -1)
    }
    ANIMATION_DELAY = 0.1  # скорость смены кадров
    ANIMATION_SMALL_RIGHT = [('mario/r1.png'),
                       ('mario/r2.png'),
                       ('mario/r3.png'),
                       ('mario/r4.png'),
                       ('mario/r5.png')]
    ANIMATION_SMALL_LEFT = [('mario/l1.png'),
                      ('mario/l2.png'),
                      ('mario/l3.png'),
                      ('mario/l4.png'),
                      ('mario/l5.png')]
    # ANIMATION_JUMP_LEFT = [('mario/jl.png', 0.1)]
    # ANIMATION_JUMP_RIGHT = [('mario/jr.png', 0.1)]
    ANIMATION_SMALL_JUMP = [('small_mario_jump.png', 0.1)]
    ANIMATION_SMALL_STAY = [('small_mario_stand.png', 0.1)]

    def __init__(self, x, y, image_name, w=16, h=16):
        super().__init__(heroes)
        w = 12
        self.image = pygame.transform.scale(Mario.images[image_name], (int(w * SCALE_D), int(h * SCALE_D)))

        self.tile_width, self.tile_height = TILE_WIDTH * SCALE_D, TILE_HEIGHT * SCALE_D
        self.pos_x, self.pos_y = x, y

        self.rect = self.image.get_rect().move(self.tile_width * self.pos_x, self.tile_height * self.pos_y)

        # print(id(self.rect) == id(self.image.get_rect()))

        self.maygo_left = True
        self.maygo_right = True
        self.maygo_up = True
        self.maygo_down = True

        self.speed_x = 0
        self.speed_y = 0
        self.check_possible_moves_x()
        self.check_possible_moves_y()
        self.on_ground = False
        self.a_y = 0

    # def update_coords(self):
    #

    def move(self):
        self.rect.x += self.speed_x
        self.check_possible_moves_x()

        self.rect.y += self.speed_y
        self.check_possible_moves_y()

    def check_possible_moves_x(self):
        self.maygo_right, self.maygo_left = False, False

        for sprite in surfaces2:
            if self.rect.colliderect(sprite.rect):
                if self.speed_x > 0:
                    self.maygo_right = False
                    self.rect.x = sprite.rect.x - self.rect.width
                elif self.speed_x < 0:
                    self.maygo_left = False
                    self.rect.x = sprite.rect.x + sprite.rect.width

    def check_possible_moves_y(self):
        self.maygo_up, self.maygo_down = False, False
        for sprite in surfaces2:
            if self.rect.colliderect(sprite.rect):
                if self.speed_y > 0:
                    self.maygo_down = False
                    self.speed_y = 1
                    self.rect.y = sprite.rect.y - self.rect.height
                if self.speed_y < 0:
                    self.maygo_up = False
                    self.speed_y = 1
                    self.rect.y = sprite.rect.y + sprite.rect.height

    def accelerate(self):
        self.speed_y += 55 / FPS


class DecorSprites(pygame.sprite.Sprite):
    sprites = [load_image('small_cloud.png'),
               load_image('small_grass.png', -1),
               load_image('big_grass.png', -1),
               load_image('light_big_grass.png', -1),
               load_image('light_small_grass.png', -1),
               load_image('light_middle_grass.png', -1)]

    def __init__(self, image_type, x, y):
        super().__init__(decoration)

        self.pos_x, self.pos_y = x, y
        self.image1 = DecorSprites.sprites[image_type]
        self.image = pygame.transform.scale(self.image1,
                                            (int(self.image1.get_width() * SCALE_D),
                                             int(self.image1.get_height() * SCALE_D)))
        self.rect = self.image.get_rect().move(
            BLOCK_SIZE * self.pos_x,
            BLOCK_SIZE * self.pos_y - (self.image1.get_height() * SCALE_D - BLOCK_SIZE))

    def update(self):
        # self.rect.x = self.pos_x - SCR_X
        # self.rect.y = self.pos_y - SCR_Y
        pass


class AllBlocks(pygame.sprite.Sprite):
    def __init__(self, image, x, y, w=16, h=16):
        super().__init__(surfaces2)
        self.image = pygame.transform.scale(load_image(image), (int(w * SCALE_D), int(h * SCALE_D)))
        self.tile_width, self.tile_height = TILE_WIDTH * SCALE_D, TILE_HEIGHT * SCALE_D
        self.pos_x, self.pos_y = x, y
        self.rect = self.image.get_rect().move(self.tile_width * self.pos_x,
                                               self.tile_height * self.pos_y)

    def update(self):
        # self.rect.x = self.pos_x
        # self.rect.y = self.pos_y
        # print(self.rect.x, self.rect.y)
        pass


class QBlock(pygame.sprite.Sprite):
    ANIMATION_DELAY = 1  # скорость смены кадров
    ANIMATION_QBLOCK = [('q_block.png'),
                        ('q_block2.png'),
                        ('q_block3.png'),
                        ('q_block2.png')]
    def __init__(self, x, y, w=16, h=16):
        super().__init__(surfaces2)
        self.image = pygame.transform.scale(load_image(QBlock.ANIMATION_QBLOCK[0]), (int(w * SCALE_D), int(h * SCALE_D)))
        self.tile_width, self.tile_height = TILE_WIDTH * SCALE_D, TILE_HEIGHT * SCALE_D
        self.pos_x, self.pos_y = x, y
        self.rect = self.image.get_rect().move(self.tile_width * self.pos_x,
                                               self.tile_height * self.pos_y)
        boltAnim = []
        for anim in QBlock.ANIMATION_QBLOCK:
            boltAnim.append((load_image(anim, -1), float(QBlock.ANIMATION_DELAY)))
        self.boltAnimQ = pyganim.PygAnimation(boltAnim)
        self.boltAnimQ.play()

    def update(self):
        self.image.fill(sky_color)
        self.boltAnimQ.blit(self.image, (0, 0))


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 8 * WIDTH // 27)


# --------------------------SOUNDS-------------------------------------
pygame.mixer.music.load('../sounds/main_theme.mp3')
pygame.mixer.music.play()
sound_jump = pygame.mixer.Sound('../sounds/Jump.wav')

tube_count = 0

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'g':
                AllBlocks('ground.png', x, y)
            elif level[y][x] == 'b':
                AllBlocks('block.png', x, y)
            elif level[y][x] == 'q':
                QBlock(x, y)
            elif level[y][x] == 's':
                AllBlocks('stair_block.png', x, y)
            elif level[y][x] == '!':
                if level[y + 1][x] == '!' and level[y - 1][x] != '!' and level[y + 2][x] != '!':
                    AllBlocks('middle_tube.png', x, y - 1, 32, 48)
                elif level[y + 1][x] != '!' and level[y - 1][x] != '!' and level[y - 2][x] != '!':
                    AllBlocks('small_tube.png', x, y - 1, 32, 32)
                elif level[y + 1][x] == '!' and level[y + 2][x] == '!':
                    AllBlocks('big_tube.png', x, y - 1, 32, 64)

            elif level[y][x] == 'c':
                DecorSprites(0, x, y)
            elif level[y][x] == 'r':
                DecorSprites(2, x, y)
            elif level[y][x] == 'p':
                DecorSprites(3, x, y)
            elif level[y][x] == 'a':
                DecorSprites(1, x, y)
            elif level[y][x] == 'w':
                DecorSprites(4, x, y)
            elif level[y][x] == '@':
                new_player = Mario(x, y, "Mario")
    return new_player, x, y


clock = pygame.time.Clock()
FPS = 60
SCALE_D = 2.5

BLOCK_SIZE = 16 * SCALE_D

surfaces2 = pygame.sprite.Group()
heroes = pygame.sprite.Group()
decoration = pygame.sprite.Group()

mario, level_x, level_y = generate_level(load_level('map1.txt'))
camera = Camera()
camera.update(mario)


BASEMARIOSPEED = 110 * SCALE_D
MARIOJUMPSPEED = 410 * SCALE_D

sky_color = (147, 147, 254)
count = 0

running = True
while running:
    mario.accelerate()
    mario.move()
    count += 1

    camera.update(mario)
    for group in [decoration, surfaces2, heroes]:
        for sprite in group:
            camera.apply(sprite)

    screen.fill(sky_color)
    decoration.draw(screen)
    surfaces2.draw(screen)
    heroes.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 276:
                mario.speed_x = - BASEMARIOSPEED / FPS
            elif event.key == 275:
                mario.speed_x = BASEMARIOSPEED / FPS
            elif event.key == 273 and mario.speed_y == 1:
                mario.speed_y = - MARIOJUMPSPEED / FPS
                sound_jump.play()

        elif event.type == pygame.KEYUP:
            if event.key == 276 and mario.speed_x < 0:
                mario.speed_x = 0
            elif event.key == 275 and mario.speed_x > 0:
                mario.speed_x = 0

    decoration.update()
    if count % 10 == 0:
        surfaces2.update()
    heroes.update()
    pygame.display.flip()

    clock.tick(FPS)
pygame.quit()
