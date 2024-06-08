import pygame

blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)


class Menu:
    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()
        self.font_menu = pygame.font.Font('Data/main_menu/adobemingstd-light.otf', 50)
        self.back_menu = pygame.image.load('Data/main_menu/menu.png').convert_alpha()
        self.back_instructions = pygame.image.load('Data/main_menu/instrucciones.jpg').convert_alpha()
        self.back_records = pygame.image.load('Data/main_menu/record.png').convert_alpha()

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
        return self.button(218, 223, 227, 46)

    def inst_but(self):
        return self.button(218, 297, 227, 46)

    def record_but(self):
        return self.button(214, 372, 227, 46)

    def quit_but(self):
        return self.button(276, 442, 98, 20)








