# Space Survival War
import pygame
import random
import os

FPS = 60 
WIDTH = 500
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 遊戲初始化 and 創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("太空生存戰")
clock = pygame.time.Clock()
score_numbers = pygame.sprite.Group()
enemies = pygame.sprite.Group()
e_bullets = pygame.sprite.Group()

# 載入圖片
def load_image(file_name):
    return pygame.image.load(os.path.join("img", file_name)).convert()

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
def load_sound(file_name):
    return pygame.mixer.Sound(os.path.join("sound", file_name))

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

font_name = os.path.join("font.ttf")
font = pygame.font.Font(font_name, 20)
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 32*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0,0))
    draw_text(screen, '太空生存戰!', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '← →移動飛船 空白鍵發射子彈~', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意鍵開始遊戲!', 22, WIDTH/2, HEIGHT*3/5)
    draw_text(screen, '(注意:請使用英文輸入法以進行遊戲)', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:
                waiting = False
                return False

def show_game_over(screen):
    screen.blit(background_img, (0, 0))
    draw_text(screen, "GAME OVER", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Press any key to restart.", 22, WIDTH / 2, HEIGHT / 2)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                waiting = False

def spawn_enemies(score, enemies, all_sprites):
    if score >= 1500 and score < 3000 and len(enemies) == 0:
        enemies.add(Enemy(80, 60, moving=False), Enemy(320, 60, moving=False))
    elif score >= 3000 and len(enemies) < 2:
        if len(enemies) == 0:
            enemies.add(Enemy(0, 60, moving=True), Enemy(WIDTH - 60, 60, moving=True))
        elif len(enemies) == 1:
            x_pos = WIDTH - 60 if enemies.sprites()[0].rect.x < WIDTH / 2 else 0
            enemies.add(Enemy(x_pos, 60, moving=True))
    for enemy in enemies:
        if enemy not in all_sprites:
            all_sprites.add(enemy)

def spawn_power(powers, all_sprites):
    if random.random() < 0.01:  # 1% 機率生成 Power
        new_power = Power((random.randint(0, WIDTH), -20))
        powers.add(new_power)
        all_sprites.add(new_power)

def handle_collision_single_with_group(single, group, dokill, collision_handler):
    hits = pygame.sprite.spritecollide(single, group, dokill)
    for hit in hits:
        collision_handler(single, hit)

def handle_rock_player_collision(player, rock):
    new_rock()
    player.health -= rock.radius * 2
    explosion = Explosion(rock.rect.center, 'sm')
    all_sprites.add(explosion)
    if player.health <= 0:
        death_expl = Explosion(player.rect.center, 'player')
        all_sprites.add(death_expl)
        die_sound.play()
        player.lives -= 1
        player.health = 100
        player.hide()
    player.gun = 1

def handle_collision_between_groups(group1, group2, dokill1, dokill2, collision_handler):
    hits = pygame.sprite.groupcollide(group1, group2, dokill1, dokill2)
    for sprite1 in hits:
        for sprite2 in hits[sprite1]:
            collision_handler(sprite1, sprite2)

def handle_bullet_enemy_collision(enemy, bullet):
    enemy.health -= 20
    if enemy.health <= 0:
        expl = Explosion(enemy.rect.center, 'lg')
        all_sprites.add(expl)
        enemy.kill()

def handle_rock_bullet_collision(rock, bullet):
    random.choice(expl_sounds).play()
    expl = Explosion(rock.rect.center, 'lg')
    all_sprites.add(expl)
    if random.random() < 0.3:  # 30% 的概率
        value = random.choice([100, 200, 300, 400, 500])
        score_number = ScoreNumber(rock.rect.centerx, rock.rect.centery, value)
        all_sprites.add(score_number)
        score_numbers.add(score_number)
    new_rock()

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

    def off_screen_kill(self):
        if self.rect.top > HEIGHT or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

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
                for rock in rocks:
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
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet3)
                    bullets.add(bullet1)
                    bullets.add(bullet3)
                self.shoot_delay_events.remove(event)  # 移除處理過的事件

    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun ==2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            elif self.gun >=3:
                # (先)發射中間的子彈
                bullet2 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
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
        for rock in rocks:
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
        self.off_screen_kill()

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
        if self.rect.top > HEIGHT:
            self.kill()

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
        if self.rect.top > HEIGHT:
            self.kill()

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
        all_sprites.add(bullet)
        e_bullets.add(bullet)

class EnemyBullet(GameObject):
    def __init__(self, x, y):
        image_path = os.path.join("img", "e_bullet.png")
        super().__init__(image_path, (x, y), image_scale=(20, 40), color_key=BLACK)
        self.rect.top = y
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        self.off_screen_kill()

pygame.mixer.music.play(-1)

# 遊戲迴圈
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0

    clock.tick(FPS)

    spawn_power(powers, all_sprites)
    spawn_enemies(score, enemies, all_sprites)
            
    # 取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 更新遊戲
    all_sprites.update()
    score_numbers.update()
    enemies.update()
    e_bullets.update()
    # 判斷石頭 v.s. 子彈的碰撞
    handle_collision_between_groups(rocks, bullets, True, True, handle_rock_bullet_collision)

    # 判斷石頭 v.s. 飛船的碰撞
    if not player.invulnerable:
        handle_collision_single_with_group(player, rocks, True, handle_rock_player_collision)

    # 判斷寶物 v.s. 飛船的碰撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'heart':
            player.health += 20
            if player.health > 100:
                player.health = 100
            shield_sound.play()
        elif hit.type == 'gun':
            player.upgrade_gun()
            gun_sound.play()
        elif hit.type == 'shield':
            player.set_invulnerable()
        elif hit.type == 'snowflower':
            player.hit_snowflower()

    # 判斷分數 v.s. 飛船的碰撞
    hits = pygame.sprite.spritecollide(player, score_numbers, True)
    for hit in hits:
        score += hit.value

    # 判斷敵人子彈 v.s. 飛船的碰撞
    hits = pygame.sprite.spritecollide(player, e_bullets, True)
    for hit in hits:
        if not player.invulnerable:
            player.health -= 20
            if player.health <= 0:
                death_expl = Explosion(player.rect.center, 'player')
                all_sprites.add(death_expl)
                die_sound.play()
                player.lives -= 1
                player.health = 100
                player.hide()
            player.gun = 1

    # 判斷子彈 v.s. 敵人的碰撞
    handle_collision_between_groups(enemies, bullets, False, True, handle_bullet_enemy_collision)

    if player.lives == 0:
        if not death_expl.alive():
            show_game_over(screen)
            show_init = True

    # 畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img, (0,0))
    for entity in all_sprites:
        entity.draw(screen) if hasattr(entity, 'draw') else screen.blit(entity.image, entity.rect)
    for entity in enemies:
        screen.blit(entity.image, entity.rect)
        entity.draw_health(screen, entity.health, 100, entity.rect.x, entity.rect.y - 15, 60, 10, RED)

    for bullet in e_bullets:
        screen.blit(bullet.image, bullet.rect)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    player.draw_health(screen, player.health, 100, 5, 15, 100, 10, GREEN)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    pygame.display.update()

pygame.quit()
