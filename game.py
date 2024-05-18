import os
import sys
import math
import random

import pygame

from scripts.utils import carga_mapa, carga_musica
from scripts.entities import Player, Enemy
from scripts.tilemap import Tilemap
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.coins_2 import Coins
from scripts.Settings import Settings
from Menu import Menu
import scripts.game_functions as gf


class Game:
    def __init__(self):
        pygame.init()

        self.ai_setting = Settings()

        self.screen = pygame.display.set_mode((self.ai_setting.screen_width, self.ai_setting.screen_height))

        pygame.display.set_caption('Juego de plataforma')
        self.display = pygame.Surface((self.ai_setting.screen_width, self.ai_setting.screen_height), pygame.SRCALPHA)

        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        self.score = 0

        self.assets = carga_mapa()
        self.sfx = carga_musica()

        self.sfx['coin'].set_volume(self.ai_setting.volumen_coin)
        self.sfx['dash'].set_volume(self.ai_setting.volumen_dash)
        self.sfx['ambience'].set_volume(self.ai_setting.volumen_ambience)
        self.sfx['jump'].set_volume(self.ai_setting.volumen_jump)
        self.sfx['hit'].set_volume(self.ai_setting.volumen_hit)
        self.sfx['shoot'].set_volume(self.ai_setting.volumen_shoot)

        self.menu = Menu()

        self.fuente_juego = pygame.font.SysFont("Arial", 16)

        self.player = Player(self, (50, 50), (16, 41))

        self.tilemap = Tilemap(self, tile_size=32)

        self.level = 0
        self.load_level(self.level)

    def load_level(self, map_id):
        self.tilemap.load('map.json')
        # self.tilemap.load('data/maps/' + str(map_id) + '.json')

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (16, 28)))

        self.coins = []
        for c in self.tilemap.extract([('coin', 0)], keep=False):
            self.coins.append(Coins(self, c['pos'], (32, 32)))

        self.projectiles = []
        self.particles = []
        self.sparks = []
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

    def main_menu(self):

        while True:

            self.menu.draw_button(self.screen, self.menu.jugar_but())
            self.menu.draw_button(self.screen, self.menu.inst_but())
            self.menu.draw_button(self.screen, self.menu.quit_but())

            self.screen.blit(self.menu.back_menu, (0, 0))

            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.menu.jugar_but().collidepoint((mx, my)):
                            self.run()

                        if self.menu.inst_but().collidepoint((mx, my)):
                            self.instructions()

                        if self.menu.quit_but().collidepoint((mx, my)):
                            pygame.quit()
                            exit()

            pygame.display.update()
            self.clock.tick(60)

    def instructions(self):
        while True:
            self.screen.blit(self.menu.back_instructions, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()

            self.screen.blit(self.menu.back_instructions, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.sfx['ambience'].play(-1)

        while True:

            self.display.fill((0, 0, 0, 0))
            self.display.blit(self.assets['background'], (0, 0))

            # Coins collect
            for c in self.coins:
                if self.player.rect().colliderect(c.rect):
                    self.score += 1
                    self.coins.remove(c)
                    self.sfx['coin'].play(0)

            for c in self.coins.copy():
                collect = c.update(self.tilemap, (0, 0))
                c.render(self.display, offset=self.scroll)
                if collect:
                    self.coins.remove(c)

            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)

            if self.transition < 0:
                self.transition += 1

            if self.dead:
                self.score = 0
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.load_level(self.level)

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1

                if self.player.rect().centerx < enemy.rect().centerx:
                    img = self.assets['arrow_1']
                else:
                    img = self.assets['arrow_2']

                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0],
                                        projectile[0][1] - img.get_height() / 2 - render_scroll[1]))

                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(
                            Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0),
                                  2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.sfx['hit'].play()
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center,
                                                           velocity=[math.cos(angle + math.pi) * speed * 0.5,
                                                                     math.sin(angle + math.pi) * speed * 0.5],
                                                           frame=random.randint(0, 7)))

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)

                if kill:
                    self.particles.remove(particle)

            gf.check_events(self.movement, self.sfx['jump'], self.player)

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255),
                                   (self.display.get_width() // 2, self.display.get_height() // 2),
                                   (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            # Display score
            self.mensaje_score = self.fuente_juego.render('Puntuación: ' + str(self.score), True, (0, 0, 0))
            self.mensaje_score_rect = self.mensaje_score.get_rect(center=(250, 14))
            self.display.blit(self.mensaje_score, self.mensaje_score_rect)

            self.screen.blit(self.display, (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Game().main_menu()
