import pygame
# import csv
import pickle
from PPlay.window import *
from InTheArmsOfMorpheus import button_mod
from InTheArmsOfMorpheus import draw_text
import os

# att 3

pygame.init()

# Janela e suas dimensões  (1200 x 700)
visual_height = 700
visual_width = 1300
# margin_height = 50
margin_width = 200
janela_width = visual_width + margin_width
janela_height = visual_height  # + margin_height

# Janela vars
janela = pygame.display.set_mode((janela_width, janela_height))
pygame.display.set_caption('Level Editor')
fps = 60
clock = pygame.time.Clock()

# Vars do jogo
# Vars Scroll da tela
move_right = False
move_left = False
move = 0
move_vertical = 0
move_spd = 1

# Vars dos tiles
num_rows = 20
max_col = 200
tile_size = visual_height // num_rows

num_tile_types = len(os.listdir('Cenário/Tile List'))

tile_atual = 0

# Vars do sistema de save
lvl = 0

# Carregando Imagens
sky_img = pygame.image.load('Cenário/Background/sky.png').convert_alpha()
sun_img = pygame.image.load('Cenário/Background/sun.png').convert_alpha()
pyramids_img = pygame.image.load('Cenário/Background/pyramids.png').convert_alpha()
pyramid_img = pygame.image.load('Cenário/Background/pyramid.png').convert_alpha()
ground_img = pygame.image.load('Cenário/Background/pyramids_and_ground.png').convert_alpha()

save_img = pygame.image.load('Botoes/save_btn.png').convert_alpha()
load_img = pygame.image.load('Botoes/load_btn.png').convert_alpha()
up_img = pygame.image.load('Botoes/arrow_up_btn.png').convert_alpha()
down_img = pygame.image.load('Botoes/arrow_down_btn.png').convert_alpha()

all_tile_imgs = []
for p in range(num_tile_types):  # carregando imagens dos tiles e appendendo na lista para mostrar deps no seletor
    img = pygame.image.load(f'Cenário/Tile List/{p}.png')
    img = pygame.transform.scale(img, (tile_size, tile_size))
    all_tile_imgs.append(img)

# Definindo Cores
green = (144, 201, 120)
red = (200, 25, 25)
white = (255, 255, 255)
black = (0, 0, 0)
brown = (102, 51, 0)

# Criando fase
mundo_data = []
mundo_data_inicial = []
for q_ in range(num_rows + 1):
    row = [-1] * max_col
    print(f'Colunas = {len(row)}')
    mundo_data.append(row)
    mundo_data_inicial.append(row.copy())

print(f'Linhas = {len(mundo_data)}')


# Desenhar plano de fundo
def drawBackground():
    width = sky_img.get_width()
    janela.fill(white)
    for i in range(5):
        janela.blit(sky_img, ((i * width) - move * 0.5, 0))
        # janela.blit(sun_img, (visual_width, 0))
        janela.blit(ground_img, ((i * width) - move * 0.8, janela_height - ground_img.get_height()))
        # janela.blit(pyramids_img, ((i * width) - move * 0.6, janela_height - pyramid_img.get_height() - 75))
        # janela.blit(pyramid_img, ((i * width) - move * 0.6, janela_height - pyramid_img.get_height() - 75))


# Desenhar o grid
def drawGrid():
    for i in range(max_col + 1):
        pygame.draw.line(janela, black, (i * tile_size - move, 0), (i * tile_size - move, visual_height))
    for i in range(num_rows + 1):
        pygame.draw.line(janela, black, (0, i * tile_size), (visual_width, i * tile_size))


# Desenha os tiles do mundo
def draw_world_tiles():
    i = 0
    for mundo_data_row in mundo_data:
        j = 0
        for tile in mundo_data_row:
            if tile > -1:
                janela.blit(all_tile_imgs[tile], (j*tile_size - move, i*tile_size))  # a fase só mexe na horizontal
            j += 1

        i += 1


