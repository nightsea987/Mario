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
    ANIMATION_SMALL_RIGHT = [load_image('small_mario_run1.png', -1),
                             load_image('small_mario_run2.png', -1),
                             load_image('small_mario_run3.png', -1)]
    ANIMATION_SMALL_LEFT = [load_image('small_mario_run1_left.png', -1),
                            load_image('small_mario_run2_left.png', -1),
                            load_image('small_mario_run3_left.png', -1)]
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

        self.running_left = False
        self.running_right = False
        self.jump = False

        self.jump_time = 0
        self.speed_x = 0
        self.speed_y = 0
        self.check_possible_moves_x()
        self.check_possible_moves_y()
        self.on_ground = False
        self.a_y = 0

        self.money = 0
        self.score = 0

    def move(self):
        self.rect.x += self.speed_x
        if self.rect.x < 0:
            self.rect.x = 0
        else:
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
                    if type(sprite) == Enemy:
                        self.hit(sprite)
                if self.speed_y < 0:
                    self.maygo_up = False
                    self.speed_y = 1
                    self.rect.y = sprite.rect.y + sprite.rect.height
                    if type(sprite) in (AllBlocks, QBlock):
                        self.hit(sprite)
        self.on_ground = not self.maygo_down

    def accelerate(self):
        if mario.running_left:
            if mario.speed_x > -MARIOSPEEDMAX:
                mario.speed_x -= BASE_ACC_X
            else:
                mario.speed_x = -MARIOSPEEDMAX
        elif mario.running_right:
            if mario.speed_x < MARIOSPEEDMAX:
                mario.speed_x += BASE_ACC_X
            else:
                mario.speed_x = MARIOSPEEDMAX
        else:
            if mario.speed_x > 0:
                mario.speed_x -= BASE_ACC_X
            if mario.speed_x < 0:
                mario.speed_x += BASE_ACC_X

        if mario.jump and ticks - self.jump_time <= 0.20 * FPS:
            mario.speed_y = - MARIOJUMPSPEED
        else:
            self.speed_y += BASE_ACC_Y_DOWN

    def hit(self, obj):
        obj.hitted(self)

    def update(self):
        pass



class Enemy(pygame.sprite.Sprite):
    ANIMATION_DELAY = 1
    ANIMATION_MUSH_RUN = [(load_image('mush1.png', -1)),
                          (load_image('mush2.png', -1))]

    score_value = 100

    def __init__(self, x, y, w=16, h=16):
        super().__init__(enemies)
        self.image = pygame.transform.scale(Enemy.ANIMATION_MUSH_RUN[0],
            (int(w * SCALE_D), int(h * SCALE_D)))

        self.tile_width, self.tile_height = TILE_WIDTH * SCALE_D, TILE_HEIGHT * SCALE_D
        self.pos_x, self.pos_y = x, y

        self.rect = self.image.get_rect().move(self.tile_width * self.pos_x, self.tile_height * self.pos_y)

        boltAnim = []
        for anim in Enemy.ANIMATION_MUSH_RUN:
            print(Enemy.ANIMATION_MUSH_RUN)
            boltAnim.append(
                (anim, float(Enemy.ANIMATION_DELAY)))
        self.boltAnimQ = pyganim.PygAnimation(boltAnim)
        self.boltAnimQ.play()

        self.is_alive = True

        self.xvel = -5

    def update(self):  # по принципу героя
        if self.is_alive:
            self.image.fill(sky_color)
            self.boltAnimQ.blit(self.image, (0, 0))


            self.rect.x += self.xvel

            self.collide()

    def collide(self):
        # for p in [surfaces2, enemies]:
        #     if sprite.collide_rect(self,
        #                            p) and self != p:
        for group in [enemies, surfaces2]:
            for sprite in group:
                if self.rect.colliderect(sprite.rect) and self != sprite:
                    # если с чем-то или кем-то столкнулись
                    self.xvel = -self.xvel  # то поворачиваем в обратную сторону


    #     self.maygo_left = True
    #     self.maygo_right = True
    #
    #     self.speed_x = 0
    #     self.check_possible_moves_x()
    #
    # def move(self):
    #     self.rect.x += self.speed_x
    #     self.check_possible_moves_x()
    #
    # def check_possible_moves_x(self):
    #     self.maygo_right, self.maygo_left = False, False
    #
    #     for sprite in surfaces2:
    #         if self.rect.colliderect(sprite.rect):
    #             if self.speed_x > 0:
    #                 self.maygo_right = False
    #                 self.rect.x = sprite.rect.x - self.rect.width
    #             elif self.speed_x < 0:
    #                 self.maygo_left = False
    #                 self.rect.x = sprite.rect.x + sprite.rect.width

    def hitted(self, mario):
        mario.score += Enemy.score_value
        sound_enemy_killed.play()




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

    def hitted(self, mario):
        sound_smallM_hit_block.play()
        print("Oh fuck.. I cant believe you done this")


