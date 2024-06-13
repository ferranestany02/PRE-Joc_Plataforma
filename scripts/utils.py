import os

import pygame

BASE_IMG_PATH = 'Data/'


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
        'coin': load_images('images/coin'),
        'decor': load_images('mapa/Floor'),
        'grass': load_images('mapa/Floor'),
        'sea': load_images('mapa/Sea'),
        'large_decor': load_images('mapa/Decor'),
        'player': load_image('images/personajes/Satyr/idle/00.png'),
        'background': load_image('images/background.png'),
        'enemy/idle': Animation(load_images('images/personajes/ranger/idle'), img_dur=6),
        'enemy/attack': Animation(load_images('images/personajes/ranger/attack'), img_dur=8),
        'coin/rotate': Animation(load_images('images/coin'), img_dur=8),
        'enemy/run': Animation(load_images('images/personajes/ranger/run'), img_dur=4),
        'player/idle': Animation(load_images('images/personajes/Satyr/idle'), img_dur=6),
        'player/run': Animation(load_images('images/personajes/Satyr/run'), img_dur=4),
        'player/jump': Animation(load_images('images/personajes/Satyr/jump'), img_dur=50),
        'player/attack': Animation(load_images('images/personajes/Satyr/attack'), img_dur=50),
        'player/wall_slide': Animation(load_images('images/personajes/Satyr/wall_slide')),
        'particle/particle': Animation(load_images('images/particles/particle'), img_dur=6, loop=False),
        'arrow_1': load_image('images/arrow_1.png'),
        'arrow_2': load_image('images/arrow_2.png'),

    }


def carga_musica():
    return {
        'jump': pygame.mixer.Sound('Data/sfx/jump.wav'),
        'dash': pygame.mixer.Sound('Data/sfx/dash.wav'),
        'hit': pygame.mixer.Sound('Data/sfx/hit.wav'),
        'shoot': pygame.mixer.Sound('Data/sfx/shoot.wav'),
        'ambience': pygame.mixer.Sound('Data/sfx/ambience.wav'),
        'coin': pygame.mixer.Sound('Data/sfx/coin.flac'),
        'music': pygame.mixer.Sound('Data/sfx/music.mp3'),
        'menu': pygame.mixer.Sound('Data/sfx/menu.wav')
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