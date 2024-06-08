import pygame
from scripts.menu import Menu
from scripts.utils import carga_musica
from Presenter import Presenter
import json


class View:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Rise of the satyr')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((640, 480), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.musica = carga_musica()
        self.presenter = Presenter(self)
        self.game_font = pygame.font.SysFont("Arial", 20)
        self.game_font_2 = pygame.font.SysFont("Arial", 26)
        self.final = pygame.image.load('Data/images/fin.png').convert_alpha()

    def display_max_score(self, level, pos, font):
        list = [6, 20, 28]
        with open('records.txt', 'r') as score_file:
            a = json.load(score_file)

        nivel_x = font.render(str(a['max_score_' + str(level)]) + '/' + str(list[level]), True, (0, 0, 170))
        nivel_x_rect = nivel_x.get_rect(center=pos)

        self.screen.blit(nivel_x, nivel_x_rect)

    def display_score(self):
        score = self.presenter.model.update_score(self.game_font)
        self.display.blit(score[0], score[1])

    def display_level(self):
        nivel_mensaje = self.game_font.render('Nivel: ' + str(self.presenter.model.level + 1), True, (0, 0, 0))
        nivel_mensaje_rect = nivel_mensaje.get_rect(center=(50, 20))
        self.display.blit(nivel_mensaje, nivel_mensaje_rect)

    def display_time(self):
        time = self.presenter.model.update_time()
        time_mensaje = self.game_font.render('Tiempo: ' + str(time) + 's', True, (0, 0, 0))
        time_mensaje_rect = time_mensaje.get_rect(center=(320, 20))
        self.display.blit(time_mensaje, time_mensaje_rect)

    def main_menu(self):

        self.musica['menu'].play(-1)

        while self.presenter.model.menu:

            self.menu.draw_button(self.screen, self.menu.jugar_but())
            self.menu.draw_button(self.screen, self.menu.inst_but())
            self.menu.draw_button(self.screen, self.menu.quit_but())
            self.menu.draw_button(self.screen, self.menu.record_but())

            self.screen.blit(self.menu.back_menu, (0, 0))

            self.presenter.handle_events()

            pygame.display.update()
            self.clock.tick(60)

    def instructions(self):

        while self.presenter.model.menu_instr:

            self.screen.blit(self.menu.back_instructions, (0, 0))

            self.presenter.handle_events()

            pygame.display.update()
            self.clock.tick(60)

    def records(self):

        while self.presenter.model.menu_records:

            self.screen.blit(self.menu.back_records, (0, 0))
            self.display_max_score(0, (350, 192), self.game_font_2)
            self.display_max_score(1, (358, 258), self.game_font_2)
            self.display_max_score(2, (358, 324), self.game_font_2)
            self.presenter.handle_events()
            pygame.display.update()
            self.clock.tick(60)

    def game(self):
        self.musica['menu'].stop()
        self.musica['music'].play(-1)
        self.musica['ambience'].play(-1)
        self.presenter.model.a_score()

        while True:
            self.display.fill((0, 0, 0, 0))
            self.display.blit(self.presenter.model.assets['background'], (0, 0))
            self.presenter.update_game(self.display, self.musica['coin'])

            self.presenter.handle_events()
            self.display_score()

            self.display_level()
            self.display_time()
            self.screen.blit(self.display, (0, 0))

            if self.presenter.model.level == 3:
                self.screen.blit(self.final, (0, 0))

            pygame.display.update()
            self.clock.tick(70)


if __name__ == "__main__":
    View().main_menu()
