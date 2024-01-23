import pygame
from resources import background_img, player_mini_img
from entities import Player
from utils import draw_text, draw_lives, new_rock, spawn_enemies, spawn_power, collision_single_with_group, rock_player_collision, player_power_collision, player_e_bullet_collision, player_scorenumber_collision, collision_between_groups, rock_bullet_collision, bullet_enemy_collision
from config import WIDTH, BLACK, GREEN, RED

class GameState:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.e_bullets = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        for i in range(8):
            new_rock(self.rocks, self.all_sprites)
        self.score = 0
        self.death_expl = None

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
        return True

    def update(self):
        self.all_sprites.update()
        spawn_power(self.powers, self.all_sprites)
        spawn_enemies(self.score, self.enemies, self.all_sprites)

        if not self.player.invulnerable:
            collision_single_with_group(self.player, self.rocks, True, rock_player_collision)
        collision_single_with_group(self.player, self.powers, True, player_power_collision)
        collision_single_with_group(self.player, GameState.score_numbers, True, player_scorenumber_collision)
        collision_single_with_group(self.player, self.e_bullets, True, player_e_bullet_collision)
        collision_between_groups(self.rocks, self.bullets, True, True, rock_bullet_collision)
        collision_between_groups(self.enemies, self.bullets, False, True, bullet_enemy_collision)

    def render(self, screen):
        screen.fill(BLACK)
        screen.blit(background_img, (0, 0))
        for entity in self.all_sprites:
            screen.blit(entity.image, entity.rect)
        for entity in self.enemies:
            screen.blit(entity.image, entity.rect)
            entity.draw_health(screen, entity.health, 100, entity.rect.x, entity.rect.y - 15, 60, 10, RED)
        for bullet in self.e_bullets:
            screen.blit(bullet.image, bullet.rect)
        draw_text(screen, str(self.score), 18, WIDTH / 2, 10)
        self.player.draw_health(screen, self.player.health, 100, 5, 15, 100, 10, GREEN)
        draw_lives(screen, self.player.lives, player_mini_img, WIDTH - 100, 15)

    def check_game_over(self):
        if self.player.lives == 0 and not self.death_expl.alive():
            return True
        return False