class QBlock(pygame.sprite.Sprite):
    ANIMATION_DELAY = 1  # скорость смены кадров
    ANIMATION_QBLOCK = [('q_block.png'),
                        ('q_block2.png'),
                        ('q_block3.png'),
                        ('q_block2.png')]
    QBLOCK_AFTER_HIT = [('q_block_after_hit.png')]


    def __init__(self, x, y, w=16, h=16, c_of_money=1):
        super().__init__(surfaces2)
        self.w, self.h = w, h
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

        self.is_hitted = False

        self.money = c_of_money

    def hitted(self, mario):
        if self.money > 0:
            mario.money += 1
            self.money -= 1
            sound_hit_qblock.play()
            self.is_hitted = True
        else:
            sound_smallM_hit_block.play()

    def update(self):
        if self.is_hitted:
            self.image = pygame.transform.scale(
                load_image('q_block_after_hit.png'),
                (int(self.w * SCALE_D), int(self.h * SCALE_D)))
            self.boltAnimQ.blit(self.image, (0, 0))
            self.boltAnimQ.stop()
        else:
            self.image.fill(sky_color)
            self.boltAnimQ.blit(self.image, (0, 0))


class Camera:
    def __init__(self):
        self.dx = 0 * SCALE_D
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        # self.dx = 0
        # self.dy = 0

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)


# --------------------------SOUNDS-------------------------------------
# pygame.mixer.music.load('../sounds/main_theme.mp3')
# pygame.mixer.music.play()
sound_jump = pygame.mixer.Sound('../sounds/Jump.wav')
sound_smallM_hit_block = pygame.mixer.Sound('../sounds/Bump.wav')
sound_hit_qblock = pygame.mixer.Sound('../sounds/Coin.wav')
sound_enemy_killed = pygame.mixer.Sound('../sounds/Kick.wav')


this_list_is_necessary_for_camera = []
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
            elif level[y][x] == 'k':
                pass

            elif level[y][x] == 'c':
                DecorSprites(0, x, y)
            elif level[y][x] == 'r':
                this_list_is_necessary_for_camera.append(DecorSprites(2, x, y))
            elif level[y][x] == 'p':
                DecorSprites(3, x, y)
            elif level[y][x] == 'a':
                DecorSprites(1, x, y)
            elif level[y][x] == 'w':
                DecorSprites(4, x, y)
            elif level[y][x] == '@':
                new_player = Mario(x, y, "Mario")
            elif level[y][x] == 'm':
                Enemy(x, y)
    return new_player, x, y


clock = pygame.time.Clock()
FPS = 60
SCALE_D = 2.5

BLOCK_SIZE = 16 * SCALE_D

surfaces2 = pygame.sprite.Group()
heroes = pygame.sprite.Group()
decoration = pygame.sprite.Group()
enemies = pygame.sprite.Group()

mario, level_x, level_y = generate_level(load_level('map1.txt'))
camera = Camera()
# camera.update(mario)


BASEMARIOSPEED = 110 * SCALE_D / FPS
MARIOSTARTSPEED = 20 * SCALE_D / FPS
MARIOJUMPSPEED = 220 * SCALE_D / FPS
MARIOSPEEDMAX = 100 * SCALE_D / FPS
BASE_ACC_X = 5 * SCALE_D / FPS
BASE_ACC_Y_DOWN = 55 / FPS
# BASE_ACC_Y_UP =
STOP_ACC_X = 30 * SCALE_D / FPS

sky_color = (147, 147, 254)

count = 0
ticks = 0

running = True
while running:
    mario.accelerate()
    mario.move()
    count += 1

    if mario.rect.x >= WIDTH // 2 - mario.rect.w // 2:
        camera.update(mario)
    else:
        camera.dx = 0

    for group in [decoration, surfaces2, heroes, enemies]:
        for sprite in group:
            camera.apply(sprite)

    # for enemy in enemies:
    #     enemy.move()

    screen.fill(sky_color)
    decoration.draw(screen)
    surfaces2.draw(screen)
    heroes.draw(screen)
    enemies.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 276:
                # mario.speed_x = - BASEMARIOSPEED
                mario.running_left = True
            elif event.key == 275:
                # mario.speed_x = BASEMARIOSPEED
                mario.running_right = True
            elif event.key == 273 and mario.speed_y == 1:
                sound_jump.play()
                # mario.speed_y = - MARIOJUMPSPEED
                mario.jump = True
                mario.jump_time = ticks

        elif event.type == pygame.KEYUP:
            if event.key == 276 and mario.speed_x < 0:
                # mario.speed_x = 0
                mario.running_left = False
            elif event.key == 275 and mario.speed_x > 0:
                # mario.speed_x = 0
                mario.running_right = False
            elif event.key == 273:
                mario.jump = False

    decoration.update()
    if count % 10 == 0:
        surfaces2.update()
    if count % 4 == 0:
        enemies.update()
    heroes.update()
    pygame.display.flip()

    ticks += 1
    clock.tick(FPS)
pygame.quit()
