import pygame
from typing import Tuple, List


class Player(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        
        # Dimensões e Posição
        self.w = config.TILE_SIZE * 0.8
        self.h = config.TILE_SIZE * 0.8
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Movimento
        self.speed = config.PLAYER_SPEED
        self.direction = pygame.Vector2(0, 0)
        self.facing = pygame.Vector2(0, 1)
        self.moving = False
        self.animation_time = 0
        self.transition_cooldown = 0
        
        # Armamento e Habilidades
        self.has_weapon = False
        self.weapon: str | None = None
        self.projectiles: List[dict] = []

        # Estado de Ataque/Feitiço
        self.attacking = False
        self.attack_timer = 0
        
        # COOLDOWN DA ESPADA
        self.SWORD_COOLDOWN_DURATION = 0.5
        self.sword_cooldown_timer = 0.0

        # Sistema de vida
        self.health = 5
        self.invulnerable = False
        self.invulnerable_timer = 0.0
        self.INVULNERABLE_DURATION = 1.0  # 1 segundo de invulnerabilidade após levar dano

        # NOVO: Sistema de chaves
        self.has_warrior_key = False
        self.has_mage_key = False

    def update_attack(self, dt: float):
        if self.attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.attacking = False
        
        if self.sword_cooldown_timer > 0:
            self.sword_cooldown_timer -= dt
            if self.sword_cooldown_timer < 0:
                self.sword_cooldown_timer = 0

        # Atualiza invulnerabilidade
        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

    def get_grid_position(self) -> Tuple[int, int]:
        grid_x = int(self.rect.centerx // config.TILE_SIZE)
        grid_y = int(self.rect.centery // config.TILE_SIZE)
        return grid_x, grid_y

    def handle_input(self, dt: float):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
            self.facing = self.direction.copy()
            self.moving = True
        else:
            self.moving = False

        if keys[pygame.K_SPACE] and self.has_weapon:
            self.attack()

    def move(self, dx: float, dy: float, dt: float, map_data: List[List[int]]):
        if not self.attacking:
            move_x = dx * self.speed * dt
            move_y = dy * self.speed * dt
            
            self.rect.x += move_x
            if self.check_map_collision(map_data):
                self.rect.x -= move_x
                
            self.rect.y += move_y
            if self.check_map_collision(map_data):
                self.rect.y -= move_y

    def attack(self):
        if self.attacking:
            return
            
        if self.weapon == "sword" and self.sword_cooldown_timer > 0:
            return 
            
        if self.has_weapon:
            self.attacking = True
            self.attack_timer = 0.25
            
            if self.weapon == "sword":
                self.attack_melee()
                self.sword_cooldown_timer = self.SWORD_COOLDOWN_DURATION
                
            elif self.weapon == "staff":
                self.cast_spell()

    def attack_melee(self):
        print("Ataque de espada!")

    def cast_spell(self):
        print("Feitiço lançado!")
        spell_speed = 400
        spell = {
            "pos": pygame.Vector2(self.rect.center),
            "dir": self.facing.normalize(),
            "speed": spell_speed,
            "lifetime": 1.5,
            "damage": 1
        }
        self.projectiles.append(spell)

    def take_damage(self):
        if not self.invulnerable:
            self.health -= 1
            self.invulnerable = True
            self.invulnerable_timer = self.INVULNERABLE_DURATION
            print(f"Player levou dano! Vida: {self.health}")
            return True
        return False

    def collect_key(self, key_type: str):
        if key_type == "warrior":
            self.has_warrior_key = True
            print("Chave do guerreiro coletada!")
        elif key_type == "mage":
            self.has_mage_key = True
            print("Chave do mago coletada!")

    def has_any_key(self):
        return self.has_warrior_key or self.has_mage_key

    def update(self, dt: float, map_data: List[List[int]]):
        self.handle_input(dt)
    
        if self.transition_cooldown > 0:
            self.transition_cooldown -= dt
        
        self.update_attack(dt)
        
        keys = pygame.key.get_pressed()
        dx = dy = 0.0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]: dy = -1.0
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy = 1.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -1.0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = 1.0

        self.move(dx, dy, dt, map_data)
        
        if self.moving:
            self.animation_time += dt
        
        # Atualiza projéteis de feitiço
        for spell in self.projectiles[:]:
            spell["pos"] += spell["dir"] * spell["speed"] * dt
            spell["lifetime"] -= dt
            
            if self.check_spell_collision(spell["pos"], map_data):
                self.projectiles.remove(spell)
                continue
            
            if spell["lifetime"] <= 0:
                self.projectiles.remove(spell)

    def check_map_collision(self, map_data):
        player_grid_x = int(self.rect.centerx // config.TILE_SIZE)
        player_grid_y = int(self.rect.centery // config.TILE_SIZE)
        
        for y in range(max(0, player_grid_y - 1), min(len(map_data), player_grid_y + 2)):
            for x in range(max(0, player_grid_x - 1), min(len(map_data[0]), player_grid_x + 2)):
                tile_type = map_data[y][x]
                if is_solid(tile_type):
                    hitbox = tile_hitbox(x, y, tile_type)
                    if hitbox.width > 0 and self.rect.colliderect(hitbox):
                        return True
        return False

    def check_spell_collision(self, spell_pos: pygame.Vector2, map_data) -> bool:
        grid_x = int(spell_pos.x // config.TILE_SIZE)
        grid_y = int(spell_pos.y // config.TILE_SIZE)
        
        for y in range(max(0, grid_y - 1), min(len(map_data), grid_y + 2)):
            for x in range(max(0, grid_x - 1), min(len(map_data[0]), grid_x + 2)):
                tile_type = map_data[y][x]
                if is_solid(tile_type):
                    hitbox = tile_hitbox(x, y, tile_type)
                    spell_rect = pygame.Rect(spell_pos.x - 4, spell_pos.y - 4, 8, 8)
                    if hitbox.width > 0 and spell_rect.colliderect(hitbox):
                        return True
        return False

    def draw(self, screen, camera):
        for spell in self.projectiles:
            pos = camera.apply_rect_center(spell["pos"])
            pygame.draw.circle(screen, (180, 90, 255), pos, 8)