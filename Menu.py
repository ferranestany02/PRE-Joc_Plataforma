import pygame

blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)


class Menu:
    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()
        self.font_menu = pygame.font.Font('data/adobemingstd-light.otf', 50)
        self.back_menu = pygame.image.load('data/images/menu/menu.jpeg').convert_alpha()
        self.back_instructions = pygame.image.load('data/images/menu/instruciones.jpg').convert_alpha()

    def draw_text(self, text, color, surface, x, y, size):
        font_letra = pygame.font.SysFont(None, size)
        txt_obj = font_letra.render(text, 1, color)
        txt_rec = txt_obj.get_rect()
        txt_rec.topleft = (x, y)
        surface.blit(txt_obj, txt_rec)

    def button(self, x, y, width, height):
        return pygame.Rect(x, y, width, height)

    def draw_button(self, surface, rec):
        pygame.draw.rect(surface, (0, 0, 0), rec)

    def jugar_but(self):
        return self.button(170, 260, 300, 40)

    def inst_but(self):
        return self.button(170, 352, 302, 38)

    def quit_but(self):
        return self.button(250, 426, 120, 28)

    def main_menu(self, surface):

        surface.blit(self.back_menu, (0, 0))

        self.draw_button(surface, self.jugar_but())
        self.draw_text('Jugar', blue, surface, 240, 248, 80)

        self.draw_button(surface, self.inst_but())
        self.draw_text('¿Como jugar?', blue, surface, 160, 348, 60)

        self.draw_button(surface,  self.quit_but())
        self.draw_text('Quit', blue, surface, 250, 426, 50)








