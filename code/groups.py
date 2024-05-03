import pygame

from settings import *
from sprites import ShootingStarSprite
from random import choice, uniform
from timer import Timer

class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height, horizon_line, bg_type, bg_tiles_dict=None, top_limit=0):
        super().__init__()

        # Camera
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()  # Offset for the camera

        # Level dimension
        self.width = width * TILE_SIZE
        self.height = height * TILE_SIZE
        self.borders = {
            'left': 0,
            'right': -self.width + WINDOW_WIDTH,
            'bottom': -self.height + WINDOW_HEIGHT,
            'top': top_limit,
        }

        # Background
        self.bg_type = bg_type
        self.bg_tiles_dict = bg_tiles_dict
        self.horizon_line = horizon_line
        if bg_type in ['forest_night']:
            # Trees
            self.bg_tiles_x = [0] * len(self.bg_tiles_dict)
            # Stars
            self.n_stars = 75
            self.distance_min_stars = 75
            self.star_x_speed_ratio = 3  # 1/3 of the speed of the camera
            # Shooting stars
            self.timer_shooting_stars = Timer(100)


    def camera_constraint(self):
        # Left limit
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders['left']
        # Right limit
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']
        # Bottom
        self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']
        # Top
        self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else self.borders['top']


    def draw_background(self, dt):
        # Forest night
        if self.bg_type == 'forest_night':
            # Sky
            self.display_surface.fill('#405273')

            # Horizon Line
            horizon_pos = self.horizon_line + self.offset.y
            #pygame.draw.line(self.display_surface, '#f5f1de', (0, horizon_pos),
            #                 (WINDOW_WIDTH, horizon_pos), 4)

            # Ground
            sea_rect = pygame.FRect(0, horizon_pos, WINDOW_WIDTH, WINDOW_HEIGHT - horizon_pos)
            pygame.draw.rect(self.display_surface, '#14233a', sea_rect)

            # Draw stars
            self.draw_random_stars(self.bg_tiles_dict['stars'])
            self.create_random_shooting_stars(self.bg_tiles_dict['shooting_stars'])

            # Draw trees
            self.draw_bg_large_tile(0, self.bg_tiles_dict['back_trees'])
            self.draw_bg_large_tile(1, self.bg_tiles_dict['mid_trees'])
            self.draw_bg_large_tile(2, self.bg_tiles_dict['front_trees'])


    def draw_bg_large_tile(self, index, surf, additonal_y_offset = 0):
        tile_width, tile_height = surf.get_size()

        # Draw
        n_tiles = int(self.width / tile_width) + 2
        for tile in range(n_tiles):
            left = self.bg_tiles_x[index] + tile * tile_width + self.offset.x * (index/5+0.5)
            top = self.horizon_line - tile_height + self.offset.y + additonal_y_offset
            self.display_surface.blit(surf, (left, top))

        # Reset if too far
        if self.bg_tiles_x[index] <= - tile_width:
            self.bg_tiles_x[index] = 0


    def draw_random_stars(self, surfs):
        # Draw the random keys and positions if not already done
        if not hasattr(self, 'stars_surf'):
            self.stars_pos = []
            self.stars_surf = []
            for i in range(self.n_stars):
                too_close = True
                while too_close:
                    # Draw
                    x = uniform(0, WINDOW_WIDTH)
                    y = uniform(-100, self.horizon_line - 100)
                    key = choice(list(surfs.keys()))
                    alpha = uniform(20, 220)
                    scale = uniform(0.5, 1)
                    too_close = False
                    for existing_pos in self.stars_pos:
                        if (abs(x - existing_pos[0]) + abs(y - existing_pos[1])) < self.distance_min_stars:
                            too_close = True
                            break
                # Modify the surface and save it
                surf = surfs[key]
                surf.set_alpha(alpha)
                original_size = surf.get_size()
                new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                surf = pygame.transform.scale(surf, new_size)
                self.stars_surf.append(surf)
                self.stars_pos.append((x,y))


        # Draw the stars
        for ((x,y), star_surf) in zip(self.stars_pos, self.stars_surf):
            if x + self.offset.x/self.star_x_speed_ratio < 0:
                x += WINDOW_WIDTH
            star_rect = star_surf.get_frect(center=(x + self.offset.x/self.star_x_speed_ratio,y + self.offset.y))
            self.display_surface.blit(star_surf, star_rect)


    def create_random_shooting_stars(self, frames):
        self.timer_shooting_stars.update()
        if not self.timer_shooting_stars.active:
            key = choice(list(frames.keys())+[None,None])
            if key:
                y = -self.borders['top']
                x = uniform(0, self.width)
                ShootingStarSprite( pos = (x, y),
                                    frames = frames[key],
                                    groups = self)
            self.timer_shooting_stars.activate()


    def draw(self, target_pos, dt):  # Overwrite the basic draw method for sprite.Group()
        # Camera movement
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
        self.camera_constraint()

        # Draw the sky
        self.draw_background(dt)

        # Draw the sprites
        for sprite in sorted(self, key=lambda sprite: sprite.z):  # Sorted according to the Z_LAYERS
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)