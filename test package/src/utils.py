import pygame
import random
from resources import background_img, die_sound, expl_sounds
from entities import Rock, Power, Explosion, ScoreNumber, Enemy
from config import FPS, WIDTH, HEIGHT, WHITE
from game_state import GameState

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    GameState.all_sprites.add(r)
    GameState.rocks.add(r)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 32*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init(clock):
    GameState.screen.blit(background_img, (0,0))
    draw_text(GameState.screen, '太空生存戰!', 64, WIDTH/2, HEIGHT/4)
    draw_text(GameState.screen, '← →移動飛船 空白鍵發射子彈~', 22, WIDTH/2, HEIGHT/2)
    draw_text(GameState.screen, '按任意鍵開始遊戲!', 22, WIDTH/2, HEIGHT*3/5)
    draw_text(GameState.screen, '(注意:請使用英文輸入法以進行遊戲)', 18, WIDTH/2, HEIGHT*3/4)
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

def off_screen_kill(sprite, width, height):
    if sprite.rect.top > height or sprite.rect.bottom < 0 or sprite.rect.right < 0 or sprite.rect.left > width:
        sprite.kill()

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

def player_death():
    global death_expl, player
    if death_expl is None or not death_expl.alive():
        death_expl = Explosion(player.rect.center, 'player')
        GameState.all_sprites.add(death_expl)
    die_sound.play()
    player.lives -= 1
    player.health = 100
    player.hide()
    player.gun = 1

def collision_single_with_group(single, group, dokill, collision_handler):
    hits = pygame.sprite.spritecollide(single, group, dokill)
    for hit in hits:
        collision_handler(single, hit)

def rock_player_collision(player, rock):
    new_rock()
    player.health -= rock.radius * 2
    explosion = Explosion(rock.rect.center, 'sm')
    GameState.all_sprites.add(explosion)
    if player.health <= 0:
        player_death()

def player_power_collision(player, power):
    if power.type == 'heart':
        player.health += 20
        if player.health > 100:
            player.health = 100
    elif power.type == 'gun':
        player.upgrade_gun()
    elif power.type == 'shield':
        player.set_invulnerable()
    elif power.type == 'snowflower':
        player.hit_snowflower()

def player_e_bullet_collision(player, bullet):
    if not player.invulnerable:
        player.health -= 20
        if player.health <= 0:
            player_death()

def player_scorenumber_collision(player, score_number):
    global score
    score += score_number.value

def collision_between_groups(group1, group2, dokill1, dokill2, collision_handler):
    hits = pygame.sprite.groupcollide(group1, group2, dokill1, dokill2)
    for sprite1 in hits:
        for sprite2 in hits[sprite1]:
            collision_handler(sprite1, sprite2)

def bullet_enemy_collision(enemy, bullet):
    enemy.health -= 20
    if enemy.health <= 0:
        expl = Explosion(enemy.rect.center, 'lg')
        GameState.all_sprites.add(expl)
        enemy.kill()

def rock_bullet_collision(rock, bullet):
    random.choice(expl_sounds).play()
    expl = Explosion(rock.rect.center, 'lg')
    GameState.all_sprites.add(expl)
    if random.random() < 0.3:  # 30% 的概率
        value = random.choice([100, 200, 300, 400, 500])
        score_number = ScoreNumber(rock.rect.centerx, rock.rect.centery, value)
        GameState.all_sprites.add(score_number)
        GameState.score_numbers.add(score_number)
    new_rock()