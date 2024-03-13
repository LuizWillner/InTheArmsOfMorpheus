import pygame


def drawText(janela, text, font_type, font_size, color, coord_x, coord_y):
    font = pygame.font.SysFont(f'{font_type}', font_size)
    txt_img = font.render(text, True, color)
    janela.blit(txt_img, (coord_x, coord_y))
