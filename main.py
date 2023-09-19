import pygame, sys, time, math, introduction
from settings import *
import sprites
from debug import debug
from carte import Carte
from player import *
from ennemy import *
from menu import Menu
from items import Item
from random import randint
from pnj import *
from menu_marchand import *
from dialog import DialogBox

pygame.init()

clock = pygame.time.Clock()

# Création des sprites

# Saves
menu = Menu()
sprites.player = menu.run()
last_save_time = pygame.time.get_ticks()

# Dialogues
dialogs_Emma_box = DialogBox(["Nique les arabes", "Paul : Aller ptit café", "Etienne, très bon gars", "Vive Dane et me mafé"])
Emma = Emma("Emma", sprites.camera_group.carte.get_waypoint('SpawnEmma'), [sprites.camera_groups["Salon"], sprites.pnj_group])

# Type camera
sprites.camera_group.set_type_camera("center")

last_time = time.time()
while True:
    dt = time.time() - last_time
    last_time = time.time()
    
    if sprites.player.is_teleporting:
        sprites.player.is_teleporting = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player_position = {"x": sprites.player.pos.x, "y": sprites.player.pos.y}
            sprites.save_data.save_player_position(player_position)
            sprites.save_data.save_player_map(sprites.camera_group.carte.map_name)
            sprites.save_data.save_player_life(sprites.player.get_HP())
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                player_position = {"x": sprites.player.pos.x, "y": sprites.player.pos.y}
                sprites.save_data.save_player_position(player_position)
                sprites.save_data.save_player_map(sprites.camera_group.carte.map_name)
                sprites.save_data.save_player_life(sprites.player.get_HP())
                pygame.quit()
                sys.exit()

            for tp in sprites.camera_group.teleporters:
                if event.key == pygame.K_e and sprites.player.rect.colliderect(tp.rect):
                    name_dest = tp.name_destination
                    sprites.camera_group = sprites.camera_groups[name_dest]
                    sprites.player.set_pos(sprites.camera_groups[name_dest].carte.get_waypoint(tp.name_tp_back))
                    sprites.player.is_teleporting = True
            for sprite in sprites.items_drop:
                if event.key == pygame.K_a and sprites.player.rect.colliderect(sprite.rect):
                    sprite.remove_object(sprites.items_drop)

            if event.key == pygame.K_SPACE:
                dialogs_Emma_box.next_text()
                

    # Background color depends of the map
    dungeon_bg = ['Dungeon']
    overworld_bg = ['Overworld', 'Swamp', 'Waterfall', 'Watertemple', 'Castle']
    watertemple_bg = ['Watertemple']
    salon_bg = ['Salon']
    if sprites.camera_group.carte.map_name in dungeon_bg:
        screen.fill('#1f1f1f') #Map Dungeon
    elif sprites.camera_group.carte.map_name in overworld_bg:
        screen.fill('#71ddee') #Map overworld
    elif sprites.camera_group.carte.map_name in watertemple_bg:
        screen.fill('#1e7cb8')
    elif sprites.camera_group.carte.map_name in salon_bg:
        screen.fill('#000000')

    if not sprites.player.is_alive():
        sprites.camera_group.carte.game_over()
        sprites.player = menu.run()

    sprites.camera_group.update(dt)
    sprites.camera_group.custom_draw(sprites.player)
    dialogs_Emma_box.render()

    # Permettre de debuger les sprites
    # sprites.camera_group.debug()

    # Sauvegarde la position du joueur toutes les 5 secondes
    current_time = pygame.time.get_ticks()
    if current_time - last_save_time > 5000:
        player_position = {"x": sprites.player.pos.x, "y": sprites.player.pos.y}
        sprites.save_data.save_player_position(player_position)
        sprites.save_data.save_player_map(sprites.camera_group.carte.map_name)
        sprites.save_data.save_player_life(sprites.player.get_HP())
        last_save_time = current_time

    # print(sprites.player)
    pygame.display.update()
    clock.tick(60)

