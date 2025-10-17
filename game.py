import pygame
import sys
import os
from dataclasses import dataclass
from typing import List, Tuple, Optional
import math

# ==================== DADOS DOS MAPAS ====================

# MAPA ORIGINAL (overworld)
overworld = [
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,0,0,9,9,9,0,0,0,0,0,0,0,0,2],
    [2,0,5,5,0,0,1,1,9,9,9,1,1,0,0,5,5,0,0,2],
    [2,0,5,5,0,0,1,0,9,9,9,0,1,0,0,5,5,0,0,2],
    [2,0,0,0,0,0,1,0,9,7,9,0,1,0,0,0,0,0,0,2],
    [2,0,0,0,2,0,1,1,1,1,1,1,1,0,0,0,2,0,0,2],
    [2,0,0,0,0,0,0,0,14,1,3,14,0,0,0,0,4,0,0,2],
    [2,0,4,0,0,2,0,14,3,6,3,3,14,0,0,0,0,0,0,2],
    [5,0,0,0,0,0,14,3,3,6,3,3,3,14,0,2,0,0,0,5],
    [5,0,0,0,0,14,3,3,6,6,6,3,3,3,14,0,0,4,0,5],
    [2,0,0,4,0,0,6,6,6,8,6,6,6,6,0,0,0,0,0,2],
    [2,0,0,0,0,14,3,3,6,6,6,3,3,3,14,0,0,0,0,2],
    [2,0,0,0,0,0,14,3,3,6,3,3,3,14,4,0,0,0,0,2],
    [2,0,4,0,0,0,0,14,3,6,3,3,14,0,0,0,0,0,0,2],
    [2,0,0,0,2,0,0,0,14,6,3,14,14,0,2,0,0,4,0,2],
    [2,0,2,0,0,0,1,1,1,6,1,1,1,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,2],
    [2,0,5,5,0,0,1,0,0,0,0,0,1,0,0,5,5,0,0,2],
    [2,0,5,5,0,0,1,0,0,0,0,0,1,0,0,5,5,0,0,2],
    [2,2,2,2,2,2,2,2,5,5,5,2,2,2,2,2,2,2,2,2],
]

# Mapa interno da casa
house_interior = [
    [11, 11, 11, 11, 11, 11, 11, 11],
    [11, 10, 12, 10, 13, 10, 10, 11],
    [11, 10, 10, 10, 10, 10, 10, 11],
    [11, 10, 10, 10, 10, 10, 10, 11],
    [11, 10, 10, 10, 10, 10, 10, 11],
    [11, 11, 11, 10, 11, 11, 11, 11],
]

# NOVO MAPA: Floresta Mágica (apenas para magos)
forest_magic = [
    [17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17],
    [17,5,5,5,5,5,1,1,1,1,1,1,1,5,5,5,5,5,5,17],
    [17,5,5,5,5,5,1,5,5,5,5,5,1,5,5,5,5,5,5,17],
    [17,5,5,5,5,5,1,5,10,10,10,5,1,5,5,5,5,5,5,17],
    [17,5,5,5,5,5,1,5,10,10,10,5,1,5,5,5,5,5,5,17],
    [17,5,5,5,17,5,1,5,5,6,5,5,1,5,17,5,5,5,5,17],
    [17,5,5,5,5,5,1,1,5,6,5,1,1,5,5,5,17,5,5,17],
    [17,5,17,5,5,17,5,5,3,6,3,5,5,5,5,5,5,5,5,17],
    [5,5,5,5,5,5,5,3,3,6,3,3,5,5,5,17,5,5,5,17],
    [5,5,5,5,5,5,3,3,6,6,6,3,3,5,5,5,5,17,5,17],
    [17,1,1,1,1,5,6,6,6,17,6,6,6,5,1,1,1,1,1,17],
    [17,5,5,5,5,5,3,3,6,6,6,3,3,5,5,5,5,5,5,17],
    [17,5,5,5,5,5,5,3,3,6,3,3,5,5,17,5,5,5,5,17],
    [17,5,17,5,5,5,5,5,3,6,3,5,5,5,5,5,5,5,5,17],
    [17,5,5,5,17,5,5,5,5,6,5,5,5,5,17,5,5,17,5,17],
    [17,5,17,5,5,5,5,5,5,6,5,5,5,5,5,5,5,5,5,17],
    [17,5,5,5,5,5,1,1,1,1,1,1,1,5,5,5,5,5,5,17],
    [17,5,5,5,5,5,1,5,5,5,5,5,1,5,5,5,5,5,5,17],
    [17,5,5,5,5,5,1,5,5,5,5,5,1,5,5,5,5,5,5,17],
    [17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17],
]

warrior_arena = [
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,2],
    [2,11,14,14,14,14,14,14,14,16,14,14,14,14,14,14,14,14,11,2],
    [2,11,14,15,14,14,14,14,16,14,14,14,14,14,14,16,14,15,11,2],
    [2,11,14,14,16,14,14,14,14,14,14,14,14,14,14,14,14,14,11,2],
    [2,11,14,14,14,14,14,14,14,14,14,16,14,14,14,14,14,14,11,2],
    [2,11,14,14,14,16,14,14,14,14,14,14,14,14,16,14,14,14,11,2],
    [2,11,14,14,14,14,14,14,14,14,16,14,14,14,14,14,14,14,11,2],
    [2,11,16,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,5,5],
    [2,11,14,14,14,14,14,14,14,14,14,14,14,16,14,14,14,14,5,5],
    [2,11,14,14,16,14,14,14,14,14,14,14,14,14,14,14,14,14,11,2],
    [2,11,15,14,14,14,14,14,16,14,14,14,14,14,14,14,14,15,11,2],
    [2,11,14,14,14,14,14,14,14,14,16,14,14,14,14,14,14,14,11,2],
    [2,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
]

# NOVO MAPA: Arena do Boss
boss_arena = [
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,20,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
]

# ==================== CONFIGURAÇÕES ====================
@dataclass
class Config:
    SCREEN_WIDTH: int = 900
    SCREEN_HEIGHT: int = 800
    TILE_SIZE: int = 48
    FPS: int = 60
    PLAYER_SPEED: int = 180
    CAMERA_SMOOTHING: float = 0.15
    DEBUG_HITBOXES: bool = False

config = Config()

# ==================== CORES ====================
class Colors:
    GRASS = (120, 180, 100)
    GRASS_DARK = (100, 160, 80)
    PATH = (180, 130, 80)
    PATH_DARK = (160, 110, 60)
    WATER = (60, 110, 180)
    PLAYER = (220, 60, 80)
    SHADOW = (20, 20, 20, 100)
    TREE = (120, 180, 100)
    ROCK = (120, 180, 100)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    WOOD_FLOOR = (150, 95, 45)
    WALL_GREY = (180, 180, 180)
    MAGIC_PORTAL = (160, 32, 240, 150)
    SAND = (235, 210, 140) 
    MAGIC_BARRIER = (160, 32, 240)
    ENEMY = (255, 255, 0)  # Amarelo para inimigos magos
    ENEMY_EYE = (255, 0, 0)  # Vermelho para olhos dos inimigos magos
    WARRIOR_ENEMY = (139, 69, 19)  # Marrom para inimigos guerreiros
    WARRIOR_ENEMY_EYE = (0, 0, 255)  # Azul para olhos dos inimigos guerreiros
    GAME_OVER_BG = (0, 0, 0, 180)  # Fundo semi-transparente para tela de game over
    KEY = (255, 215, 0)  # Cor dourada para a chave
    BOSS_PORTAL = (255, 0, 0, 150)  # Portal vermelho para o boss
    BOSS_WARRIOR = (70, 70, 70)  # Cinza escuro para o boss guerreiro
    BOSS_WARRIOR_SWORD = (200, 200, 200)  # Prata para a espada
    BOSS_MAGE = (75, 0, 130)  # Roxo escuro para o boss mago
    BOSS_MAGE_STAFF = (139, 0, 139)  # Magenta para o cajado
    LASER_WARNING = (255, 255, 0, 100)  # Amarelo transparente para aviso de laser
    LASER_BEAM = (255, 0, 0)  # Vermelho para o laser
    VICTORY_BG = (0, 100, 0, 180)  # Verde semi-transparente para tela de vitória

# ==================== SISTEMA DE TILES ====================
@dataclass
class TileType:
    name: str
    color: Tuple[int, int, int]
    solid: bool
    hitbox_scale: float = 1.0
    is_transition: bool = False

TILE_TYPES = {
    0: TileType('grass', Colors.GRASS, False, 0.0),
    1: TileType('path', Colors.PATH, False, 0.0),
    2: TileType('tree', Colors.TREE, True, 1.0),
    3: TileType('water', Colors.WATER, True, 0.8),
    4: TileType('rock', Colors.ROCK, True, 0.3),
    5: TileType('grass_dark', Colors.GRASS_DARK, False, 0.0),
    6: TileType('bridge', Colors.PATH_DARK, False, 0.0),
    7: TileType('house_entry', Colors.PATH, False, 0.0, is_transition=True), 
    8: TileType('placa', Colors.PATH, False, 0.0), 
    9: TileType('barreira', Colors.GRASS, True, 0.8),
    10: TileType('wood_floor', Colors.WOOD_FLOOR, False, 0.0, is_transition=True),
    11: TileType('wall', Colors.WALL_GREY, True, 1.0),
    12: TileType('Sword', Colors.WOOD_FLOOR, False, 1.0),
    13: TileType('Staff', Colors.WOOD_FLOOR, False, 1.0),
    14: TileType('sand', Colors.SAND, False, 0.0),
    15: TileType('cactus', Colors.SAND, False, 0.0, ),
    16: TileType('mato', Colors.SAND, False, 0.0, ),
    17: TileType('pinheiro', Colors.GRASS_DARK, True, 0.5, ),
    18: TileType('key', Colors.KEY, False, 0.0),  # NOVO: Tile da chave
    19: TileType('boss_portal', Colors.BOSS_PORTAL, False, 0.0, is_transition=True),  # NOVO: Portal do boss
    20: TileType('boss_warrior', Colors.BOSS_WARRIOR, True, 1.0),
    21: TileType('boss_mage', Colors.BOSS_MAGE, True, 1.0),
}

# ==================== DADOS DOS MAPAS COM TRANSITION POINTS ====================
MAPS = {
    "overworld": {
        "data": overworld,
        "transition_point": (9, 4),
        "destination_map": "house_interior",
        "spawn_on_dest": (3, 4),
    },
    "house_interior": {
        "data": house_interior,
        "transition_point": (3, 5),
        "destination_map": "overworld",
        "spawn_on_dest": (9, 5),
    },
    "forest_magic": {
        "data": forest_magic,
        "transition_point": (1, 8),
        "destination_map": "overworld",
        "spawn_on_dest": (20, 8),
    },
    "warrior_arena": {
        "data": warrior_arena,
        "transition_point": (1, 8),
        "destination_map": "overworld", 
        "spawn_on_dest": (0, 8),
    },
    # NOVOS MAPAS: Corredor e Arena do Boss
    "boss_arena": {
        "data": boss_arena,
        "transition_point": (19, 7),
        "destination_map": "overworld",
        "spawn_on_dest": (8, 19),
    }
}

