import pygame
import os
from maps.map_1 import surfaces

from pygame.examples.eventlist import main
# main()
os.chdir('../sprites')
SCALE_D = 3
SCR_X = 0
SCR_Y = 150

BLOCK_SIZE = 48

surfaces2 = pygame.sprite.Group()
heroes = pygame.sprite.Group()
decoration = pygame.sprite.Group()


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


def is_intersect(self, surface):
    left1, up1, right1, down1, left2, up2, right2, down2 = self.left, self.up, self.right, self.down, surface.left, surface.up, surface.right, surface.down
    return right1 > left2 and left1 < right2 and up1 < down2 and down1 > up2


class Mario(pygame.sprite.Sprite):
    image = load_image('small_mario_stand.png', -1)

    def __init__(self, x, y):
        super().__init__(heroes)
        self.image = pygame.transform.scale(Mario.image, (48, 48))
        self.tile_width, self.tile_height = 48, 48
        self.pos_x, self.pos_y = x, y
        self.speed_x = 0
        self.speed_y = 0
        self.rect = self.image.get_rect().move(self.tile_width * self.pos_x, self.tile_height * self.pos_y)
        self.a_y = 0

    def move(self):
        # self.check_possible_moves_x()
        # if self.speed_x < 0 and self.maygo_left or self.speed_x > 0 and self.maygo_right:
        #     self.x += self.speed_x

        if not pygame.sprite.spritecollideany(self, surfaces2):
            self.pos_x += self.speed_x
            self.pos_y += self.speed_y

    def change_speed(self):
        # self.check_possible_moves_x()
        # self.check_possible_moves_y()
        if not pygame.sprite.spritecollideany(self, surfaces2):
            self.a_y = (40 * 40 / (FPS ** 2)) * SCALE_D
            self.speed_y += self.a_y
        else:
            self.a_y = 0
            if self.speed_y > 0:
                self.speed_y = 1


class Unit:
    def __init__(self, x, y, width = 20, height=30):
        self.pos = self.x, self.y = x, y
        self.width = width
        self.height = height
        self.left = self.x
        self.right = self.x + self.width
        self.up = self.y
        self.down = self.y + self.height

        self.maygo_left = True
        self.maygo_right = True
        self.maygo_up = True
        self.maygo_down = True
        self.check_possible_moves_x()
        self.check_possible_moves_y()

        self.speed_x = 0
        self.speed_y = 0
        self.body_color = pygame.Color("red")
        self.on_ground = False
        self.a_y = 0

    def set_pos(self, x, y):
        self.pos = self.x, self.y = x, y
        self.set_borders()

    def set_borders(self):
        self.pos = self.x, self.y
        self.left = self.x
        self.right = self.x + self.width
        self.up = self.y
        self.down = self.y + self.height

    def move(self):
        # self.check_possible_moves_x()
        # if self.speed_x < 0 and self.maygo_left or self.speed_x > 0 and self.maygo_right:
        #     self.x += self.speed_x
        self.x += self.speed_x
        self.set_borders()
        self.check_possible_moves_x()

        # self.check_possible_moves_y()
        # if self.speed_y < 0 and self.maygo_up or self.speed_y > 0 and self.maygo_down:
        self.y += self.speed_y
        self.set_borders()
        self.check_possible_moves_y()

    def render(self, screen):
        global SCR_X, SCR_Y
        rect = pygame.Rect(
            int(self.x - SCR_X),
            int(self.y - SCR_Y),
            self.width,
            self.height,
        )
        pygame.draw.rect(screen, self.body_color, rect)

    def change_speed(self):
        # self.check_possible_moves_x()
        # self.check_possible_moves_y()
        if self.maygo_down:
            self.a_y = (40 * 40 / (FPS ** 2)) * SCALE_D
            self.speed_y += self.a_y
        else:
            self.a_y = 0
            if self.speed_y > 0:
                self.speed_y = 1

    def check_possible_moves_x(self):
        self.maygo_left, self.maygo_right = True, True
        for surface in surfaces:
            if is_intersect(self, surface):
                if self.speed_x > 0:
                    self.maygo_right = False
                    self.x = surface.left - self.width
                    # self.x -= self.speed_x
                elif self.speed_x < 0:
                    self.maygo_left = False
                    self.x = surface.right
                    # self.x -= self.speed_x
                self.set_borders()


    def check_possible_moves_y(self):
        self.maygo_up, self.maygo_down = True, True
        for surface in surfaces:
            if is_intersect(self, surface):
                if self.speed_y > 0:
                    self.maygo_down = False
                    self.y = surface.up - self.height
                    # self.y -= self.speed_y
                elif self.speed_y < 0:
                    self.maygo_up = False
                    self.speed_y = 1
                    self.y = surface.down
                    # self.y -= self.speed_y
                self.set_borders()


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
                                            (self.image1.get_width() * 3,
                                             self.image1.get_height() * 3))
        self.rect = self.image.get_rect().move(
            BLOCK_SIZE * self.pos_x,
            BLOCK_SIZE * self.pos_y - (self.image1.get_height() * 3 - BLOCK_SIZE))

    def update(self):
        # self.rect.x = self.pos_x - SCR_X
        # self.rect.y = self.pos_y - SCR_Y
        pass


