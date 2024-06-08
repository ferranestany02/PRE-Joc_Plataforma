import pygame
from Model import Model
import sys


class Presenter:
    def __init__(self, view):
        self.view = view
        self.model = Model()

    def update_game(self, surface, musica):
        self.model.coins_collect(musica, surface)
        self.model.terminar_partida()
        self.model.set_transition()
        self.model.reset()
        self.model.renderiza_map(surface)
        self.model.def_enemies(surface)
        self.model.player_render(surface)
        self.model.enemies_attack(surface)
        self.model.remove_sparks(surface)
        self.model.remove_particle(surface)
        self.model.trans(surface)

    def handle_events(self):
        for event in pygame.event.get():
            if self.model.game_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.model.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.model.movement[1] = True
                    if event.key == pygame.K_UP:
                        if self.model.player.jump():
                            self.view.musica['jump'].play()
                    if event.key == pygame.K_x:
                        self.model.player.dash()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.model.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.model.movement[1] = False

            if self.model.menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.view.menu.jugar_but().collidepoint(pygame.mouse.get_pos()):
                            self.model.game_active = True
                            self.model.menu = False
                            self.model.start_time = int(pygame.time.get_ticks() / 1000)
                            self.view.game()
                        elif self.view.menu.inst_but().collidepoint(pygame.mouse.get_pos()):
                            self.model.menu = False
                            self.model.menu_instr = True
                            self.view.instructions()
                        elif self.view.menu.record_but().collidepoint(pygame.mouse.get_pos()):
                            self.model.menu = False
                            self.model.menu_records = True
                            self.view.records()
                        elif self.view.menu.quit_but().collidepoint(pygame.mouse.get_pos()):
                            pygame.quit()
                            exit()

            if self.model.menu_instr:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.model.menu_instr = False
                        self.model.menu = True

            if self.model.menu_records:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.model.menu_records = False
                        self.model.menu = True

            self.salir(event)

    def salir(self, event):
        if event.type == pygame.QUIT:
            if self.model.game_active:
                self.model.max_score_create_file()
            pygame.quit()
            sys.exit()



