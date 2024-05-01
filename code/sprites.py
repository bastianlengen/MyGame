from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None, z = Z_LAYERS['main']):
        super().__init__(groups)

        # Images
        self.image = surf
        self.z = z

        # Rectangles
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()


class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z = Z_LAYERS['main'], animation_speed = ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)

