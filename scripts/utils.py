import os

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))   # To delate the black part behind the image
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def carga_mapa():
    return {
        'fin': load_images('fin'),
        'coin': load_images('coin'),
        'decor': load_images('pixel_platform/Floor'),
        'grass': load_images('pixel_platform/Floor'),
        'sea': load_images('pixel_platform/Sea'),
        'large_decor': load_images('pixel_platform/Decor'),
        'stone': load_images('tiles/stone'),
        'player': load_image('entities/Satyr/idle/00.png'),
        'background': load_image('background.png'),
        'enemy/idle': Animation(load_images('entities/ranger/idle'), img_dur=6),
        'enemy/attack': Animation(load_images('entities/ranger/attack'), img_dur=8),
        'coin/rotate': Animation(load_images('coin'), img_dur=8),
        'enemy/run': Animation(load_images('entities/ranger/run'), img_dur=4),
        'player/idle': Animation(load_images('entities/Satyr/idle'), img_dur=6),
        'player/run': Animation(load_images('entities/Satyr/run'), img_dur=4),
        'player/jump': Animation(load_images('entities/Satyr/jump'), img_dur=50),
        'player/attack': Animation(load_images('entities/Satyr/attack'), img_dur=50),
        'player/wall_slide': Animation(load_images('entities/Satyr/wall_slide')),
        'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
        'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
        'arrow_1': load_image('arrow_1.png'),
        'arrow_2': load_image('arrow_2.png')


    }

def carga_musica():
    return {
        'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
        'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
        'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
        'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
        'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        'coin': pygame.mixer.Sound('data/sfx/coin.flac')
    }

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]