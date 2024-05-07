from settings import *


class UI():
    def __init__(self, font, surfs):
        self.display_surface = pygame.display.get_surface()
        self.font = font
        self.padding = 5

        # Health
        self.heart_surf = surfs['heart']
        self.heart_surf_width = self.heart_surf.get_width()
        self.heart_surf_height = self.heart_surf.get_height()

        # Ducks
        self.duck_surf = surfs['duck']
        self.duck_amount = 0

    def draw_hearts(self, amount):
        for i in range(amount):
            x = 8 + i * (self.padding + self.heart_surf_width)
            y = 8
            heart_rect = self.heart_surf.get_frect(topleft = (x,y))
            self.display_surface.blit(self.heart_surf, heart_rect)

    def draw_ducks(self, amount):
        # Text
        text_surf = self.font.render(str(amount), False, '#f1f6f0')
        text_rect = text_surf.get_frect(topleft=(8, 8 + self.padding + self.heart_surf_height))
        self.display_surface.blit(text_surf, text_rect)

        # Ducks
        x,y = text_rect.topright
        duck_rect = self.duck_surf.get_frect(topleft = (x, y + self.padding))
        self.display_surface.blit(self.duck_surf, duck_rect)

    def update(self, data):
        self.draw_hearts(data.health)
        self.draw_ducks(data.ducks)
