import pygame
from camera import CameraGroup
from save import SaveData
from dialog import DialogBox



all_sprites = pygame.sprite.Group()

projectile_sprites = pygame.sprite.Group()

ennemi_projectiles = pygame.sprite.Group()

items_drop = pygame.sprite.Group()

ennemi_group = pygame.sprite.Group()
pnj_group = pygame.sprite.Group()
player_sprite = pygame.sprite.GroupSingle()
player = None
items_drop = pygame.sprite.Group()
items_sprites = pygame.sprite.Group()

#Messages
dialogues_Emma_salon = DialogBox(["Salut, utilisateur Sarah.", "Je m'appelle Emma, et je serais ton guide. ", "Ton objectif sera de trouver dans mon ordinateur une donnée sensible.", "Pour cela, tu vas devoir rentrer dans mon ordinateur.", "Ne t'inquiète pas, je serais là pour te guider.", "Bon courage."])
dialogues_Emma_teleporter = DialogBox(["Bienvenue !", "Tu te situe dans mon ordinateur", "Maintenant, tu vas te diriger vers la porte en bas...", "Ce sera l'entrée vers le firewall", "Je t'expliquerai à l'intérieur ta mission"])
dialogues_Emma_firewall = DialogBox(["Un des ordinateurs dans le fond est allumé, trouve le.", "Il va te permettre de trouver un port qui te permettra de rentrer dans le serveur", "Tu devras te connecter avec l'identifiant root...", "... c'est l'administrateur du serveur, il a tous les droits.", "Tentes de rentrer ces mots de passes : 1234, azerty, admin, root"])
dialogues_Emma_server = DialogBox(["Tu as réussi à rentrer dans le serveur, bien joué !", "Maintenant tu vas tenter d'attaquer la base de données", "Pour cela tu vas chercher quelques indices parmi les différentes salles autour.", "Ce sont des réseaux, dont l'un possède la BDD", "Bonne chance !"])
salon_collisions = pygame.sprite.Group()
teleporter_collisions = pygame.sprite.Group()
firewall_collisions = pygame.sprite.Group()
server_collisions = pygame.sprite.Group()

camera_groups = {
    "Salon": CameraGroup(name_map='Salon', list_teleporters=[('EntranceTeleporter', 'Teleporter', 'EntranceTeleporter')], layers_obstacles=(['Collisions'], salon_collisions), messages=dialogues_Emma_salon),
    "Teleporter": CameraGroup(name_map='Teleporter', list_teleporters=[('ExitTeleporter', 'Salon', 'ExitTeleporter'), ('EntranceFirewall', 'Firewall', 'EntranceFirewall')], layers_obstacles=(['Collisions'], teleporter_collisions), messages=dialogues_Emma_teleporter),
    "Firewall": CameraGroup(name_map='Firewall', list_teleporters=[('ExitFirewall', 'Teleporter', 'ExitFirewall'), ('EntranceServer', 'Server', 'EntranceServer')], layers_obstacles=(['Collisions'], firewall_collisions), messages=dialogues_Emma_firewall),
    "Server": CameraGroup(name_map='Server', list_teleporters=[('ExitServer', 'Firewall', 'ExitServer')], layers_obstacles=(['Collisions'], server_collisions), messages=dialogues_Emma_server)
}
# Water Fall ;)

save_data = SaveData('save.json')
map_name = save_data.load_player_map()
mob_dead = save_data.load_mob_dead()

if map_name is None:
    camera_group = camera_groups["Salon"]
else:
    camera_group = camera_groups[map_name]