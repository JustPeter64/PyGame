import pygame

pygame.init()

"""
Screen
"""
screen_width = 1800
screen_height = 900
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Peters Platformer')
tile_size = 100

"""
constants
"""
fps = 60
timer = pygame.time.Clock()
player_scale = 12

# level = 18 tiles wide and 9 tiles heigh
level = [[0 for x in range(18)] for x in range(3)]

#level design test
# 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player, 5-9 is knowledge, 10 is door
level.append([0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
level.append([0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2])
level.append([0,0,0,0,3,6,0,0,0,7,0,0,0,0,0,8,2,1])
level.append([4,0,10,0,0,3,0,0,0,3,0,9,0,3,0,2,1,1])
level.append([2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1])
level.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

print(level)

# loop trough the full list and find where 4 (player) is
for y in range(len(level)):
    if 4 in level[y]:
        start_pos = (level[y].index(4), y)
        print(f"starting pos {start_pos}")


"""
Game variables
"""

player_x = start_pos[0] * tile_size 
player_y = start_pos[1] * tile_size - (12 * player_scale - tile_size) 
# remember initial location for respawn purposes
init_x = player_x
init_y = player_y

inventory = [False, False, False, False, False]
counter = 0
mode = 'idle'
in_air = False
direction = 1
player_speed = 12
colliding = False
x_change = 0
y_change = 0
jump_height = 15
gravity = 1


"""
Load images
"""
background = pygame.transform.scale(pygame.image.load('assets/images/background.png'), (screen_width, screen_height))
ground = pygame.transform.scale(pygame.image.load('assets/images/tiles/ground.png'), (tile_size, tile_size))
underground = pygame.transform.scale(pygame.image.load('assets/images/tiles/underground2.png'), (tile_size, tile_size))
platform = pygame.transform.scale(pygame.image.load('assets/images/tiles/platform.png'), (tile_size, 0.25 * tile_size))
door = pygame.transform.scale(pygame.image.load('assets/images/door.png'), (tile_size, tile_size))
lock = pygame.transform.scale(pygame.image.load('assets/images/lock.png'), (tile_size, tile_size))
knowledge_1 = pygame.transform.scale(pygame.image.load('assets/images/knowledge.png'), (tile_size, tile_size))
knowledge_2 = pygame.transform.scale(pygame.image.load('assets/images/knowledge.png'), (tile_size, tile_size))
knowledge_3 = pygame.transform.scale(pygame.image.load('assets/images/knowledge.png'), (tile_size, tile_size))
knowledge_4 = pygame.transform.scale(pygame.image.load('assets/images/knowledge.png'), (tile_size, tile_size))
knowledge_5 = pygame.transform.scale(pygame.image.load('assets/images/knowledge.png'), (tile_size, tile_size))
logo = pygame.transform.scale(pygame.image.load('assets/images/logo.png'), (300, 300)) 

player_frames = []
for x in range(4):
    player_frames.append(pygame.transform.scale(pygame.image.load(f'assets/images/player/player_stance_{x+1}.png'), (5 * player_scale, 12 * player_scale)))

 # 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player
tiles = ["", underground, ground, platform] # 0 is empty for easier coding later
collectables = [knowledge_1, knowledge_2, knowledge_3, knowledge_4, knowledge_5]

def show_menu():
    
    main_menu_background = pygame.image.load("assets/images/main_menu_background.png")
    main_menu_background = pygame.transform.scale(main_menu_background, (screen_width, screen_height))
    
    menu_running = True
    while menu_running:
        screen.blit(main_menu_background, (0, 0))
        
        font = pygame.font.SysFont(None, 74)
        title_surface = font.render("BASECAMP", True, (255, 255, 255))
        start_surface = font.render("press ENTER to start your journey", True, (255, 255, 255))
        exit_surface = font.render("press ESC to quit", True, (255, 255, 255))
        
        screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, screen_height // 2 - 100))
        screen.blit(start_surface, (screen_width // 2 - start_surface.get_width() // 2, screen_height // 2))
        screen.blit(exit_surface, (screen_width // 2 - exit_surface.get_width() // 2, screen_height // 2 + 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # start spel
                    menu_running = False
                elif event.key == pygame.K_ESCAPE:  # eit spel
                    pygame.quit()
                    exit()

        pygame.display.flip()


def draw_player(count, direcection, mod):
    """
    Drawes the player in the game
    :param count: frames in animation
    :param direcection: direction of movement 
    :param mod: idle, walking, maybe more
    """
    if mod != 'idle': # walking
        if direcection == 1: # to right
            screen.blit(player_frames[count // 5], (player_x, player_y))
        else: # to to left
            screen.blit(pygame.transform.flip(player_frames[count // 5], True, False), (player_x, player_y))
    else: # idle
        if direcection == 1: # to right
            screen.blit(player_frames[0], (player_x, player_y))
        else: # to to left
            screen.blit(pygame.transform.flip(player_frames[0], True, False), (player_x, player_y))



def draw_level(level):
    """
    Drawes tiles in the game
    loop trough level and find values and load sprites
    :param level: 2d list of tiles
    """
    # 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player, 5-9 is knowledge, 10 is door
    for x in range(len(level)):
        for y in range(len(level[x])):
            value = level[x][y]
            if 0 < value < 4:
                screen.blit(tiles[value], (y * tile_size, x * tile_size))
                # if value == 3: #visualize visual platform border
                    # pygame.draw.circle(screen, (  255,   0, 0), (y * tile_size, x * tile_size), 5)
                    # pygame.draw.circle(screen, (  255,   0, 0), (y * tile_size + 100, x * tile_size + 20), 5)
                    # pygame.draw.circle(screen, (  255,   0, 0), (y * tile_size, x * tile_size + 20), 5)
                    # pygame.draw.circle(screen, (  255,   0, 0), (y * tile_size + 100, x * tile_size), 5)
            elif 4 < value < 10:
                if not inventory[value - 5]: # not in inventory so draw it
                    screen.blit(collectables[value - 5], (y * tile_size, x * tile_size))
            elif value == 10:
                screen.blit(door, (y * tile_size, x * tile_size))
                if not inventory == [True, True, True, True, True]: 
                    # if not all knowledge is collected, draw lock
                    screen.blit(lock, (y * tile_size, x * tile_size))

def checkCollision(level):
    """
     Check if player is colliding
     Not actual position but visual so it looks good while playing
    :param level: 2d list of tiles
    """
    collide = False
    
    # hitbox of player
    right_coord = int((player_x + 60) // tile_size)
    left_coord = int(player_x // tile_size)
    top_coord = int((player_y + 10) // tile_size)
    bottom_coord = int((player_y + 140) // tile_size)

    top_right = level[top_coord][right_coord]
    bottom_right = level[bottom_coord][right_coord]
    top_left = level[top_coord][left_coord]
    bottom_left = level[bottom_coord][left_coord]
    #visualize hitbox
    # pygame.draw.circle(screen, (  0,   0, 255), (player_x + 60, player_y + 10), 5)
    # pygame.draw.circle(screen, (  0,   0, 255), (player_x + 60, player_y + 140), 5)
    # pygame.draw.circle(screen, (  0,   0, 255), (player_x, player_y + 10), 5)
    # pygame.draw.circle(screen, (  0,   0, 255), (player_x, player_y + 140), 5)

    # hitbox of player with knowledge
    right_coord_knowledge = int((player_x + 20) // tile_size)
    left_coord_knowledge = int(player_x // tile_size)
    top_coord_knowledge = int((player_y + 25) // tile_size)
    bottom_coord_knowledge = int((player_y + 140) // tile_size)

    top_right_knowledge = level[top_coord_knowledge][right_coord_knowledge]
    bottom_right_knowledge = level[bottom_coord_knowledge][right_coord_knowledge]
    top_left_knowledge = level[top_coord_knowledge][left_coord_knowledge]
    bottom_left_knowledge = level[bottom_coord_knowledge][left_coord_knowledge]

    # 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player, 5 is knowledge

    if top_coord >= 0: # check if player moves higher than screen and top coords collide
        # check if player collides with something on the right or left
        if 0 < top_right < 3 or 0 < bottom_right < 3:
            collide = 1
        elif 0 < top_left < 3 or 0 < bottom_left < 3:
            collide = -1
        else:
            collide = 0
    elif bottom_right >= 0: # check if player moves higher than screen and bottom coords collide
        if 0 < bottom_right < 3:
            collide = 1
        elif 0 < bottom_right < 3:
            collide = -1
        else:
            collide = 0
    else:
        collide = 0

    # Contact with knowledge
    if 5 <= top_left_knowledge <= 9: # when colliding with knowledge, 
        if not inventory[top_left_knowledge - 5]:
            inventory[top_left_knowledge - 5] = True
    elif 5 <= top_right_knowledge <= 9: 
        if not inventory[top_right_knowledge - 5]:
            inventory[top_right_knowledge - 5] = True
    elif 5 <= bottom_left_knowledge <= 9: 
        if not inventory[bottom_left_knowledge - 5]:
            inventory[bottom_left_knowledge - 5] = True
    elif 5 <= bottom_right_knowledge <= 9: 
        if not inventory[bottom_right_knowledge - 5]:
            inventory[bottom_right_knowledge - 5] = True

    return collide

# check feet collision on landings
def check_verticals(y_pos):
    """
     Check if player should fall or stay on tile
     Not actual position but visual so it looks good while playing
     :param y_pos: player y position
    """
    center_coord = int((player_x + 25) // tile_size)
    bottom_coord = int((player_y + 140) // tile_size)
    # pygame.draw.circle(screen, (  0,   255, 0), (player_x + 25, player_y + 140), 5)
    
    top_coord_platform = int((player_y + 240) // tile_size)
    # pygame.draw.circle(screen, (  255,   0, 0), (player_x + 25, player_y + 240), 5)

    bottom_coord_platform = int((player_y + 40) // tile_size)
    # pygame.draw.circle(screen, (  0,   0, 255), (player_x + 25, player_y + 40), 5)

    # 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player, 5 is knowledge
    if player_y + 110 > 0: # if full player is in level
        if 0 < level[bottom_coord][center_coord] <  4: # ground or underground
            falling = False
        # elif level[bottom_coord_platform][center_coord] == 3: # platform
        #     falling = False
        else:
            falling = True
    else:
        falling = True
    if not falling: # compensate for falling trough a tile
        y_pos = (bottom_coord - 1) * 100 - 41

    return falling, y_pos

"""
Game loop
"""
show_menu()
game_running = True
while game_running:
    
    
    timer.tick(fps)

    if counter < 19: # counter for frames of player animation
        counter += 1
    else:
        counter = 1

    screen.blit(background, (0,0))
    draw_level(level)
    draw_player(counter, direction, mode)
    colliding = checkCollision(level)

    # handle player movement
    if mode == 'walk':
        if direction == -1 and player_x > 0 and colliding != -1: # player moves to left
            player_x -= player_speed
        elif direction == 1 and player_x < screen_width - 50 and colliding != 1: # player moves to right
            player_x += player_speed

    
    # jumping code
    if in_air:
        y_change -= gravity
        player_y -= y_change
    in_air, player_y = check_verticals(player_y)
    if not in_air:
        y_change = 0

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: # arrow right 
                direction = 1
                mode = 'walk'
            elif event.key == pygame.K_LEFT: # arrow left
                direction = -1
                mode = 'walk'
            elif event.key == pygame.K_SPACE and not in_air: # spacebar
                in_air = True
                y_change = jump_height
            elif event.key == pygame.K_UP and not in_air: # arrow up
                in_air = True
                y_change = jump_height
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction == 1:
                mode = 'idle'
            elif event.key == pygame.K_LEFT and direction == -1:
                mode = 'idle'
                

    pygame.display.flip()

# Quit Pygame
pygame.quit()
