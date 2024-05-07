from pytmx.util_pygame import load_pygame
import os

from settings import *
from support import *
from data import Data
from level import Level
from debug import debug
from ui import UI

class Game():
    def __init__(self):
        # Launch the game
        pygame.init()

        # Create the screen
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Le jeu de la galère: Forest')
        self.clock = pygame.time.Clock()   # For the FPS

        # Import images
        self.import_assets()

        # Import data
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)

        # Import UI:
        # TODO

        # Import levels
        self.tmx_maps = {
            0: load_pygame(join('data', 'levels', 'test.tmx')),
        }

        # Set the current stage
        self.current_stage = Level(self.tmx_maps[0], self.level_frames, self.data, self.switch_stage)


    def import_assets(self):
        self.level_frames = {
            'player': import_sub_folders('graphics', 'player'),
            'forest_night': import_folder_dict('graphics', 'background', 'forest_night'),
            'stars': import_images_from_spritesheet(4,2, 'graphics', 'background','stars','stars', name='star'),
            'shooting_stars': import_animations_from_spritsheets(3,2, ['shooting_star_red', 'shooting_star_yellow'],
                                                                 'graphics', 'background','stars', 'shooting_stars'),
        }
        self.font = pygame.font.Font(join( 'graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart': import_image('graphics', 'ui', 'heart'),
            'duck': import_image('graphics', 'ui', 'duck'),
        }

    def switch_stage(self, target, unlock = 0):
        # TODO
        pass

    def check_game_over(self):
        # TODO
        pass

    def run(self):
        while True:
            # Store the time between 2 images to normalize the speed of the movement
            dt = self.clock.tick(60) / 1000

            # Go through the events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Game over
            self.check_game_over()

            # Run the current stage
            self.current_stage.run(dt)

            # Update UI
            self.ui.update(self.data)

            # Debug
            # debug(dt)

            # Update what's on screen
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()