class AllBlocks(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(surfaces2)
        self.image = pygame.transform.scale(load_image(image), (48, 48))
        self.tile_width, self.tile_height = 48, 48
        self.pos_x, self.pos_y = x, y
        self.rect = self.image.get_rect().move(self.tile_width * (self.pos_x),
                                               self.tile_height * (self.pos_y))
        # print(self.pos_x * self.tile_width, self.tile_height * (self.pos_y))

    def update(self):
        # self.rect.x = self.pos_x
        # self.rect.y = self.pos_y
        # print(self.rect.x, self.rect.y)
        pass




pygame.init()
pygame.mixer.init()

#--------------------------SOUNDS-------------------------------------
# pygame.mixer.music.load('../sounds/main_theme.mp3')
# pygame.mixer.music.play()
sound_jump = pygame.mixer.Sound('../sounds/Jump.wav')


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'g':
                AllBlocks('ground.png', x, y)
            elif level[y][x] == 'b':
                AllBlocks('block.png', x, y)
            elif level[y][x] == 'q':
                AllBlocks('q_block.png', x, y)
            elif level[y][x] == 's':
                AllBlocks('stair_block.png', x, y)
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
                new_player = Mario(x, y)
    return new_player, x, y



Mario, level_x, level_y = generate_level(load_level('map1.txt'))

size = WIDTH, HEIGHT = 800, 630
FPS = 60

BASEMARIOSPEED = 150 * SCALE_D
MARIOJUMPSPEED = 450 * SCALE_D

screen = pygame.display.set_mode(size)


clock = pygame.time.Clock()
sky_color = (147, 147, 254)

# Mario = Mario(42 * SCALE_D, 193 * SCALE_D, 10 * SCALE_D, 15 * SCALE_D)

# ground_group = pygame.sprite.Group()
# for i in range(0, int((1104 + 16) * SCALE_D), int(16 * SCALE_D)):
#     for j in range(int(208 * SCALE_D), int((239 + 16) * SCALE_D), int(16 * SCALE_D)):
#         ground_block = AllBlocks(surfaces2, load_image('ground.png'), i, j)
#         surfaces2.add(ground_block)


running = True
while running:
    # Mario.check_possible_moves_y()
    # Mario.check_possible_moves_x()
    Mario.move()
    SCR_X = (Mario.rect.x - 150)
    Mario.change_speed()

    screen.fill(sky_color)

    decoration.draw(screen)
    surfaces2.draw(screen)
    heroes.draw(screen)

    # Mario.render(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # moving left-right
        if event.type == pygame.KEYDOWN:
            if event.key == 276:
                Mario.rect.x += -BASEMARIOSPEED / FPS
                print(Mario.speed_x)
            elif event.key == 275:
                Mario.rect.x += BASEMARIOSPEED / FPS

            elif event.key == 273:
                if Mario.maygo_up and not Mario.maygo_down:
                    Mario.speed_y = -MARIOJUMPSPEED / FPS
                    sound_jump.play()

                    # Mario.maygo_down = True
        elif event.type == pygame.KEYUP:
            if event.key == 276:
                if Mario.speed_x < 0:
                    Mario.speed_x = 0
            elif event.key == 275:
                if Mario.speed_x > 0:
                    Mario.speed_x = 0

    decoration.update()
    surfaces2.update()
    heroes.update()
    pygame.display.flip()

    clock.tick(FPS)
pygame.quit()