# Criando os botões
save_button = button_mod.Button(janela_width/1.07, visual_height//1.1, save_img, 1)
load_button = button_mod.Button(janela_width/1.15, visual_height//1.1, load_img, 1)
# arrow_up_button = button_mod.Button(janela_width)
all_buttons = []
button_num_rows = 0
button_num_col = 0

for p in range(num_tile_types):
    tile_button = button_mod.Button(visual_width + (75 * button_num_col) + 10, 75 * button_num_rows + 10, all_tile_imgs[p], 1)
    all_buttons.append(tile_button)
    button_num_col += 1
    if button_num_col == 3:
        button_num_rows += 1
        button_num_col = 0

# Game Loop
on = True
while on:
    clock.tick(fps)

    drawBackground()
    drawGrid()
    draw_world_tiles()

    # Desenhar texto das informações das fases
    draw_text.drawText(janela=janela, text=f'Level {lvl}', font_type='Futura', font_size=30, color=red, coord_x=5, coord_y=5)
    draw_text.drawText(janela=janela, text=f'UP e DOWN para mudar nível', font_type='Futura', font_size=20, color=red, coord_x=5, coord_y=25)

    # Desenhar Seletor de Tiles
    pygame.draw.rect(janela, brown, (visual_width, 0, margin_width, visual_height))
    # pygame.draw.rect(janela, brown, (0, visual_height - 10, janela_width, margin_height + 10))

    # Escolher um tile
    contador = 0
    for button in all_buttons:
        button.rect.y += move_vertical
        if button.draw(janela):
            tile_atual = contador
        contador += 1

    # Desenhar Área Botões
    pygame.draw.rect(janela, green, (visual_width, visual_height/1.15, margin_width, 100))

    # Destacar Tile Selecionado
    pygame.draw.rect(janela, red, all_buttons[tile_atual].rect, 3)

    # Configurações de salvar e carregar o mundo
    if save_button.draw(janela):  # salvar mundo
        pickle_out = open(f'InTheArmsOfMorpheus/level data/level{lvl}_data', 'wb')
        pickle.dump(mundo_data, pickle_out)
        pickle_out.close()
        # with open(f'level{lvl}_data.csv', 'w', newline='') as csvfile:
        '''    writer_mundo = csv.writer(csvfile, dialect='excel', delimiter=',')
            for row in mundo_data:
                writer_mundo.writerow(row)'''

    if load_button.draw(janela):  # carregar mundo
        move = 0  # resetando move para o início da fase
        mundo_data = []
        pickle_in = open(f'InTheArmsOfMorpheus/level data/level{lvl}_data', 'rb')
        mundo_data = pickle.load(pickle_in)
        # with open(f'level{lvl}_data.csv', 'r', newline='') as csvfile:
        '''    reader_mundo = csv.reader(csvfile, dialect='excel', delimiter=',')
            for index_row, row in enumerate(mundo_data):
                for index_tile, tile in enumerate(row):
                    mundo_data[index_row][index_tile] = int(tile)'''


    # Editando os tiles na tela
    pos = pygame.mouse.get_pos()
    x = (pos[0] + move)//tile_size  # temos que compensar o fato da tela estar movendo
    y = pos[1]//tile_size
    if pos[0] < visual_width:
        if pygame.mouse.get_pressed(3)[0] == 1:  # if pygame.mouse.get_pressed(3)[0] == 1: if teste != -1:  # if pygame.key.get_pressed()[pygame.K_SPACE] == 1:
            if mundo_data[y][x] != tile_atual:
                mundo_data[y][x] = tile_atual
        if pygame.mouse.get_pressed(3)[2] == 1:
            if mundo_data[y][x] != -1:
                mundo_data[y][x] = -1
    # print(mundo_data)

    for event in pygame.event.get():
        # Checando "X" de fechar programa
        if event.type == pygame.QUIT:
            on = False

        # Mover a fase
        if move_left and move > 0:
            move -= 5 * move_spd
        if move_right and move < max_col * tile_size - visual_width:
            move += 5 * move_spd

        # Checando Botões do Teclado pressionados
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                lvl += 1
            if event.key == pygame.K_DOWN and lvl > 0:
                lvl -= 1
            if event.key == pygame.K_RSHIFT:
                for index, linha in enumerate(mundo_data_inicial):
                    mundo_data[index] = linha.copy()

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_LSHIFT:
                move_spd = 5

        # Checando Botões do Teclado NÃO presisoandos
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_LSHIFT:
                move_spd = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                move_vertical -= 5
            elif event.button == 5:
                move_vertical += 5

        '''elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4 or event.button == 5:
                move_vertical = 0'''

    pygame.display.update()

pygame.quit()