# Variáveis globais para o mapa atual
MAP_WIDTH = 0
MAP_HEIGHT = 0

# ==================== UTILITÁRIOS ====================
def tile_rect(x: int, y: int) -> pygame.Rect:
    return pygame.Rect(x * config.TILE_SIZE, y * config.TILE_SIZE, 
                        config.TILE_SIZE, config.TILE_SIZE)

def tile_hitbox(x: int, y: int, tile_type: int) -> pygame.Rect:
    tile_info = TILE_TYPES[tile_type]
    if not tile_info.solid or tile_info.hitbox_scale == 0:
        return pygame.Rect(0, 0, 0, 0) 
    
    full_rect = tile_rect(x, y)
    scale = tile_info.hitbox_scale
    
    new_size = int(config.TILE_SIZE * scale)
    offset_x = (config.TILE_SIZE - new_size) // 2
    offset_y = (config.TILE_SIZE - new_size) // 2
    
    return pygame.Rect(
        full_rect.x + offset_x,
        full_rect.y + offset_y,
        new_size,
        new_size
    )

def is_solid(tile_value: int) -> bool:
    return TILE_TYPES[tile_value].solid

def is_transition_tile(tile_value: int) -> bool:
    return TILE_TYPES[tile_value].is_transition

def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))

# ==================== PLAYER ====================
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
        self.health = 3
        self.invulnerable = False
        self.invulnerable_timer = 0.0
        self.INVULNERABLE_DURATION = 2.0  # 2 segundos de invulnerabilidade após levar dano

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

