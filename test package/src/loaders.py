import pygame
import os

def load_image(file_name):
    return pygame.image.load(os.path.join("img", file_name)).convert()

def load_sound(file_name):
    return pygame.mixer.Sound(os.path.join("sound", file_name))