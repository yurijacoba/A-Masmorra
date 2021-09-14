from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from tile import *
from Map import *
from Player import *
from Enemy import *
from Menu import *
from UI import *
from Npc import *
import random

window = Window(800, 600)
keyboard = Window.get_keyboard()
mouse = Window.get_mouse()
window.set_title("A Masmorra")

tiles = wall_tileset = Tileset([
    Tile("resources/tiles/floor/floor_1.png", 1, 0),
    Tile("resources/tiles/floor/floor_2.png", 1, 0),
    Tile("resources/tiles/floor/floor_3.png", 1, 0),
    Tile("resources/tiles/wall/wall_corner_bottom_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_bottom_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_front_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_front_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_top_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_top_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_fountain_top.png", 1, 2),
    Tile("resources/tiles/wall/wall_hole_1.png", 1, 2),
    Tile("resources/tiles/wall/wall_hole_2.png", 1, 2),
    Tile("resources/tiles/wall/wall_inner_corner_l_top_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_inner_corner_l_top_rigth.png", 1, 2),
    Tile("resources/tiles/wall/wall_inner_corner_mid_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_inner_corner_mid_rigth.png", 1, 2),
    Tile("resources/tiles/wall/wall_inner_corner_t_top_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_inner_corner_t_top_rigth.png", 1, 2),
    Tile("resources/tiles/wall/wall_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_mid.png", 1, 2),
    Tile("resources/tiles/wall/wall_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_side_front_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_side_front_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_side_mid_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_side_mid_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_side_top_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_side_top_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_top_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_top_mid.png", 1, 2),
    Tile("resources/tiles/wall/wall_top_right.png", 1, 2)
    ])

state = "menu"
map_level = 0
bg = Sprite("assets/bg.png")
main_menu = Menu()
main_menu.organize(window, "main")
map = Map(800, 600, 48, 48, tiles, 3)
player = Player()
wiz = Npc()
player.set_initial_position(map.get_layer(0), map.get_grid_size())
enemies = []
enemies_type = ["goblin", "zombie"]
ui = UI(window, player.get_max_life(), player.get_exp(), player.get_level())


#---------------------Funções Auxiliares---------------------
def move(key: str):
    if(player.can_move(map.get_layer(0), key)):
        player.move(key, map.get_grid_size())

def decrease_delays():
    player.decrease_all_delay(window.delta_time())
    for i in range(len(enemies)):
        enemies[i].decrease_all_delay(window.delta_time())

def animations():
    player.move_animation(window.delta_time())
    player.attack_animation(window.delta_time())
    for i in range(len(enemies)):
        enemies[i].move_animation(window.delta_time())
    if(wiz.is_active()):
        wiz.summon_animation(window.delta_time(), map.get_grid_size())

def damage_control():
    for i in range(len(enemies)):
        if(player._weapon.collided(enemies[i].get_sprite()) and player.is_attacking()):
            enemies[i].get_damage(player.get_str() + 5*(random.randint(0,1)))
        if(player.get_sprite().collided(enemies[i].get_sprite())):
            player.get_damage(enemies[i].get_size() * 0.5)
            ui.update_life_display(player, enemies[i].get_size() * 0.5)

def level_control():
    exp_to_next = (((player.get_level() - 1)**2) * 15) + 55
    if(player.get_exp() >= exp_to_next):
        player.level_up()
        player.set_exp(0)
        ui.level_up()
        ui.set_exp(0)

def enemies_draw():
    for i in range(len(enemies)):
        enemies[i].draw(window)

def clear_enemies():
    for i in range(len(enemies)):
        if(i < len(enemies)):
            if(enemies[i].get_life() <= 0):
                gain = (enemies[i].get_max_life() / 3) * enemies[i].get_size()
                player.add_exp(gain)
                ui.add_exp(gain)
                enemies.pop(i)

#-------------------------Game State-------------------------
def play():
    global state
    global map_level

    # Geração de inimigos para teste
    if(map_level == 0):
        for i in range(2):
            new_enemy = Enemy(enemies_type[random.randint(0,1)], 1)
            enemies.append(new_enemy)
            enemies[i].set_initial_position(map.get_layer(0), map.get_grid_size(), player)
            map_level += 1

    if((len(enemies) == 0) and (not wiz.is_active())):
        wiz.set_position(map.get_layer(0), map.get_grid_size(), player)
        wiz.set_active()
    # Update do Player
    if(keyboard.key_pressed("W")):
        move("u")
    if(keyboard.key_pressed("A")):
        move("l")
    if(keyboard.key_pressed("S")):
        move("d")
    if(keyboard.key_pressed("D")):
        move("r")

    if((mouse.get_position()[0] < player.get_sprite().x) and (player.get_facing() == "right")):
        player.flip_sprite()
    if((mouse.get_position()[0] > player.get_sprite().x) and (player.get_facing() == "left")):
        player.flip_sprite()

    if(mouse.is_button_pressed(1)):
        player.attack()

    # Update dos inimigos
    for i in range(len(enemies)):
        enemies[i].move(map.get_layer(0), map.get_grid_size(), player)
    clear_enemies()

    # Updates Unificados
    decrease_delays()
    animations()
    damage_control()
    level_control()

    # Draw dos Game Objects
    bg.draw()
    map.draw_layer(0)
    enemies_draw()
    if(player.can_move(map.get_layer(0), 'u')):
        player.draw()
        map.draw_layer(2)
    else:
        map.draw_layer(2)
        player.draw()
    wiz.draw()
    ui.draw()
    window.update()

def menu():
    global state

    # Update dos Game Objects
    for name in main_menu.get_buttons_name():
        if(mouse.is_over_object(main_menu.get_button(name))):
            main_menu.set_selected_over(name)
            if(mouse.is_button_pressed(1)):
                main_menu.play_selected()
                state = name
                
    # Draw/play dos Game Objects
    main_menu.play_bgm()
    bg.draw()
    main_menu.draw()
    window.update()

#-------------------------Game Loop-------------------------
while(state != "exit"):
    if(state == "menu"):
        menu()
    if(state == "play"):
        play()
