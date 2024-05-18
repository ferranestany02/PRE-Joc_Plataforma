import pygame


class Coins:
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        self.action = ''
        self.anim_offset = (-3, -3)

        self.set_action('coin/rotate')

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.action].copy()

    def update(self, tilemap, movement=(0, 0)):

        self.animation.update()
        self.set_action('coin/rotate')

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
