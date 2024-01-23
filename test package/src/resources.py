import pygame
import os
from loaders import load_image, load_sound
from config import BLACK


def init():
    global player_img, background_img, bullet_img, e_bullet_img, player_mini_img, enemy_img, rock_imgs, expl_anim, power_imgs, shoot_sound, gun_sound, shield_sound, die_sound, expl_sounds, font

    # 載入圖片
    player_img = load_image("player.png")
    background_img = load_image("background.png")
    bullet_img = load_image("bullet.png")
    e_bullet_img = load_image("e_bullet.png")
    player_mini_img = pygame.transform.scale(player_img, (25, 19))
    player_mini_img.set_colorkey(BLACK)
    pygame.display.set_icon(player_mini_img)
    enemy_img = pygame.image.load(os.path.join("img", "enemy.png")).convert_alpha()

    rock_imgs = []
    for i in range(7):
        rock_imgs.append(load_image(f"rock{i}.png"))
    expl_anim = {}
    expl_anim['lg'] = []
    expl_anim['sm'] = []
    expl_anim['player'] = []
    for i in range(9):
        expl_img = load_image(f"expl{i}.png")
        expl_img.set_colorkey(BLACK)
        expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
        expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
        player_expl_img = load_image(f"player_expl{i}.png")
        player_expl_img.set_colorkey(BLACK)
        expl_anim['player'].append(player_expl_img)
    power_imgs = {}
    power_imgs['heart'] = load_image("heart.png")
    power_imgs['heart'] = pygame.transform.scale(power_imgs['heart'], (50, 50))
    power_imgs['gun'] = load_image("gun.png")
    power_imgs['shield'] = load_image("shield.png")
    power_imgs['snowflower'] = load_image("snowflower.png")
    power_imgs['snowflower'] = pygame.transform.scale(power_imgs['snowflower'], (50, 50))

    # 載入音樂、音效
    shoot_sound = load_sound("shoot.wav")
    gun_sound = load_sound("pow1.wav")
    shield_sound = load_sound("pow0.wav")
    die_sound = load_sound("rumble.ogg")
    expl_sounds = [
        load_sound("expl0.wav"),
        load_sound("expl1.wav")
    ]
    pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    # 載入文字
    font = pygame.font.Font(os.path.join("font.ttf"), 20)