##INIMIGO MAGE##
class MageEnemy(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        
        self.w = config.TILE_SIZE * 0.7
        self.h = config.TILE_SIZE * 0.7
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.health = 2  # Morre com 2 feitiços
        self.speed = 100
        
        # Lógica de Ataque
        self.attack_cooldown_timer = 5.0
        self.ATTACK_COOLDOWN_DURATION = 5.0
        
        self.projectiles: List[dict] = [] 
        self.spell_speed = 300
        self.spell_damage = 1
        
        self.facing = pygame.Vector2(0, 1)
        self.moving = False
        self.animation_time = 0

    def update(self, dt: float, player: 'Player', game_map: List[List[int]]):
        # Mira no Jogador
        player_center = pygame.Vector2(player.rect.center)
        enemy_center = pygame.Vector2(self.rect.center)
        direction_to_player = player_center - enemy_center
        
        if direction_to_player.length_squared() > 0:
             self.facing = direction_to_player.normalize()
        
        # Atualiza o Cooldown
        self.attack_cooldown_timer -= dt
        if self.attack_cooldown_timer <= 0:
            self.attack()
            self.attack_cooldown_timer = self.ATTACK_COOLDOWN_DURATION
            
        # Atualiza Projéteis
        self.update_projectiles(dt, game_map)
        
        # Animação de movimento
        if self.moving:
            self.animation_time += dt
        
    def attack(self):
        spell = {
            "pos": pygame.Vector2(self.rect.center),
            "dir": self.facing,
            "speed": self.spell_speed,
            "lifetime": 2.5,
            "damage": self.spell_damage
        }
        self.projectiles.append(spell)

    def update_projectiles(self, dt: float, map_data: List[List[int]]):
        for spell in self.projectiles[:]:
            spell["pos"] += spell["dir"] * spell["speed"] * dt
            spell["lifetime"] -= dt
            
            if self.check_spell_collision(spell["pos"], map_data) or spell["lifetime"] <= 0:
                self.projectiles.remove(spell)

    def check_spell_collision(self, pos: pygame.Vector2, map_data: List[List[int]]) -> bool:
        tile_x = int(pos.x // config.TILE_SIZE)
        tile_y = int(pos.y // config.TILE_SIZE)
        
        if tile_x < 0 or tile_y < 0 or tile_y >= len(map_data) or tile_x >= len(map_data[0]):
             return True
        
        tile_type = TILE_TYPES[map_data[tile_y][tile_x]]
        return tile_type.solid

    def take_damage(self, damage: int = 1):
        self.health -= damage
        return self.health <= 0

    def draw(self, screen: pygame.Surface, camera: 'Camera'):
        # Desenha sombra
        enemy_screen_rect = camera.apply(self.rect.copy())
        shadow_surf = pygame.Surface((int(self.w), int(self.h * 0.4)), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, Colors.SHADOW, shadow_surf.get_rect())
        shadow_pos = (enemy_screen_rect.x, enemy_screen_rect.y + int(enemy_screen_rect.h * 0.7))
        screen.blit(shadow_surf, shadow_pos)
        
        # Animação de movimento
        bob = 0
        if self.moving:
            bob = int(abs(pygame.math.Vector2(0, 1).rotate(self.animation_time * 400).y) * 3)
        enemy_rect_animated = enemy_screen_rect.copy()
        enemy_rect_animated.y -= bob
        
        # Corpo amarelo
        pygame.draw.ellipse(screen, Colors.ENEMY, enemy_rect_animated)
        
        # Olhos vermelhos
        eye_size = max(3, int(enemy_screen_rect.w * 0.15))
        eye_y = enemy_rect_animated.y + enemy_rect_animated.h // 3
        left_eye_x = enemy_rect_animated.x + enemy_rect_animated.w // 3
        pygame.draw.circle(screen, Colors.ENEMY_EYE, (left_eye_x, eye_y), eye_size)
        right_eye_x = enemy_rect_animated.x + enemy_rect_animated.w * 2 // 3
        pygame.draw.circle(screen, Colors.ENEMY_EYE, (right_eye_x, eye_y), eye_size)
        
        # Desenha projéteis
        for spell in self.projectiles:
            pos = camera.apply_point(spell["pos"])
            pygame.draw.circle(screen, Colors.ENEMY_EYE, pos, int(config.TILE_SIZE * 0.15))

## INIMIGO GUERREIRO ##
class WarriorEnemy(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        
        self.w = config.TILE_SIZE * 0.8
        self.h = config.TILE_SIZE * 0.8
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.health = 3  # Morre com 3 golpes de espada
        self.speed = 120  # Mais rápido que os magos
        self.attack_damage = 1
        self.attack_cooldown = 0.0
        self.ATTACK_COOLDOWN = 1.0  # 1 segundo entre ataques
        
        self.facing = pygame.Vector2(0, 1)
        self.moving = True  # Sempre se movendo
        self.animation_time = 0

    def update(self, dt: float, player: 'Player', game_map: List[List[int]]):
        # Persegue o jogador
        player_center = pygame.Vector2(player.rect.center)
        enemy_center = pygame.Vector2(self.rect.center)
        direction_to_player = player_center - enemy_center
        
        if direction_to_player.length_squared() > 0:
            self.facing = direction_to_player.normalize()
            
            # Move na direção do jogador
            move_x = self.facing.x * self.speed * dt
            move_y = self.facing.y * self.speed * dt
            
            # Salva posição original
            original_x = self.rect.x
            original_y = self.rect.y
            
            # Tenta mover em X
            self.rect.x += move_x
            if self.check_map_collision(game_map):
                self.rect.x = original_x
                
            # Tenta mover em Y
            self.rect.y += move_y
            if self.check_map_collision(game_map):
                self.rect.y = original_y
        
        # Atualiza cooldown do ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        
        # Animação de movimento
        if self.moving:
            self.animation_time += dt

    def check_map_collision(self, map_data):
        enemy_grid_x = int(self.rect.centerx // config.TILE_SIZE)
        enemy_grid_y = int(self.rect.centery // config.TILE_SIZE)
        
        for y in range(max(0, enemy_grid_y - 1), min(len(map_data), enemy_grid_y + 2)):
            for x in range(max(0, enemy_grid_x - 1), min(len(map_data[0]), enemy_grid_x + 2)):
                tile_type = map_data[y][x]
                if is_solid(tile_type):
                    hitbox = tile_hitbox(x, y, tile_type)
                    if hitbox.width > 0 and self.rect.colliderect(hitbox):
                        return True
        return False

    def take_damage(self, damage: int = 1):
        self.health -= damage
        return self.health <= 0

    def attack_player(self, player: 'Player'):
        if self.attack_cooldown <= 0:
            if player.take_damage():
                self.attack_cooldown = self.ATTACK_COOLDOWN
                return True
        return False

    def draw(self, screen: pygame.Surface, camera: 'Camera'):
        # Desenha sombra
        enemy_screen_rect = camera.apply(self.rect.copy())
        shadow_surf = pygame.Surface((int(self.w), int(self.h * 0.4)), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, Colors.SHADOW, shadow_surf.get_rect())
        shadow_pos = (enemy_screen_rect.x, enemy_screen_rect.y + int(enemy_screen_rect.h * 0.7))
        screen.blit(shadow_surf, shadow_pos)
        
        # Animação de movimento
        bob = 0
        if self.moving:
            bob = int(abs(pygame.math.Vector2(0, 1).rotate(self.animation_time * 400).y) * 3)
        enemy_rect_animated = enemy_screen_rect.copy()
        enemy_rect_animated.y -= bob
        
        # Corpo marrom
        pygame.draw.ellipse(screen, Colors.WARRIOR_ENEMY, enemy_rect_animated)
        
        # Olhos azuis
        eye_size = max(3, int(enemy_screen_rect.w * 0.15))
        eye_y = enemy_rect_animated.y + enemy_rect_animated.h // 3
        left_eye_x = enemy_rect_animated.x + enemy_rect_animated.w // 3
        pygame.draw.circle(screen, Colors.WARRIOR_ENEMY_EYE, (left_eye_x, eye_y), eye_size)
        right_eye_x = enemy_rect_animated.x + enemy_rect_animated.w * 2 // 3
        pygame.draw.circle(screen, Colors.WARRIOR_ENEMY_EYE, (right_eye_x, eye_y), eye_size)

# ==================== BOSS GUERREIRO ====================
class BossWarrior(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        
        self.w = config.TILE_SIZE * 2
        self.h = config.TILE_SIZE * 2
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Sistema de vida
        self.health = 300
        self.max_health = 300
        
        # Movimento e combate
        self.speed = 80
        self.attack_damage = 2
        self.attack_range = config.TILE_SIZE * 1.5
        self.attack_cooldown = 0.0
        self.ATTACK_COOLDOWN = 1.0
        
        # Ataque à distância
        self.ranged_attack_cooldown = 0.0
        self.RANGED_ATTACK_COOLDOWN = 3.0
        self.projectiles = []
        
        self.facing = pygame.Vector2(0, 1)
        self.moving = False
        self.animation_time = 0
        self.attacking = False
        self.attack_timer = 0.0

    def update(self, dt: float, player: 'Player', game_map: List[List[int]]):
        player_center = pygame.Vector2(player.rect.center)
        boss_center = pygame.Vector2(self.rect.center)
        direction_to_player = player_center - boss_center
        distance_to_player = direction_to_player.length()
        
        if direction_to_player.length_squared() > 0:
            self.facing = direction_to_player.normalize()
        
        # Comportamento baseado na distância
        if distance_to_player > self.attack_range * 2:
            move_x = self.facing.x * self.speed * dt
            move_y = self.facing.y * self.speed * dt
            
            original_x = self.rect.x
            original_y = self.rect.y
            
            self.rect.x += move_x
            if self.check_map_collision(game_map):
                self.rect.x = original_x
                
            self.rect.y += move_y
            if self.check_map_collision(game_map):
                self.rect.y = original_y
                
            self.moving = True
        else:
            self.moving = False
            
            # Ataque corpo a corpo
            if self.attack_cooldown <= 0 and distance_to_player <= self.attack_range:
                self.attack_player(player)
                self.attack_cooldown = self.ATTACK_COOLDOWN
            
            # Ataque à distância
            if self.ranged_attack_cooldown <= 0 and distance_to_player > self.attack_range:
                self.ranged_attack()
                self.ranged_attack_cooldown = self.RANGED_ATTACK_COOLDOWN
        
        # Atualiza cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            
        if self.ranged_attack_cooldown > 0:
            self.ranged_attack_cooldown -= dt
            
        # Atualiza estado de ataque
        if self.attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.attacking = False
                
        # Atualiza projéteis
        self.update_projectiles(dt, game_map, player)
        
        # Animação
        if self.moving:
            self.animation_time += dt

    def attack_player(self, player: 'Player'):
        self.attacking = True
        self.attack_timer = 0.3
        # Verifica colisão direta com o jogador durante o ataque
        attack_range = config.TILE_SIZE * 1.5
        attack_rect = pygame.Rect(
            self.rect.centerx - attack_range // 2 + self.facing.x * attack_range * 0.3,
            self.rect.centery - attack_range // 2 + self.facing.y * attack_range * 0.3,
            attack_range,
            attack_range
        )
        
        if attack_rect.colliderect(player.rect):
            player.take_damage()
            print("Boss Guerreiro acertou o jogador!")

    def ranged_attack(self):
        # Lança um projétil de energia
        projectile = {
            "pos": pygame.Vector2(self.rect.center),
            "dir": self.facing,
            "speed": 200,
            "lifetime": 2.0,
            "damage": 1,
            "radius": int(config.TILE_SIZE * 0.2)
        }
        self.projectiles.append(projectile)

    def update_projectiles(self, dt: float, map_data: List[List[int]], player: 'Player'):
        for projectile in self.projectiles[:]:
            projectile["pos"] += projectile["dir"] * projectile["speed"] * dt
            projectile["lifetime"] -= dt
            
            # Verifica colisão com o jogador
            projectile_rect = pygame.Rect(
                projectile["pos"].x - projectile["radius"],
                projectile["pos"].y - projectile["radius"],
                projectile["radius"] * 2,
                projectile["radius"] * 2
            )
            
            if projectile_rect.colliderect(player.rect):
                player.take_damage()
                self.projectiles.remove(projectile)
                continue
            
            if self.check_projectile_collision(projectile["pos"], map_data) or projectile["lifetime"] <= 0:
                self.projectiles.remove(projectile)

    def check_projectile_collision(self, pos: pygame.Vector2, map_data: List[List[int]]) -> bool:
        tile_x = int(pos.x // config.TILE_SIZE)
        tile_y = int(pos.y // config.TILE_SIZE)
        
        if tile_x < 0 or tile_y < 0 or tile_y >= len(map_data) or tile_x >= len(map_data[0]):
            return True
        
        tile_type = TILE_TYPES[map_data[tile_y][tile_x]]
        return tile_type.solid

    def check_map_collision(self, map_data):
        boss_grid_x = int(self.rect.centerx // config.TILE_SIZE)
        boss_grid_y = int(self.rect.centery // config.TILE_SIZE)
        
        for y in range(max(0, boss_grid_y - 2), min(len(map_data), boss_grid_y + 3)):
            for x in range(max(0, boss_grid_x - 2), min(len(map_data[0]), boss_grid_x + 3)):
                tile_type = map_data[y][x]
                if is_solid(tile_type):
                    hitbox = tile_hitbox(x, y, tile_type)
                    if hitbox.width > 0 and self.rect.colliderect(hitbox):
                        return True
        return False

    def take_damage(self, damage: int):
        self.health -= damage
        return self.health <= 0

    def draw(self, screen: pygame.Surface, camera: 'Camera'):
        boss_screen_rect = camera.apply(self.rect.copy())
        
        # Sombra
        shadow_surf = pygame.Surface((int(self.w), int(self.h * 0.4)), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, Colors.SHADOW, shadow_surf.get_rect())
        shadow_pos = (boss_screen_rect.x, boss_screen_rect.y + int(boss_screen_rect.h * 0.7))
        screen.blit(shadow_surf, shadow_pos)
        
        # Corpo do boss
        body_rect = boss_screen_rect.copy()
        if self.moving:
            bob = int(abs(pygame.math.Vector2(0, 1).rotate(self.animation_time * 300).y) * 4)
            body_rect.y -= bob
            
        pygame.draw.ellipse(screen, Colors.BOSS_WARRIOR, body_rect)
        
        # Espada
        sword_length = config.TILE_SIZE * 1.5
        sword_width = config.TILE_SIZE * 0.2
        
        if self.attacking:
            sword_offset = self.facing * (config.TILE_SIZE * 1.2)
        else:
            sword_offset = self.facing * (config.TILE_SIZE * 0.5)
            
        sword_start = body_rect.center
        sword_end = (body_rect.centerx + sword_offset.x, body_rect.centery + sword_offset.y)
        
        pygame.draw.line(screen, Colors.BOSS_WARRIOR_SWORD, sword_start, sword_end, int(sword_width))
        
        # Olhos
        eye_size = max(5, int(body_rect.w * 0.1))
        eye_y = body_rect.y + body_rect.h // 3
        left_eye_x = body_rect.x + body_rect.w // 3
        right_eye_x = body_rect.x + body_rect.w * 2 // 3
        
        pygame.draw.circle(screen, Colors.WARRIOR_ENEMY_EYE, (left_eye_x, eye_y), eye_size)
        pygame.draw.circle(screen, Colors.WARRIOR_ENEMY_EYE, (right_eye_x, eye_y), eye_size)
        
        # Barra de vida
        health_width = body_rect.width
        health_height = 8
        health_rect = pygame.Rect(
            body_rect.x,
            body_rect.y - 15,
            health_width,
            health_height
        )
        background_rect = health_rect.copy()
        pygame.draw.rect(screen, (255, 0, 0), background_rect)
        
        health_percentage = self.health / self.max_health
        current_health_width = int(health_width * health_percentage)
        current_health_rect = pygame.Rect(
            health_rect.x,
            health_rect.y,
            current_health_width,
            health_rect.height
        )
        pygame.draw.rect(screen, (0, 255, 0), current_health_rect)
        pygame.draw.rect(screen, (255, 255, 255), health_rect, 2)
        
        # Projéteis
        for projectile in self.projectiles:
            pos = camera.apply_point(projectile["pos"])
            pygame.draw.circle(screen, Colors.BOSS_WARRIOR_SWORD, pos, projectile["radius"])

# ==================== BOSS MAGO ====================
class BossMage(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        
        self.w = config.TILE_SIZE * 2
        self.h = config.TILE_SIZE * 2
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Sistema de vida
        self.health = 50
        self.max_health = 50
        
        # Movimento e combate
        self.speed = 60
        self.attack_damage = 1
        self.attack_cooldown = 0.0
        self.ATTACK_COOLDOWN = 2.0
        
        # Ataque laser
        self.laser_cooldown = 0.0
        self.LASER_COOLDOWN = 8.0  # Aumentado para 8 segundos
        self.laser_warning_timer = 0.0
        self.laser_active = False
        self.laser_duration = 3.0  # Laser ativo por 3 segundos
        self.laser_timer = 0.0
        self.laser_angle = 0.0
        self.laser_rotation_speed = 90.0  # Graus por segundo
        self.laser_length = config.TILE_SIZE * 15
        
        # Ataques normais
        self.projectiles = []
        self.multi_attack_cooldown = 0.0
        self.MULTI_ATTACK_COOLDOWN = 3.0
        
        self.facing = pygame.Vector2(0, 1)
        self.moving = False
        self.animation_time = 0

    def update(self, dt: float, player: 'Player', game_map: List[List[int]]):
        player_center = pygame.Vector2(player.rect.center)
        boss_center = pygame.Vector2(self.rect.center)
        direction_to_player = player_center - boss_center
        
        if direction_to_player.length_squared() > 0:
            self.facing = direction_to_player.normalize()
        
        # Movimento evasivo
        distance_to_player = direction_to_player.length()
        if distance_to_player < config.TILE_SIZE * 3:
            move_away = -self.facing * self.speed * dt
            original_x = self.rect.x
            original_y = self.rect.y
            
            self.rect.x += move_away.x
            if self.check_map_collision(game_map):
                self.rect.x = original_x
                
            self.rect.y += move_away.y
            if self.check_map_collision(game_map):
                self.rect.y = original_y
                
            self.moving = True
        else:
            self.moving = False
        
        # Ataque normal
        if self.attack_cooldown <= 0:
            self.normal_attack()
            self.attack_cooldown = self.ATTACK_COOLDOWN
            
        # Ataque múltiplo
        if self.multi_attack_cooldown <= 0:
            self.multi_attack()
            self.multi_attack_cooldown = self.MULTI_ATTACK_COOLDOWN
            
        # Ataque laser
        if self.laser_cooldown <= 0 and not self.laser_active and self.laser_warning_timer <= 0:
            self.start_laser_attack()
            
        # Atualiza laser
        if self.laser_warning_timer > 0:
            self.laser_warning_timer -= dt
            if self.laser_warning_timer <= 0:
                self.activate_laser()
                
        if self.laser_active:
            self.update_laser(dt, player)
        
        # Atualiza cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            
        if self.multi_attack_cooldown > 0:
            self.multi_attack_cooldown -= dt
            
        if self.laser_cooldown > 0:
            self.laser_cooldown -= dt
            
        # Atualiza projéteis
        self.update_projectiles(dt, game_map, player)
        
        # Animação
        if self.moving:
            self.animation_time += dt

    def normal_attack(self):
        projectile = {
            "pos": pygame.Vector2(self.rect.center),
            "dir": self.facing,
            "speed": 180,
            "lifetime": 3.0,
            "damage": 1,
            "radius": int(config.TILE_SIZE * 0.2)
        }
        self.projectiles.append(projectile)

    def multi_attack(self):
        directions = [
            pygame.Vector2(1, 0),
            pygame.Vector2(0, 1),
            pygame.Vector2(-1, 0),
            pygame.Vector2(0, -1),
            pygame.Vector2(0.7, 0.7),
            pygame.Vector2(-0.7, 0.7),
            pygame.Vector2(0.7, -0.7),
            pygame.Vector2(-0.7, -0.7)
        ]
        
        for direction in directions:
            projectile = {
                "pos": pygame.Vector2(self.rect.center),
                "dir": direction.normalize(),
                "speed": 150,
                "lifetime": 2.5,
                "damage": 1,
                "radius": int(config.TILE_SIZE * 0.15)
            }
            self.projectiles.append(projectile)

    def start_laser_attack(self):
        self.laser_angle = 0.0
        self.laser_warning_timer = 2.0  # 2 segundos de aviso
        self.laser_active = False

    def activate_laser(self):
        self.laser_active = True
        self.laser_timer = self.laser_duration

    def update_laser(self, dt: float, player: 'Player'):
        # Rotaciona o laser
        self.laser_angle += self.laser_rotation_speed * dt
        
        # Atualiza timer do laser
        self.laser_timer -= dt
        if self.laser_timer <= 0:
            self.laser_active = False
            self.laser_cooldown = self.LASER_COOLDOWN
            return
        
        # Calcula direção do laser baseado no ângulo
        laser_dir = pygame.Vector2(1, 0).rotate(self.laser_angle)
        laser_start = pygame.Vector2(self.rect.center)
        laser_end = laser_start + laser_dir * self.laser_length
        
        # Verifica colisão com o jogador
        laser_vector = laser_end - laser_start
        laser_length = laser_vector.length()
        laser_vector_normalized = laser_vector.normalize()
        
        # Cria uma hitbox fina ao longo do laser para detecção de colisão
        laser_rect_width = config.TILE_SIZE * 0.3
        player_center = pygame.Vector2(player.rect.center)
        
        # Calcula a distância do ponto mais próximo no laser ao jogador
        t = max(0, min(laser_length, (player_center - laser_start).dot(laser_vector_normalized)))
        closest_point = laser_start + laser_vector_normalized * t
        distance_to_laser = (player_center - closest_point).length()
        
        # Se o jogador está perto o suficiente do laser, leva dano
        if distance_to_laser < (player.rect.width / 2 + laser_rect_width / 2):
            if player.take_damage():
                print("Jogador atingido pelo laser!")

    def update_projectiles(self, dt: float, map_data: List[List[int]], player: 'Player'):
        for projectile in self.projectiles[:]:
            projectile["pos"] += projectile["dir"] * projectile["speed"] * dt
            projectile["lifetime"] -= dt
            
            # Verifica colisão com o jogador
            projectile_rect = pygame.Rect(
                projectile["pos"].x - projectile["radius"],
                projectile["pos"].y - projectile["radius"],
                projectile["radius"] * 2,
                projectile["radius"] * 2
            )
            
            if projectile_rect.colliderect(player.rect):
                player.take_damage()
                self.projectiles.remove(projectile)
                continue
            
            if self.check_projectile_collision(projectile["pos"], map_data) or projectile["lifetime"] <= 0:
                self.projectiles.remove(projectile)

    def check_projectile_collision(self, pos: pygame.Vector2, map_data: List[List[int]]) -> bool:
        tile_x = int(pos.x // config.TILE_SIZE)
        tile_y = int(pos.y // config.TILE_SIZE)
        
        if tile_x < 0 or tile_y < 0 or tile_y >= len(map_data) or tile_x >= len(map_data[0]):
            return True
        
        tile_type = TILE_TYPES[map_data[tile_y][tile_x]]
        return tile_type.solid

    def check_map_collision(self, map_data):
        boss_grid_x = int(self.rect.centerx // config.TILE_SIZE)
        boss_grid_y = int(self.rect.centery // config.TILE_SIZE)
        
        for y in range(max(0, boss_grid_y - 2), min(len(map_data), boss_grid_y + 3)):
            for x in range(max(0, boss_grid_x - 2), min(len(map_data[0]), boss_grid_x + 3)):
                tile_type = map_data[y][x]
                if is_solid(tile_type):
                    hitbox = tile_hitbox(x, y, tile_type)
                    if hitbox.width > 0 and self.rect.colliderect(hitbox):
                        return True
        return False

    def take_damage(self, damage: int):
        self.health -= damage
        return self.health <= 0

    def draw(self, screen: pygame.Surface, camera: 'Camera'):
        boss_screen_rect = camera.apply(self.rect.copy())
        
        # Sombra
        shadow_surf = pygame.Surface((int(self.w), int(self.h * 0.4)), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, Colors.SHADOW, shadow_surf.get_rect())
        shadow_pos = (boss_screen_rect.x, boss_screen_rect.y + int(boss_screen_rect.h * 0.7))
        screen.blit(shadow_surf, shadow_pos)
        
        # Corpo do boss
        body_rect = boss_screen_rect.copy()
        if self.moving:
            bob = int(abs(pygame.math.Vector2(0, 1).rotate(self.animation_time * 300).y) * 4)
            body_rect.y -= bob
            
        pygame.draw.ellipse(screen, Colors.BOSS_MAGE, body_rect)
        
        # Cajado
        staff_length = config.TILE_SIZE * 1.8
        staff_width = config.TILE_SIZE * 0.15
        
        staff_start = body_rect.center
        staff_end = (body_rect.centerx + self.facing.x * staff_length * 0.7, 
                    body_rect.centery + self.facing.y * staff_length * 0.7)
        
        pygame.draw.line(screen, Colors.BOSS_MAGE_STAFF, staff_start, staff_end, int(staff_width))
        
        # Cristal no topo do cajado
        crystal_size = config.TILE_SIZE * 0.3
        crystal_rect = pygame.Rect(
            staff_end[0] - crystal_size // 2,
            staff_end[1] - crystal_size // 2,
            crystal_size,
            crystal_size
        )
        pygame.draw.ellipse(screen, (255, 255, 255), crystal_rect)
        
        # Olhos
        eye_size = max(5, int(body_rect.w * 0.1))
        eye_y = body_rect.y + body_rect.h // 3
        left_eye_x = body_rect.x + body_rect.w // 3
        right_eye_x = body_rect.x + body_rect.w * 2 // 3
        
        pygame.draw.circle(screen, Colors.ENEMY_EYE, (left_eye_x, eye_y), eye_size)
        pygame.draw.circle(screen, Colors.ENEMY_EYE, (right_eye_x, eye_y), eye_size)
        
        # Barra de vida
        health_width = body_rect.width
        health_height = 8
        health_rect = pygame.Rect(
            body_rect.x,
            body_rect.y - 15,
            health_width,
            health_height
        )
        background_rect = health_rect.copy()
        pygame.draw.rect(screen, (255, 0, 0), background_rect)
        
        health_percentage = self.health / self.max_health
        current_health_width = int(health_width * health_percentage)
        current_health_rect = pygame.Rect(
            health_rect.x,
            health_rect.y,
            current_health_width,
            health_rect.height
        )
        pygame.draw.rect(screen, (0, 255, 0), current_health_rect)
        pygame.draw.rect(screen, (255, 255, 255), health_rect, 2)
        
        # Aviso de laser
        if self.laser_warning_timer > 0:
            laser_start = camera.apply_point(pygame.Vector2(self.rect.center))
            laser_dir = pygame.Vector2(1, 0).rotate(self.laser_angle)
            laser_end = camera.apply_point(pygame.Vector2(self.rect.center) + laser_dir * self.laser_length)
            
            # Laser de aviso piscante
            if int(pygame.time.get_ticks() / 200) % 2 == 0:
                pygame.draw.line(screen, Colors.LASER_WARNING, laser_start, laser_end, 10)
            
            warning_text = pygame.font.SysFont('Arial', 24).render("LASER INCOMING!", True, (255, 255, 0))
            screen.blit(warning_text, (config.SCREEN_WIDTH // 2 - warning_text.get_width() // 2, 100))
        
        # Laser ativo
        if self.laser_active:
            laser_start = camera.apply_point(pygame.Vector2(self.rect.center))
            laser_dir = pygame.Vector2(1, 0).rotate(self.laser_angle)
            laser_end = camera.apply_point(pygame.Vector2(self.rect.center) + laser_dir * self.laser_length)
            pygame.draw.line(screen, Colors.LASER_BEAM, laser_start, laser_end, 15)
        
        # Projéteis
        for projectile in self.projectiles:
            pos = camera.apply_point(projectile["pos"])
            pygame.draw.circle(screen, (180, 90, 255), pos, projectile["radius"])

# ==================== CAMERA ====================
class Camera:
    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.x = 0.0
        self.y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0

    def update(self, target_rect: pygame.Rect):
        global MAP_WIDTH, MAP_HEIGHT
        
        map_pixel_width = MAP_WIDTH * config.TILE_SIZE
        map_pixel_height = MAP_HEIGHT * config.TILE_SIZE
        
        if map_pixel_width < config.SCREEN_WIDTH or map_pixel_height < config.SCREEN_HEIGHT:
            self.target_x = (config.SCREEN_WIDTH - map_pixel_width) // 2
            self.target_y = (config.SCREEN_HEIGHT - map_pixel_height) // 2
            self.target_x = -self.target_x
            self.target_y = -self.target_y
        else:
            self.target_x = target_rect.centerx - config.SCREEN_WIDTH // 2
            self.target_y = target_rect.centery - config.SCREEN_HEIGHT // 2
            
            max_x = max(0, map_pixel_width - config.SCREEN_WIDTH)
            max_y = max(0, map_pixel_height - config.SCREEN_HEIGHT)
            
            self.target_x = clamp(self.target_x, 0, max_x)
            self.target_y = clamp(self.target_y, 0, max_y)
        
        self.x += (self.target_x - self.x) * config.CAMERA_SMOOTHING
        self.y += (self.target_y - self.y) * config.CAMERA_SMOOTHING

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        return rect.move(-int(self.x), -int(self.y))
    
    def apply_rect_center(self, pos: pygame.Vector2) -> Tuple[int, int]:
        return (int(pos.x - self.x), int(pos.y - self.y))
    
    def apply_point(self, pos: pygame.Vector2) -> Tuple[int, int]:
        return (int(pos.x - self.x), int(pos.y - self.y))

# ==================== RENDERIZADOR DE TILES ====================
class TileRenderer:
    def __init__(self):
        self.images = {}
        self.slash_image = None 
        self.load_images()  # LINHA ADICIONADA - chamar load_images no construtor
        self.water_offset = 0

    def load_images(self):
        image_paths = {
            'tree': 'arvore.png',
            'rock': 'pedra.png', 
            'house': 'Casa_Madeira.png',
            'placa': 'placa.png',
            'Sword': 'Sword.png',
            'slash': 'slash.png',
            'Staff': 'Staff.png',
            'cactus': 'cactus.png',
            'mato': 'mato.png',
            'pinheiro': 'pinheiro.png',
            'key': 'Key.png',  # NOVO: Imagem da chave
        }
        
        for key, filename in image_paths.items():
            try:
                path = os.path.join("imagens", filename)
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Arquivo não encontrado: {path}")
                
                img = pygame.image.load(path).convert_alpha()

                if key == 'house':
                    scale_factor = 1
                    w = int(img.get_width() * scale_factor)
                    h = int(img.get_height() * scale_factor)
                    img = pygame.transform.scale(img, (w, h))
                elif key == 'placa':
                    img = pygame.transform.scale(img, (int(config.TILE_SIZE * 2), int(config.TILE_SIZE * 2)))
                elif key == 'Sword':
                    sword_width = int(config.TILE_SIZE * 0.6)
                    sword_height = int(config.TILE_SIZE * 0.8)
                    img = pygame.transform.scale(img, (sword_width, sword_height))
                elif key == 'slash':
                    slash_size = int(config.TILE_SIZE * 1.5)
                    self.slash_image = pygame.transform.scale(img, (slash_size, slash_size))
                    continue
                elif key == 'key':  # NOVO: Escala para a chave
                    key_size = int(config.TILE_SIZE * 0.8)
                    img = pygame.transform.scale(img, (key_size, key_size))
                else:
                    img = pygame.transform.scale(img, (config.TILE_SIZE, config.TILE_SIZE))

                self.images[key] = img

            except (pygame.error, FileNotFoundError) as e:
                print(f"[AVISO] Erro ao carregar {filename}: {e}")
                print(f"Gerando placeholder para '{key}'...")
                placeholder = self.create_placeholder(key)
                if key == 'slash':
                    self.slash_image = placeholder
                else:
                    self.images[key] = placeholder

    def create_placeholder(self, key: str) -> pygame.Surface:
        if key == 'slash':
            surf = pygame.Surface((int(config.TILE_SIZE * 1.5), int(config.TILE_SIZE * 1.5)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 0, 0, 150), surf.get_rect().center, int(config.TILE_SIZE * 0.7))
            font = pygame.font.SysFont('Arial', 12)
            text = font.render("SLASH", True, Colors.BLACK)
            surf.blit(text, text.get_rect(center=surf.get_rect().center))
            return surf
        elif key == 'house':
            surf = pygame.Surface((config.TILE_SIZE * 2, config.TILE_SIZE * 2), pygame.SRCALPHA)
            base_rect = pygame.Rect(config.TILE_SIZE * 0.1, config.TILE_SIZE * 0.6,
                                    config.TILE_SIZE * 1.8, config.TILE_SIZE * 1.3)
            pygame.draw.rect(surf, (140, 90, 50), base_rect)
            pygame.draw.polygon(surf, (180, 70, 60),
                                [(0, config.TILE_SIZE * 0.6), 
                                 (config.TILE_SIZE, config.TILE_SIZE * 0.1), 
                                 (config.TILE_SIZE * 2, config.TILE_SIZE * 0.6)])
            pygame.draw.rect(surf, (100, 60, 40),
                             pygame.Rect(config.TILE_SIZE * 0.7, config.TILE_SIZE * 1.2,
                                         config.TILE_SIZE * 0.6, config.TILE_SIZE * 0.7))
            return surf
        elif key == 'key':  # NOVO: Placeholder para a chave
            surf = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE), pygame.SRCALPHA)
            # Desenha uma chave simples
            pygame.draw.ellipse(surf, Colors.KEY, 
                               (config.TILE_SIZE * 0.3, config.TILE_SIZE * 0.3,
                                config.TILE_SIZE * 0.4, config.TILE_SIZE * 0.4))
            pygame.draw.rect(surf, Colors.KEY, 
                           (config.TILE_SIZE * 0.4, config.TILE_SIZE * 0.5,
                            config.TILE_SIZE * 0.2, config.TILE_SIZE * 0.3))
            font = pygame.font.SysFont('Arial', 10)
            text = font.render("KEY", True, Colors.BLACK)
            surf.blit(text, text.get_rect(center=surf.get_rect().center))
            return surf
        else:
            surf = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE), pygame.SRCALPHA)
            color = Colors.TREE if key == 'tree' else Colors.ROCK
            surf.fill(color)
            pygame.draw.rect(surf, Colors.BLACK, surf.get_rect(), 2)
            font = pygame.font.SysFont('Arial', 10)
            text = font.render(key[:5].upper(), True, Colors.BLACK)
            surf.blit(text, text.get_rect(center=surf.get_rect().center))
            return surf

    def update(self, dt: float):
        self.water_offset = (self.water_offset + dt * 50) % config.TILE_SIZE

    def draw_tile(self, screen: pygame.Surface, tile_type: int, rect: pygame.Rect, draw_sword: bool = True):
        tile_info = TILE_TYPES[tile_type]
        pygame.draw.rect(screen, tile_info.color, rect)

        if tile_type == 2:
            screen.blit(self.images['tree'], rect)
        elif tile_type == 4:
            screen.blit(self.images['rock'], rect)
        elif tile_type == 8:
            placa_img = self.images['placa']
            screen.blit(placa_img, placa_img.get_rect(center=rect.center))
        elif tile_type == 10:
            pygame.draw.rect(screen, Colors.WOOD_FLOOR, rect)
            for i in range(0, config.TILE_SIZE, 12):
                pygame.draw.line(screen, (130, 80, 40),
                                 (rect.x + i, rect.y),
                                 (rect.x + i, rect.y + config.TILE_SIZE), 2)
        elif tile_type == 11:
            pygame.draw.rect(screen, Colors.WALL_GREY, rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
        elif tile_type == 12:
            pygame.draw.rect(screen, Colors.WOOD_FLOOR, rect)
            for i in range(0, config.TILE_SIZE, 12):
                pygame.draw.line(screen, (130, 80, 40),
                                 (rect.x + i, rect.y),
                                 (rect.x + i, rect.y + config.TILE_SIZE), 2)
            if draw_sword:
                sword_img = self.images.get('Sword')
                if sword_img:
                    screen.blit(sword_img, sword_img.get_rect(center=rect.center))
        elif tile_type == 13:
            pygame.draw.rect(screen, Colors.WOOD_FLOOR, rect)
            for i in range(0, config.TILE_SIZE, 12):
                pygame.draw.line(screen, (130, 80, 40),
                                 (rect.x + i, rect.y),
                                 (rect.x + i, rect.y + config.TILE_SIZE), 2)
            if draw_sword:
                staff_img = self.images.get('Staff')
                if staff_img:
                    screen.blit(staff_img, staff_img.get_rect(center=rect.center))
        elif tile_type == 15:
            screen.blit(self.images['cactus'], rect)
        elif tile_type == 16:
            screen.blit(self.images['mato'], rect)
        elif tile_type == 17:
            screen.blit(self.images['pinheiro'], rect)
        elif tile_type == 18:  # CHAVE - AGORA COM IMAGEM PNG
            # Fundo do tile (opcional, pode remover se quiser só a imagem)
            pygame.draw.rect(screen, Colors.WOOD_FLOOR, rect)
            
            # Desenha a imagem da chave centralizada
            key_img = self.images.get('key')
            if key_img:
                screen.blit(key_img, key_img.get_rect(center=rect.center))
            else:
                # Fallback caso a imagem não carregue
                pygame.draw.ellipse(screen, Colors.KEY, 
                                   (rect.centerx - config.TILE_SIZE//4, 
                                    rect.centery - config.TILE_SIZE//4,
                                    config.TILE_SIZE//2, 
                                    config.TILE_SIZE//2))
        elif tile_type == 19:  # Portal do boss
            # Portal vermelho pulsante
            pulse = (pygame.time.get_ticks() // 200) % 2
            portal_color = (255, 0, 0) if pulse else (200, 0, 0)
            pygame.draw.rect(screen, portal_color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)

# ==================== GAME ====================
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Floresta Encantada - Aventura Top-Down")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        # NOVO: Sistema de música
        pygame.mixer.init()
        self.current_music = None
        self.music_volume = 0.5  # Volume entre 0.0 e 1.0
        
        self.tile_renderer = TileRenderer()
        
        self.current_map_name = "overworld"
        self.current_map_data = MAPS[self.current_map_name]["data"]
        
        self.sword_collected = False
        self.staff_collected = False

        self.player = Player(0, 0)
        self.camera = Camera(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

        # INICIALIZAÇÃO CORRETA DOS INIMIGOS - DEVE VIR ANTES DE change_map
        self.mage_enemies = pygame.sprite.Group()
        self.warrior_enemies = pygame.sprite.Group()
        
        self.change_map("overworld", (9, 14))

        self.font_small = pygame.font.SysFont('Arial', 18)
        self.font_large = pygame.font.SysFont('Arial', 32, bold=True)
        self.font_xlarge = pygame.font.SysFont('Arial', 48, bold=True)
        self.ui_surface = pygame.Surface((config.SCREEN_WIDTH, 60), pygame.SRCALPHA)
        
        # Variáveis para mensagens
        self.show_portal_message = False
        self.portal_message_timer = 0.0
        self.show_forest_welcome = False
        self.forest_welcome_timer = 0.0
        self.show_warrior_welcome = False
        self.warrior_welcome_timer = 0.0
        self.show_warrior_message = False
        self.warrior_message_timer = 0.0
        self.show_boss_message = False
        self.boss_message_timer = 0.0

        # NOVO: Estado das chaves no mapa
        self.warrior_key_spawned = False
        self.mage_key_spawned = False

        self.boss = None
        self.victory = False
        self.victory_timer = 0.0

    def load_music(self, map_name: str):
        """Carrega e toca a música apropriada para cada mapa"""
        music_map = {
            "overworld": "Musica1",
            "house_interior": "Musica1",
            "warrior_arena": "Musica2", 
            "forest_magic": "Musica2",
            "boss_arena": "Musica2"
        }
        
        target_music = music_map.get(map_name, "Musica1")
        
        # Se já está tocando a música correta, não faz nada
        if self.current_music == target_music and pygame.mixer.music.get_busy():
            return
        
        # Para a música atual
        pygame.mixer.music.stop()
        
        # Tenta carregar a nova música
        try:
            music_path = os.path.join("musicas", f"{target_music}.mp3")
            if not os.path.exists(music_path):
                # Tenta outras extensões comuns
                for ext in [".wav", ".ogg", ".mp3"]:
                    music_path = os.path.join("musicas", f"{target_music}{ext}")
                    if os.path.exists(music_path):
                        break
                else:
                    print(f"[AVISO] Música {target_music} não encontrada na pasta 'musicas'")
                    return
            
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # -1 para loop infinito
            self.current_music = target_music
            print(f"Tocando: {target_music}")
            
        except pygame.error as e:
            print(f"[ERRO] Não foi possível carregar a música {target_music}: {e}")

    def load_enemies(self):
        """Carrega inimigos baseado no mapa atual"""
        self.mage_enemies.empty()
        self.warrior_enemies.empty()
        self.boss = None  
        
        if self.current_map_name == "forest_magic":
            spawn_positions = [
                (5, 5), (15, 5), (5, 15), (15, 15),
                (10, 3), (10, 17), (3, 10), (17, 10),
                (7, 7), (13, 13)
            ]
            
            for grid_x, grid_y in spawn_positions:
                pixel_x = grid_x * config.TILE_SIZE + config.TILE_SIZE / 2
                pixel_y = grid_y * config.TILE_SIZE + config.TILE_SIZE / 2
                
                enemy = MageEnemy(pixel_x - config.TILE_SIZE * 0.7 / 2, pixel_y - config.TILE_SIZE * 0.7 / 2)
                self.mage_enemies.add(enemy)
                
        elif self.current_map_name == "warrior_arena":
            warrior_spawns = [
                (5, 5), (15, 5), (5, 12), (15, 12),
                (8, 3), (12, 3), (8, 12), (12, 12)
            ]
            
            for grid_x, grid_y in warrior_spawns:
                pixel_x = grid_x * config.TILE_SIZE + config.TILE_SIZE / 2
                pixel_y = grid_y * config.TILE_SIZE + config.TILE_SIZE / 2
                
                enemy = WarriorEnemy(pixel_x - config.TILE_SIZE * 0.8 / 2, pixel_y - config.TILE_SIZE * 0.8 / 2)
                self.warrior_enemies.add(enemy)

        elif self.current_map_name == "boss_arena":
            # CORREÇÃO: Spawn do boss sempre que entrar na arena do boss
            center_x = len(self.current_map_data[0]) // 2
            center_y = len(self.current_map_data) // 2
            
            boss_x = center_x * config.TILE_SIZE - config.TILE_SIZE
            boss_y = center_y * config.TILE_SIZE - config.TILE_SIZE
            
            print(f"Tentando spawnar boss na arena. Weapon do player: {self.player.weapon}")
            
            if self.player.weapon == "sword":
                self.boss = BossWarrior(boss_x, boss_y)
                print("Boss Guerreiro spawnado com sucesso!")
            elif self.player.weapon == "staff":
                self.boss = BossMage(boss_x, boss_y)
                print("Boss Mago spawnado com sucesso!")
            else:
                print("AVISO: Player não tem arma definida, spawnando Boss Guerreiro por padrão")
                self.boss = BossWarrior(boss_x, boss_y)

    def spawn_key(self, key_type: str):
        """Spawna uma chave no centro do mapa atual"""
        center_x = len(self.current_map_data[0]) // 2
        center_y = len(self.current_map_data) // 2
        
        if key_type == "warrior" and not self.warrior_key_spawned:
            self.current_map_data[center_y][center_x] = 18
            self.warrior_key_spawned = True
            print("Chave do guerreiro spawnada!")
        elif key_type == "mage" and not self.mage_key_spawned:
            self.current_map_data[center_y][center_x] = 18
            self.mage_key_spawned = True
            print("Chave do mago spawnada!")

    def change_map(self, map_name: str, start_pos: Tuple[int, int]):
        global MAP_WIDTH, MAP_HEIGHT

        map_info = MAPS[map_name]
        
        self.current_map_name = map_name
        self.current_map_data = map_info["data"]
        
        MAP_HEIGHT = len(map_info["data"])
        MAP_WIDTH = len(map_info["data"][0])

        start_x = start_pos[0] * config.TILE_SIZE
        start_y = start_pos[1] * config.TILE_SIZE
        self.player.rect.topleft = (start_x, start_y)
        
        self.camera.x = self.player.rect.centerx - config.SCREEN_WIDTH // 2
        self.camera.y = self.player.rect.centery - config.SCREEN_HEIGHT // 2
        self.camera.update(self.player.rect)
        
        # NOVO: Carrega a música do mapa
        self.load_music(map_name)
        
        # Mensagens de boas-vindas
        if map_name == "forest_magic":
            self.show_forest_welcome = True
            self.forest_welcome_timer = 5.0

        if map_name == "warrior_arena":
            self.show_warrior_welcome = True
            self.warrior_welcome_timer = 5.0

        # Recarrega inimigos e configurações do mapa
        self.load_enemies()

        print(f"Transição para o mapa: {map_name}. Nova posição: {start_pos}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_h:
                    config.DEBUG_HITBOXES = not config.DEBUG_HITBOXES
                    print(f"Debug Hitboxes: {'ON' if config.DEBUG_HITBOXES else 'OFF'}")
                elif event.key == pygame.K_SPACE and not self.game_over:
                    self.player.attack()
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                # NOVO: Controles de música
                elif event.key == pygame.K_m:
                    # Mute/Unmute
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                        print("Música pausada")
                    else:
                        pygame.mixer.music.unpause()
                        print("Música retomada")
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    # Aumentar volume
                    self.music_volume = min(1.0, self.music_volume + 0.1)
                    pygame.mixer.music.set_volume(self.music_volume)
                    print(f"Volume: {int(self.music_volume * 100)}%")
                elif event.key == pygame.K_MINUS:
                    # Diminuir volume
                    self.music_volume = max(0.0, self.music_volume - 0.1)
                    pygame.mixer.music.set_volume(self.music_volume)
                    print(f"Volume: {int(self.music_volume * 100)}%")

    def check_transitions_and_items(self):
        if self.game_over:
            return
            
        grid_x, grid_y = self.player.get_grid_position()
        
        if self.player.transition_cooldown > 0:
            return

        # Porta casa → interior
        if self.current_map_name == "overworld" and (grid_x, grid_y) == (9, 4):
            self.player.transition_cooldown = 0.5
            self.change_map("house_interior", (3, 4))

        # Porta interior → overworld
        elif self.current_map_name == "house_interior" and (grid_x, grid_y) == (3, 5):
            self.player.transition_cooldown = 0.5
            self.change_map("overworld", (9, 5))

        # Portal Mágico → Floresta Mágica (APENAS MAGO)
        elif (self.current_map_name == "overworld" and 
            ((grid_x, grid_y) == (20, 8) or (grid_x, grid_y) == (20, 9))):
            
            if self.player.has_weapon and self.player.weapon == "staff":
                self.player.transition_cooldown = 0.5
                self.change_map("forest_magic", (1, 8))
            else:
                self.show_portal_message = True
                self.portal_message_timer = 2.0

        # Saída da Floresta Mágica → Overworld
        elif self.current_map_name == "forest_magic" and ((grid_x, grid_y) == (1, 8) or (grid_x, grid_y) == (1, 9)):
            self.player.transition_cooldown = 0.5
            self.change_map("overworld", (20, 8))

        # Entrada Arena Guerreiro → Arena (APENAS GUERREIRO)
        elif (self.current_map_name == "overworld" and 
            ((grid_x, grid_y) == (0, 8) or (grid_x, grid_y) == (0, 9))):
            
            if self.player.has_weapon and self.player.weapon == "sword":
                self.player.transition_cooldown = 0.5
                self.change_map("warrior_arena", (19, 8))
            else:
                self.show_warrior_message = True
                self.warrior_message_timer = 2.0

        # Saída Arena Guerreiro → Overworld
        elif self.current_map_name == "warrior_arena" and ((grid_x, grid_y) == (19, 8) or (grid_x, grid_y) == (19, 9)):
            self.player.transition_cooldown = 0.5
            self.change_map("overworld", (0, 8))

        # NOVO: Entrada para o Corredor do Boss
        elif (self.current_map_name == "overworld" and 
            ((grid_x, grid_y) == (8, 19) or (grid_x, grid_y) == (9, 19) or (grid_x, grid_y) == (10, 19))):
            
            if self.player.has_any_key():
                self.player.transition_cooldown = 0.5
                self.change_map("boss_arena", (10, 1))
            else:
                self.show_boss_message = True
                self.boss_message_timer = 2.0

        # NOVO: Entrada da Arena do Boss
        elif self.current_map_name == "overworld" and ((grid_x, grid_y) == (10, 13) or (grid_x, grid_y) == (10, 14)):
            self.player.transition_cooldown = 0.5
            self.change_map("boss_arena", (10, 1))

        # ITENS
        if self.current_map_name == "house_interior":
            if 0 <= grid_y < len(self.current_map_data) and 0 <= grid_x < len(self.current_map_data[0]):
                tile = self.current_map_data[grid_y][grid_x]

                if tile == 12 and not self.player.has_weapon:
                    self.player.has_weapon = True
                    self.player.weapon = "sword"
                    self.sword_collected = True
                    self.current_map_data[grid_y][grid_x] = 10
                    print("ESPADA COLETADA! Escolha permanente feita.")

                elif tile == 13 and not self.player.has_weapon:
                    self.player.has_weapon = True
                    self.player.weapon = "staff"
                    self.staff_collected = True
                    self.current_map_data[grid_y][grid_x] = 10
                    print("CAJADO COLETADO! Escolha permanente feita.")

        # NOVO: Coleta de chaves
        if 0 <= grid_y < len(self.current_map_data) and 0 <= grid_x < len(self.current_map_data[0]):
            tile = self.current_map_data[grid_y][grid_x]
            
            if tile == 18:  # Tile da chave
                if self.current_map_name == "warrior_arena":
                    self.player.collect_key("warrior")
                elif self.current_map_name == "forest_magic":
                    self.player.collect_key("mage")
                self.current_map_data[grid_y][grid_x] = 0  # Remove a chave

    def check_collisions(self):
        """Verifica colisões entre projéteis do player e inimigos, e entre projéteis inimigos e player"""
        if self.game_over or self.victory:
            return
            
        # Projéteis do player contra inimigos magos
        for spell in self.player.projectiles[:]:
            spell_rect = pygame.Rect(spell["pos"].x - 4, spell["pos"].y - 4, 8, 8)
            
            for enemy in self.mage_enemies.sprites():
                if spell_rect.colliderect(enemy.rect):
                    if enemy.take_damage(spell["damage"]):
                        self.mage_enemies.remove(enemy)
                        print("Inimigo mago derrotado!")
                    self.player.projectiles.remove(spell)
                    break

        # Projéteis inimigos magos contra player
        for enemy in self.mage_enemies:
            for spell in enemy.projectiles[:]:
                spell_rect = pygame.Rect(spell["pos"].x - 4, spell["pos"].y - 4, 8, 8)
                
                if spell_rect.colliderect(self.player.rect):
                    if self.player.take_damage():
                        if self.player.health == 0:
                            self.game_over = True
                            print("GAME OVER!")
                    enemy.projectiles.remove(spell)

        # Colisões com inimigos guerreiros
        for enemy in self.warrior_enemies.sprites():
            # Colisão corpo a corpo com player
            if self.player.rect.colliderect(enemy.rect):
                if enemy.attack_player(self.player):
                    if self.player.health <= 0:
                        self.game_over = True
                        print("GAME OVER!")
            
            # Colisão com ataque de espada do player
        if (self.player.attacking and 
            self.player.has_weapon and 
            self.player.weapon == "sword"):
            
            # Cria hitbox do ataque de espada na direção correta
            player_center = pygame.Vector2(self.player.rect.center)
            slash_offset = self.player.facing * (config.TILE_SIZE * 0.8)
            slash_center = player_center + slash_offset
            
            # Tamanho da hitbox do ataque
            slash_size = config.TILE_SIZE * 1.2  # Um pouco menor que a animação visual
            
            # Cria retângulo de colisão baseado na direção
            if abs(self.player.facing.x) > abs(self.player.facing.y):
                # Ataque horizontal
                slash_rect = pygame.Rect(
                    slash_center.x - slash_size // 2,
                    slash_center.y - slash_size // 4,
                    slash_size,
                    slash_size // 2
                )
            else:
                # Ataque vertical
                slash_rect = pygame.Rect(
                    slash_center.x - slash_size // 4,
                    slash_center.y - slash_size // 2,
                    slash_size // 2,
                    slash_size
                )
            
            for enemy in self.warrior_enemies.sprites():
                if slash_rect.colliderect(enemy.rect):
                    if enemy.take_damage(1):
                        self.warrior_enemies.remove(enemy)
                        print("Inimigo guerreiro derrotado!")

        # Colisões com o boss
        if self.boss:
            # Projéteis do player contra o boss
            for spell in self.player.projectiles[:]:
                spell_rect = pygame.Rect(spell["pos"].x - 4, spell["pos"].y - 4, 8, 8)
                
                if spell_rect.colliderect(self.boss.rect):
                    if self.boss.take_damage(spell["damage"]):
                        self.victory = True
                        self.victory_timer = 5.0  # 5 segundos de tela de vitória
                        print("BOSS DERROTADO! VITÓRIA!")
                    self.player.projectiles.remove(spell)
                    break
            
            # Ataque de espada contra o boss
            if (self.player.attacking and 
                self.player.has_weapon and 
                self.player.weapon == "sword"):
                
                # Hitbox do ataque de espada (mesma lógica anterior)
                player_center = pygame.Vector2(self.player.rect.center)
                slash_offset = self.player.facing * (config.TILE_SIZE * 0.8)
                slash_center = player_center + slash_offset
                slash_size = config.TILE_SIZE * 1.2
                
                if abs(self.player.facing.x) > abs(self.player.facing.y):
                    slash_rect = pygame.Rect(
                        slash_center.x - slash_size // 2,
                        slash_center.y - slash_size // 4,
                        slash_size,
                        slash_size // 2
                    )
                else:
                    slash_rect = pygame.Rect(
                        slash_center.x - slash_size // 4,
                        slash_center.y - slash_size // 2,
                        slash_size // 2,
                        slash_size
                    )
                
                if slash_rect.colliderect(self.boss.rect):
                    if self.boss.take_damage(1):
                        self.victory = True
                        self.victory_timer = 5.0
                        print("BOSS DERROTADO! VITÓRIA!")

            # Projéteis do boss contra o player
            if isinstance(self.boss, BossWarrior):
                for projectile in self.boss.projectiles[:]:
                    projectile_rect = pygame.Rect(
                        projectile["pos"].x - projectile["radius"],
                        projectile["pos"].y - projectile["radius"],
                        projectile["radius"] * 2,
                        projectile["radius"] * 2
                    )
                    
                    if projectile_rect.colliderect(self.player.rect):
                        if self.player.take_damage():
                            if self.player.health <= 0:
                                self.game_over = True
                                print("GAME OVER!")
                        self.boss.projectiles.remove(projectile)
            
            elif isinstance(self.boss, BossMage):
                for projectile in self.boss.projectiles[:]:
                    projectile_rect = pygame.Rect(
                        projectile["pos"].x - projectile["radius"],
                        projectile["pos"].y - projectile["radius"],
                        projectile["radius"] * 2,
                        projectile["radius"] * 2
                    )
                    
                    if projectile_rect.colliderect(self.player.rect):
                        if self.player.take_damage():
                            if self.player.health <= 0:
                                self.game_over = True
                                print("GAME OVER!")
                        self.boss.projectiles.remove(projectile)

    def update(self, dt: float):
        if not self.game_over and not self.victory:
            self.player.update(dt, self.current_map_data)
            self.camera.update(self.player.rect)
            self.tile_renderer.update(dt)
            self.check_transitions_and_items()
            self.check_collisions()
            
            # Atualiza inimigos
            for enemy in self.mage_enemies:
                enemy.update(dt, self.player, self.current_map_data)
            
            for enemy in self.warrior_enemies:
                enemy.update(dt, self.player, self.current_map_data)
            
            # NOVO: Atualiza o boss
            if self.boss:
                self.boss.update(dt, self.player, self.current_map_data)
            
            # NOVO: Spawn de chaves quando todos os inimigos são derrotados
            if (self.current_map_name == "warrior_arena" and 
                len(self.warrior_enemies) == 0 and 
                not self.warrior_key_spawned):
                self.spawn_key("warrior")
            
            if (self.current_map_name == "forest_magic" and 
                len(self.mage_enemies) == 0 and 
                not self.mage_key_spawned):
                self.spawn_key("mage")
        
        # Atualiza timers de mensagens
        if self.show_portal_message and self.portal_message_timer > 0:
            self.portal_message_timer -= dt
            if self.portal_message_timer <= 0:
                self.show_portal_message = False
        
        if self.show_forest_welcome and self.forest_welcome_timer > 0:
            self.forest_welcome_timer -= dt
            if self.forest_welcome_timer <= 0:
                self.show_forest_welcome = False
        
        if self.show_warrior_welcome and self.warrior_welcome_timer > 0:
            self.warrior_welcome_timer -= dt
            if self.warrior_welcome_timer <= 0:
                self.show_warrior_welcome = False
        
        if self.show_warrior_message and self.warrior_message_timer > 0:
            self.warrior_message_timer -= dt
            if self.warrior_message_timer <= 0:
                self.show_warrior_message = False
        
        if self.show_boss_message and self.boss_message_timer > 0:
            self.boss_message_timer -= dt
            if self.boss_message_timer <= 0:
                self.show_boss_message = False

        if self.victory and self.victory_timer > 0:
            self.victory_timer -= dt

    def draw(self):
        self.screen.fill((30, 30, 40))

        cam_left = max(0, int(self.camera.x) // config.TILE_SIZE - 1)
        cam_right = min(MAP_WIDTH, (int(self.camera.x) + config.SCREEN_WIDTH) // config.TILE_SIZE + 2)
        cam_top = max(0, int(self.camera.y) // config.TILE_SIZE - 1)
        cam_bottom = min(MAP_HEIGHT, (int(self.camera.y) + config.SCREEN_HEIGHT) // config.TILE_SIZE + 2)

        for row in range(cam_top, cam_bottom):
            for col in range(cam_left, cam_right):
                tile_type = self.current_map_data[row][col]
                r = tile_rect(col, row)
                r_screen = self.camera.apply(r)
                
                if self.current_map_name == "house_interior":
                    if tile_type == 12:
                        self.tile_renderer.draw_tile(self.screen, tile_type, r_screen, draw_sword=(not self.sword_collected))
                    elif tile_type == 13:
                        self.tile_renderer.draw_tile(self.screen, tile_type, r_screen, draw_sword=(not self.staff_collected))
                    else:
                        self.tile_renderer.draw_tile(self.screen, tile_type, r_screen)
                elif self.current_map_name == "overworld" and tile_type == 7:
                    self.tile_renderer.draw_tile(self.screen, 1, r_screen)
                else:
                    self.tile_renderer.draw_tile(self.screen, tile_type, r_screen)

        if self.current_map_name == "overworld":
            house_img = self.tile_renderer.images.get('house')
            door_align_tile = tile_rect(9, 5) 
            door_align_screen = self.camera.apply(door_align_tile)
            if house_img:
                house_rect = house_img.get_rect(midbottom=(
                    door_align_screen.centerx, 
                    door_align_screen.centery - (config.TILE_SIZE * 0.5) 
                ))
                self.screen.blit(house_img, house_rect)
        
        self.draw_player(self.screen)
        
        # Desenha inimigos magos
        for enemy in self.mage_enemies:
            enemy.draw(self.screen, self.camera)
        
        # Desenha inimigos guerreiros
        for enemy in self.warrior_enemies:
            enemy.draw(self.screen, self.camera)
        
        if self.boss:
            self.boss.draw(self.screen, self.camera)

        if (self.player.attacking and 
            self.tile_renderer.slash_image and 
            self.player.has_weapon and 
            self.player.weapon == "sword"):
            
            slash_img = self.tile_renderer.slash_image
            player_screen_center = self.camera.apply(self.player.rect).center
            slash_offset = pygame.math.Vector2(self.player.facing) * (config.TILE_SIZE * 0.8)
            slash_center_x = player_screen_center[0] + slash_offset.x
            slash_center_y = player_screen_center[1] + slash_offset.y
            slash_rect = slash_img.get_rect(center=(int(slash_center_x), int(slash_center_y)))
            
            # CORREÇÃO: Calcular o ângulo baseado na direção do facing
            # O Vector2(0, -1) aponta para cima, então ajustamos para a direção correta
            if self.player.facing.x == 0 and self.player.facing.y == 0:
                # Se não há direção definida, usa a última direção conhecida
                angle = 0
            else:
                # Calcula o ângulo baseado no vetor de direção
                # Vector2(0, -1) é "para cima" (0 graus), então ajustamos
                base_vector = pygame.math.Vector2(0, -1)  # Para cima
                angle = base_vector.angle_to(self.player.facing)
            
            rotated_slash = pygame.transform.rotate(slash_img, angle)
            rotated_rect = rotated_slash.get_rect(center=slash_rect.center)
            self.screen.blit(rotated_slash, rotated_rect)
        
        self.player.draw(self.screen, self.camera)
        
        if config.DEBUG_HITBOXES:
            for row in range(cam_top, cam_bottom):
                for col in range(cam_left, cam_right):
                    if 0 <= row < len(self.current_map_data) and 0 <= col < len(self.current_map_data[0]):
                        tile_type = self.current_map_data[row][col]
                        if is_solid(tile_type): 
                            hitbox = tile_hitbox(col, row, tile_type)
                            if hitbox.width > 0:
                                hitbox_screen = self.camera.apply(hitbox)
                                pygame.draw.rect(self.screen, (255, 0, 0), hitbox_screen, 1)

            player_hitbox = self.camera.apply(self.player.rect.copy())
            pygame.draw.rect(self.screen, (0, 255, 0), player_hitbox, 1)
        
        fps = int(self.clock.get_fps())
        self.draw_ui(self.screen, fps)

        grid_x, grid_y = self.player.get_grid_position()

        # Mensagens do jogo
        if self.show_portal_message:
            self.draw_dialog_box(self.screen, "Parece que requer poder mágico para ativar.")
        elif self.show_warrior_message:
            self.draw_dialog_box(self.screen, "Apenas guerreiros podem entrar nesta arena!")
        elif self.show_boss_message:
            self.draw_dialog_box(self.screen, "Você precisa de uma chave para entrar!")
        elif self.show_forest_welcome:
            self.draw_dialog_box(self.screen, "Bem-vindo à Floresta Mágica! Apenas os portadores do cajado podem entrar aqui.")
        elif self.show_warrior_welcome:
            self.draw_dialog_box(self.screen, "Bem-vindo à Arena do Guerreiro! Apenas os portadores da espada podem entrar aqui.")
        elif self.current_map_name == "overworld" and grid_y < len(self.current_map_data) and grid_x < len(self.current_map_data[0]):
            if self.current_map_data[grid_y][grid_x] == 8:
                self.draw_dialog_box(self.screen, "Entre na casa para receber sua ESCOLHA.")
            elif ((grid_x, grid_y) == (20, 8) or (grid_x, grid_y) == (20, 9)):
                if self.player.has_weapon and self.player.weapon == "staff":
                    self.draw_dialog_box(self.screen, "Portal Mágico ativado! Passe para a Floresta Mágica.")
                else:
                    self.draw_dialog_box(self.screen, "Portal Mágico... Parece que requer poder mágico para ativar.")
            elif ((grid_x, grid_y) == (0, 8) or (grid_x, grid_y) == (0, 9)):
                if self.player.has_weapon and self.player.weapon == "sword":
                    self.draw_dialog_box(self.screen, "Arena do Guerreiro ativada! Entre para treinar.")
                else:
                    self.draw_dialog_box(self.screen, "Arena do Guerreiro... Apenas portadores da espada podem entrar.")
            elif ((grid_x, grid_y) == (8, 19) or (grid_x, grid_y) == (9, 19) or (grid_x, grid_y) == (10, 19)):
                if self.player.has_any_key():
                    self.draw_dialog_box(self.screen, "Entrada para a Luta Final! Pressione para entrar.")
                else:
                    self.draw_dialog_box(self.screen, "Entrada selada... Parece que precisa de uma chave.")
        elif self.current_map_name == "house_interior" and not self.player.has_weapon:
            if (grid_x, grid_y) == (1,1) or (grid_x, grid_y) == (2,1):
                self.draw_dialog_box(self.screen, "Pressione ESPAÇO para pegar a ESPADA!")
            elif (grid_x, grid_y) == (4,1) or (grid_x, grid_y) == (3,1):
                self.draw_dialog_box(self.screen, "Pressione ESPAÇO para pegar o CAJADO!")
        elif self.current_map_name == "house_interior" and self.player.has_weapon:
            if self.player.weapon == "sword":
                self.draw_dialog_box(self.screen, "Espada coletada! Pressione ESPAÇO para atacar.")
            elif self.player.weapon == "staff":
                self.draw_dialog_box(self.screen, "Cajado coletado! Pressione ESPAÇO para atacar.")
        elif self.current_map_name == "warrior_arena" and len(self.warrior_enemies) == 0 and self.warrior_key_spawned:
            center_x = len(self.current_map_data[0]) // 2
            center_y = len(self.current_map_data) // 2
            if (grid_x, grid_y) == (center_x, center_y):
                self.draw_dialog_box(self.screen, "Chave do Guerreiro! Pressione para coletar.")
        elif self.current_map_name == "forest_magic" and len(self.mage_enemies) == 0 and self.mage_key_spawned:
            center_x = len(self.current_map_data[0]) // 2
            center_y = len(self.current_map_data) // 2
            if (grid_x, grid_y) == (center_x, center_y):
                self.draw_dialog_box(self.screen, "Chave do Mago! Pressione para coletar.")

        # Tela de Game Over
        if self.game_over:
            self.draw_game_over_screen()
        
        # NOVO: Tela de Vitória
        if self.victory:
            self.draw_victory_screen()

        pygame.display.flip()

    def draw_player(self, screen: pygame.Surface):
        player_screen_rect = self.camera.apply(self.player.rect.copy())
        shadow_surf = pygame.Surface((int(self.player.w), int(self.player.h * 0.4)), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, Colors.SHADOW, shadow_surf.get_rect())
        shadow_pos = (player_screen_rect.x, player_screen_rect.y + int(player_screen_rect.h * 0.7))
        screen.blit(shadow_surf, shadow_pos)
        bob = 0
        if self.player.moving:
            bob = int(abs(pygame.math.Vector2(0, 1).rotate(self.player.animation_time * 400).y) * 3)
        player_rect_animated = player_screen_rect.copy()
        player_rect_animated.y -= bob
        
        # Efeito de piscar quando invulnerável
        if self.player.invulnerable and int(pygame.time.get_ticks() / 100) % 2 == 0:
            color = (255, 255, 255)  # Branco piscante
        elif self.player.has_weapon:
            if self.player.weapon == "sword":
                color = Colors.PLAYER
            else:
                color = (160, 32, 240)
        else:
            color = (200, 200, 200)
            
        pygame.draw.ellipse(screen, color, player_rect_animated)
        eye_size = max(3, int(player_screen_rect.w * 0.15))
        eye_y = player_rect_animated.y + player_rect_animated.h // 3
        left_eye_x = player_rect_animated.x + player_rect_animated.w // 3
        pygame.draw.circle(screen, Colors.WHITE, (left_eye_x, eye_y), eye_size)
        pygame.draw.circle(screen, Colors.BLACK, (left_eye_x, eye_y), eye_size // 2)
        right_eye_x = player_rect_animated.x + player_rect_animated.w * 2 // 3
        pygame.draw.circle(screen, Colors.WHITE, (right_eye_x, eye_y), eye_size)
        pygame.draw.circle(screen, Colors.BLACK, (right_eye_x, eye_y), eye_size // 2)

    def draw_ui(self, screen: pygame.Surface, fps: int):
        self.ui_surface.fill((0, 0, 0, 150))
        screen.blit(self.ui_surface, (0, 0))
        title = self.font_large.render("Floresta Encantada", True, (255, 255, 200))
        title_shadow = self.font_large.render("Floresta Encantada", True, (0, 0, 0))
        screen.blit(title_shadow, (config.SCREEN_WIDTH // 2 - title.get_width() // 2 + 2, 12))
        screen.blit(title, (config.SCREEN_WIDTH // 2 - title.get_width() // 2, 10))
        
        # Barra de vida do player
        health_text = self.font_small.render(f"Vida: {self.player.health}", True, Colors.WHITE)
        screen.blit(health_text, (10, 10))
        
        # NOVO: Mostra chaves coletadas
        keys_text = ""
        if self.player.has_warrior_key:
            keys_text += " Chave Guerreiro"
        if self.player.has_mage_key:
            keys_text += " Chave Mago"
        
        if keys_text:
            key_display = self.font_small.render(keys_text, True, Colors.KEY)
            screen.blit(key_display, (config.SCREEN_WIDTH - key_display.get_width() - 10, 10))
        
        # NOVO: Indicador de música
        music_status = "♪ ON" if pygame.mixer.music.get_busy() else "♪ OFF"
        music_text = self.font_small.render(f"Música: {music_status} (M: Mute +/-: Vol)", True, Colors.WHITE)
        screen.blit(music_text, (config.SCREEN_WIDTH // 2 - music_text.get_width() // 2, 35))
        
        bottom_surf = pygame.Surface((config.SCREEN_WIDTH, 40), pygame.SRCALPHA)
        bottom_surf.fill((0, 0, 0, 150))
        screen.blit(bottom_surf, (0, config.SCREEN_HEIGHT - 40))
        
        controls_text = "WASD/Setas: Mover  •  H: Hitboxes  •  ESC: Sair"
        if config.DEBUG_HITBOXES:
            controls_text += "  [DEBUG ON]"
        
        if self.player.has_weapon:
            weapon_name = "Espada" if self.player.weapon == "sword" else "Cajado Mágico"
            controls_text += f"  •  ESPAÇO: Atacar ({weapon_name})"
        else:
            controls_text += "  •  Entre na casa para escolher arma"

        controls = self.font_small.render(controls_text, True, Colors.WHITE)
        screen.blit(controls, (config.SCREEN_WIDTH // 2 - controls.get_width() // 2, config.SCREEN_HEIGHT - 30))
        grid_x, grid_y = self.player.get_grid_position()
        debug_text = self.font_small.render(f"Mapa: {self.current_map_name} | Pos: ({grid_x}, {grid_y}) | FPS: {fps}", True, (200, 200, 200))
        screen.blit(debug_text, (10, 35))

    def draw_dialog_box(self, screen: pygame.Surface, text: str):
        box_height = 100
        margin = 20
        box_rect = pygame.Rect(margin, config.SCREEN_HEIGHT - box_height - margin, config.SCREEN_WIDTH - margin * 2, box_height)
        pygame.draw.rect(screen, (255, 255, 255), box_rect)
        pygame.draw.rect(screen, (0, 0, 0), box_rect, 4)
        font = pygame.font.SysFont('Arial', 24, bold=True)
        wrapped_text = self.wrap_text(text, font, box_rect.width - 40)
        y_offset = box_rect.y + 20
        for line in wrapped_text:
            rendered = font.render(line, True, (0, 0, 0))
            screen.blit(rendered, (box_rect.x + 20, y_offset))
            y_offset += rendered.get_height() + 5

    def draw_game_over_screen(self):
        # Fundo semi-transparente
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(Colors.GAME_OVER_BG)
        self.screen.blit(overlay, (0, 0))
        
        # Texto de Game Over
        game_over_text = self.font_xlarge.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(game_over_text, (config.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                        config.SCREEN_HEIGHT // 2 - 100))
        
        # Instruções para reiniciar
        restart_text = self.font_large.render("Pressione R para reiniciar", True, Colors.WHITE)
        self.screen.blit(restart_text, (config.SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                      config.SCREEN_HEIGHT // 2))
        
        quit_text = self.font_small.render("ou ESC para sair", True, Colors.WHITE)
        self.screen.blit(quit_text, (config.SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 
                                   config.SCREEN_HEIGHT // 2 + 50))

    def draw_victory_screen(self):
        # Fundo semi-transparente verde
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(Colors.VICTORY_BG)
        self.screen.blit(overlay, (0, 0))
        
        # Texto de Vitória
        victory_text = self.font_xlarge.render("VITÓRIA!", True, (255, 255, 0))
        self.screen.blit(victory_text, (config.SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 
                                      config.SCREEN_HEIGHT // 2 - 100))
        
        # Mensagem de parabéns
        congrats_text = self.font_large.render("Você derrotou o Boss Final!", True, Colors.WHITE)
        self.screen.blit(congrats_text, (config.SCREEN_WIDTH // 2 - congrats_text.get_width() // 2, 
                                       config.SCREEN_HEIGHT // 2))
        
        # Instruções
        if self.victory_timer > 0:
            timer_text = self.font_small.render(f"Retornando em {int(self.victory_timer)} segundos...", True, Colors.WHITE)
            self.screen.blit(timer_text, (config.SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 
                                        config.SCREEN_HEIGHT // 2 + 50))

    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def restart_game(self):
        """Reinicia o jogo do zero"""
        self.game_over = False
        self.player.health = 5
        self.player.invulnerable = False
        self.player.invulnerable_timer = 0.0
        
        # Reseta armas
        self.player.has_weapon = False
        self.player.weapon = None
        self.sword_collected = False
        self.staff_collected = False
        
        # Reseta chaves
        self.player.has_warrior_key = False
        self.player.has_mage_key = False
        self.warrior_key_spawned = False
        self.mage_key_spawned = False
        
        # Limpa projéteis
        self.player.projectiles.clear()
        
        # Volta para o overworld
        self.change_map("overworld", (9, 14))
        
        print("Jogo reiniciado!")

    def run(self):
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Erro fatal: {e}")
        pygame.quit()
        sys.exit(1)