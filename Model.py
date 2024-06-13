import pygame
from scripts.coins import Coins
from scripts.entidades import Enemigos
import random

import json
import math
from scripts.chispa import Spark
from scripts.particle import Particle
from scripts.mapa import Mapa
from scripts.entidades import Jugador
from scripts.utils import carga_mapa, carga_musica


class Model:
    def __init__(self):
        self.game_active = False
        self.menu = True
        self.menu_instr = False
        self.menu_records = False
        self.movement = [False, False]

        self.score = 0
        self.assets = carga_mapa()
        self.sfx = carga_musica()

        self.player = Jugador(self, (50, 50), (16, 41))
        self.tilemap = Mapa(self, tile_size=32)

        self.level = 0
        self.load_level(self.level)

        self.start_time = 0
        self.end_time = 0

        self.records = {
            'max_score_0': 0,
            'max_score_1': 0,
            'max_score_2': 0
        }

    def a_score(self):
        try:
            with open('records.txt', 'r') as score_file:
                self.records = json.load(score_file)
        except:
            pass

    def max_score_create_file(self):
        with open('records.txt', 'w') as score_file:
            json.dump(self.records, score_file)

    def load_level(self, map_id):

        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemigos(self, spawner['pos'], (16, 28)))

        self.coins = []
        for c in self.tilemap.extract([('coin', 0)], keep=False):
            self.coins.append(Coins(self, c['pos'], (32, 32)))

        self.projectiles = []
        self.particles = []
        self.sparks = []
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

    def coins_collect(self, musica, screen):
        for c in self.coins:
            if self.player.rect().colliderect(c.rect):
                self.score += 1
                if self.records['max_score_' + str(self.level)] < self.score:
                    self.records['max_score_' + str(self.level)] = self.score
                self.coins.remove(c)
                musica.play(0)

        for c in self.coins.copy():
            collect = c.update(self.tilemap, (0, 0))
            c.render(screen, offset=self.scroll)
            if collect:
                self.coins.remove(c)

    def terminar_partida(self):
        if not len(self.enemies):
            self.transition += 1
            self.end_time = int(pygame.time.get_ticks() / 1000)
            if self.transition > 30:
                self.level = self.level + 1
                self.load_level(self.level)

    def set_transition(self):
        if self.transition < 0:
            self.transition += 1

    def reset(self):
        if self.dead:
            self.score = 0
            self.dead += 1
            if self.dead >= 10:
                self.transition = min(30, self.transition + 1)
            if self.dead > 40:
                self.load_level(self.level)

    def move_camera(self, surface):
        self.scroll[0] += (self.player.rect().centerx - surface.get_width() / 2 - self.scroll[0]) / 200
        self.scroll[1] += (self.player.rect().centery - surface.get_height() / 2 - self.scroll[1]) / 200
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
        return render_scroll

    def renderiza_map(self, surface):
        scroll = self.move_camera(surface)
        self.tilemap.render(surface, offset=scroll)

    def def_enemies(self, surface):
        scroll = self.move_camera(surface)

        for enemy in self.enemies.copy():
            kill = enemy.update(self.tilemap, (0, 0))
            enemy.render(surface, offset=scroll)
            if kill:
                self.enemies.remove(enemy)

    def player_render(self, surface):
        scroll = self.move_camera(surface)
        if not self.dead:
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(surface, offset=scroll)

    def enemies_attack(self, surface):

        scroll = self.move_camera(surface)

        for projectile in self.projectiles.copy():
            projectile[0][0] += projectile[1]
            projectile[2] += 1

            img = self.assets['arrow_2']

            for a in self.enemies.copy():
                if self.player.rect().centerx < a.rect().centerx:
                    img = self.assets['arrow_1']

            surface.blit(img, (projectile[0][0] - img.get_width() / 2 - scroll[0],
                               projectile[0][1] - img.get_height() / 2 - scroll[1]))

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
                    for i in range(30):
                        angle = random.random() * math.pi * 2
                        speed = random.random() * 5
                        self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                        self.particles.append(Particle(self, 'particle', self.player.rect().center,
                                                       velocity=[math.cos(angle + math.pi) * speed * 0.5,
                                                                 math.sin(angle + math.pi) * speed * 0.5],
                                                       frame=random.randint(0, 7)))

    def remove_sparks(self, surface):
        scroll = self.move_camera(surface)
        for spark in self.sparks.copy():
            kill = spark.update()
            spark.render(surface, scroll)
            if kill:
                self.sparks.remove(spark)

    def remove_particle(self, surface):
        scroll = self.move_camera(surface)
        for particle in self.particles.copy():
            kill = particle.update()
            particle.render(surface, offset=scroll)

            if kill:
                self.particles.remove(particle)

    def trans(self, surface):
        if self.transition:
            transition_surf = pygame.Surface(surface.get_size())
            pygame.draw.circle(transition_surf, (255, 255, 255),
                               (surface.get_width() // 2, surface.get_height() // 2),
                               (30 - abs(self.transition)) * 8)
            transition_surf.set_colorkey((255, 255, 255))
            surface.blit(transition_surf, (0, 0))

    def update_score(self, fuente):
        mensaje_score = fuente.render('Puntuación: ' + str(self.score), True, (0, 0, 0))
        mensaje_score_rect = mensaje_score.get_rect(center=(570, 20))
        return mensaje_score, mensaje_score_rect

    def update_time(self):
        time = int(pygame.time.get_ticks() / 1000) - self.start_time - self.end_time
        return time
