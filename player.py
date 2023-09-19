from caracter import *
from sprites import *

class Player(Caracter):
    type = 'Player'
    
    def __init__(self, name, pos, groups):
        super().__init__(name, pos, groups)
        self.transform_to_player()
    
    def transform_to_player(self):
        self.frames["Bottom Walk"] = player_bottom_walks
        self.frames["Left Walk"] = player_left_walks
        self.frames["Top Walk"] = player_top_walks
        self.frames["Right Walk"] = player_right_walks
        self.image = self.frames[self.animation_direction][self.animation_index]
        self.image = self.transform_scale()
    
    def is_alive(self):
        if self.HP == 0:
            self.kill()
            return False
        return True
    
    def input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        
        if mouse[0] and (self.get_ticks() - self.last_shot > self.cooldown_attack):
            self.shoot()
        
        if keys[pygame.K_z] or keys[pygame.K_s] or keys[pygame.K_d] or keys[pygame.K_q]:
            if keys[pygame.K_z]:
                self.direction.y = -1
                self.animation_direction = 'Top Walk'
                self.is_moving = True
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.animation_direction = 'Bottom Walk'
                self.is_moving = True
            else:
                self.direction.y = 0
                
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.animation_direction = 'Right Walk'
                self.is_moving = True
            elif keys[pygame.K_q]:
                self.direction.x = -1
                self.animation_direction = 'Left Walk'
                self.is_moving = True
            else:
                self.direction.x = 0
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.is_moving = False
            self.animation_index = 0

    def shoot(self):
        Projectile(self, [sprites.projectile_sprites] + list(sprites.camera_groups.values()))
        self.last_shot = pygame.time.get_ticks()  # on enregistre le temps du dernier tir
        self.is_attack = True
        
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.apply_collisions(dt)
        self.animation_state()
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

class Archer(Player):
    type = "Archer"
    
    def __init__(self, name, pos, groups):
        super().__init__(name, pos, groups)
        self.transform_to_archer()
    
    def transform_to_archer(self):
        """Transformer le player en warrior"""
        self.frames['Bottom Walk'] = archer_bottom_walks
        self.frames['Left Walk'] = archer_left_walks
        self.frames['Top Walk'] = archer_top_walks
        self.frames['Right Walk'] = archer_right_walks
        self.frames['Bottom Attack'] = archer_bottom_walks
        self.frames['Left Attack'] = archer_left_attack
        self.frames['Top Attack'] = archer_top_attack
        self.frames['Right Attack'] = archer_right_attack
        self.image = self.frames[self.animation_direction][self.animation_index]
        self.image = self.transform_scale()
        self.set_range(75)
        self.set_max_HP(95)
        self.set_HP(self.get_max_HP())
        self.set_attack_value(18)
        self.set_defense_value(2)
        self.set_cooldown_attack(850)
        self.set_speed(450)