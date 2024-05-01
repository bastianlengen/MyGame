from settings import *
from groups import AllSprites
from sprites import Sprite, AnimatedSprite
from player import Player

class Level():
    def __init__(self, tmx_map, level_frames, data, switch_stage):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.switch_stage = switch_stage

        # Level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties

        # Groups
        bg_type = tmx_level_properties['bg']
        if bg_type == 'forest_night':
            bg_tiles_dict = level_frames['forest_night']
            bg_tiles_dict['stars'] = level_frames['stars']
        else:
            bg_tiles_dict = None
        self.all_sprites = AllSprites(
            width=tmx_map.width,
            height=tmx_map.height,
            top_limit=tmx_level_properties['top_limit'],
            bg_type=bg_type,
            bg_tiles_dict=bg_tiles_dict,
            horizon_line=tmx_level_properties['horizon_line']
        )
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        '''
        self.damage_sprites = pygame.sprite.Group()
        self.tooth_sprites = pygame.sprite.Group()
        self.pearl_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        '''

        # Set up the level
        self.setup(tmx_map, level_frames)

        # Frames
        '''
        self.pearl_surf = level_frames['pearl']
        self.particle_frames = level_frames['particle']
        '''

    def setup(self, tmx_map, level_frames):
        # Get the terrain
        for layer in ['Terrain']:
            # TODO
            # add Platforms, BG and FG
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                # Assign each tile to its corresponding groups
                groups = [self.all_sprites]
                if layer == 'Terrain': groups.append(self.collision_sprites)
                if layer == 'Platforms': groups.append(self.semi_collision_sprites)
                # Assign their correct z-value
                match layer:
                    case 'BG':
                        z = Z_LAYERS['bg tiles']
                    case 'FG':
                        z = Z_LAYERS['bg tiles']
                    case _:
                        z = Z_LAYERS['main']
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

        # Get the bg details
        # TODO

        # Get the objects (and the player)
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    semi_collision_sprites=self.semi_collision_sprites,
                    frames=level_frames['player'],
                    data=self.data
                )
            else:
                pass

            # Get the moving objects
            # TODO

            # Get the enemies
            # TODO

            # Get the items
            # TODO

            # Get the water
            # TODO

    def check_constraint(self):
        # Left and right
        if self.player.hitbox_rect.left <= 0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right >= self.level_width:
            self.player.hitbox_rect.right = self.level_width

        # Bottom border
        if self.player.hitbox_rect.bottom >= self.level_bottom:
            # TODO
            print('Death')

        # Success state, i.e. reached the flag
        # TODO

    def run(self, dt):
        self.display_surface.fill('black')

        # Update
        self.all_sprites.update(dt)
        self.check_constraint()

        # Draw
        self.all_sprites.draw(self.player.hitbox_rect.center, dt)