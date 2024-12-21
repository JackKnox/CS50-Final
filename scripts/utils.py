import pygame
import os

BASE_IMG_PATH = 'data/images/'
BASE_FNT_PATH = 'data/fonts/'

def load_image(path) -> pygame.image:
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 255, 0))
    return img

def load_images(path) -> list:
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def load_fonts() -> list:
    fonts = {}
    for font_name in sorted(os.listdir(BASE_FNT_PATH)):
        fonts[font_name.split(".")[0]] = pygame.Font(BASE_FNT_PATH + font_name)
    return fonts

def mix_colors(*colors: object) -> tuple:
    num_colors = len(colors)
    
    summed_color = [0, 0, 0]
    for color in colors:
        for i in range(3):
            summed_color[i] += color[i]
    
    return tuple(s // num_colors for s in summed_color)

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self) -> "Animation":
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self) -> None:
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self) -> pygame.image:
        return self.images[int(self.frame / self.img_duration)]