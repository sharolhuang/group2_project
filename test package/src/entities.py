import pygame
import random
import os
from utils import off_screen_kill
from config import FPS, WIDTH, HEIGHT, BLACK, WHITE, YELLOW
from game_state import GameState
from resources import shoot_sound, expl_anim, power_imgs, font

class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, center, image_scale=None, color_key=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        if image_scale:
            self.image = pygame.transform.scale(self.image, image_scale)
        if color_key is not None:
            self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def move(self, speedx, speedy):
        self.rect.x += speedx
        self.rect.y += speedy

    def draw_health(self, surf, hp, max_hp, x, y, bar_length, bar_height, bar_color):
        fill = (hp / max_hp) * bar_length
        outline_rect = pygame.Rect(x, y, bar_length, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(surf, bar_color, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Player(GameObject):
    def __init__(self):
        image_path = os.path.join("img", "player.png")
        center = (WIDTH / 2, HEIGHT - 25)
        super().__init__(image_path, center, image_scale=(50, 38), color_key=BLACK)
        self.radius = 20
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
        self.invulnerable = False
        self.invulnerable_time = 0
        self.invulnerable_duration = 5000
        self.snowflower_effect_time = 0
        self.shoot_delay_events = []
        
    def update(self):
        now = pygame.time.get_ticks()
        if self.invulnerable and now - self.invulnerable_time > self.invulnerable_duration:
            self.invulnerable = False

        if self.gun > 1 and now - self.gun_time > 10000:
            self.gun -= 1
            self.gun_time = now

        if self.snowflower_effect_time > 0:
            if pygame.time.get_ticks() - self.snowflower_effect_time > 5000:
                self.snowflower_effect_time = 0
                for rock in GameState.rocks:
                    rock.set_speed(1)  # 恢復正常速度

        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
        current_time = pygame.time.get_ticks()
        # 檢查所有射擊延遲事件
        for event in self.shoot_delay_events[:]:
            event_time, event_type = event
            if current_time - event_time >= FPS * 0.1:  # 延遲0.1秒後
                if event_type == 'side_bullets':
                    # 發射左右兩側的子彈
                    bullet1 = Bullet(self.rect.left, self.rect.top)
                    bullet3 = Bullet(self.rect.right, self.rect.top)
                    GameState.all_sprites.add(bullet1)
                    GameState.all_sprites.add(bullet3)
                    GameState.bullets.add(bullet1)
                    GameState.bullets.add(bullet3)
                self.shoot_delay_events.remove(event)  # 移除處理過的事件

    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                GameState.all_sprites.add(bullet)
                GameState.bullets.add(bullet)
                shoot_sound.play()
            elif self.gun ==2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                GameState.all_sprites.add(bullet1)
                GameState.all_sprites.add(bullet2)
                GameState.bullets.add(bullet1)
                GameState.bullets.add(bullet2)
                shoot_sound.play()
            elif self.gun >=3:
                # (先)發射中間的子彈
                bullet2 = Bullet(self.rect.centerx, self.rect.top)
                GameState.all_sprites.add(bullet2)
                GameState.bullets.add(bullet2)
                # 添加延遲兩側子彈射擊的事件
                current_time = pygame.time.get_ticks()
                self.shoot_delay_events.append((current_time, 'side_bullets'))
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        if self.gun < 3:
            self.gun += 1
            self.gun_time = pygame.time.get_ticks()

    def upgrade_gun(self):
        if self.gun == 1:
            self.gun = 2
        elif self.gun == 2:
            self.gun = 3
        self.gun_time = pygame.time.get_ticks()

    def set_invulnerable(self):
        self.invulnerable = True
        self.invulnerable_time = pygame.time.get_ticks()
    
    def draw(self, surf):
        surf.blit(self.image, self.rect)
        if self.invulnerable:
            pygame.draw.circle(surf, WHITE, self.rect.center, self.radius + 10, 2)

    def hit_snowflower(self):
        self.snowflower_effect_time = pygame.time.get_ticks()
        for rock in GameState.rocks:
            rock.set_speed(0.1)  # 隕石降速

class Rock(GameObject):
    def __init__(self):
        image_path = random.choice([os.path.join("img", f"rock{i}.png") for i in range(7)])
        center = (random.randrange(0, WIDTH), random.randrange(-180, -100))
        super().__init__(image_path, center, color_key=BLACK)
        self.radius = int(self.rect.width * 0.85 / 2)
        self.original_speedy = random.randrange(2, 5)  # 原始速度
        self.speedy = self.original_speedy
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
        self.image_ori = self.image.copy()

    def set_speed(self, speed_factor):
        self.speedy = self.original_speedy * speed_factor

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)
    
class Bullet(GameObject):
    def __init__(self, x, y):
        image_path = os.path.join("img", "bullet.png")
        super().__init__(image_path, (x, y), color_key=BLACK)
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        off_screen_kill(self, WIDTH, HEIGHT)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['heart', 'gun', 'shield', 'snowflower'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        off_screen_kill(self, WIDTH, HEIGHT)

class ScoreNumber(pygame.sprite.Sprite):
    def __init__(self, x, y, value):
        pygame.sprite.Sprite.__init__(self)
        self.value = value
        self.image = font.render(str(value), True, YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        off_screen_kill(self, WIDTH, HEIGHT)

class Enemy(GameObject):
    def __init__(self, x, y, moving=False):
        image_path = os.path.join("img", "enemy.png")
        super().__init__(image_path, (x, y), image_scale=(60, 45), color_key=BLACK)
        self.last_shot = pygame.time.get_ticks()
        self.health = 100
        self.moving = moving
        self.speedx = 2 if moving else 0
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > 2000:
            self.shoot()
            self.last_shot = now
        
        if self.moving:
            self.rect.x += self.speedx
            if self.rect.right > WIDTH:
                self.speedx = -2
            if self.rect.left < 0:
                self.speedx = 2

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        GameState.all_sprites.add(bullet)
        GameState.e_bullets.add(bullet)

class EnemyBullet(GameObject):
    def __init__(self, x, y):
        image_path = os.path.join("img", "e_bullet.png")
        super().__init__(image_path, (x, y), image_scale=(20, 40), color_key=BLACK)
        self.rect.top = y
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        off_screen_kill(self, WIDTH, HEIGHT)