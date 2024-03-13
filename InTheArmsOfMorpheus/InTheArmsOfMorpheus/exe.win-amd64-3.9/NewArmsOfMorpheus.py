import pygame
import os
import random
import pickle
from pygame import mixer
import draw_text


# Att 17
def game(level):
    pygame.init()
    mixer.init()

    index_transition = 0
    contador_transition = 0
    lista_transition = []

    janela_width = 1300
    janela_height = 700

    janela_game = pygame.display.set_mode((janela_width, janela_height))
    pygame.display.set_caption('NEW - In The Arms Of Morpheus')

    clock = pygame.time.Clock()
    fps = 60

    quant_linhas = 20
    quant_colunas = 200
    tile_size = janela_height // quant_linhas
    tipos_tile = len(os.listdir(f'InTheArmsOfMorpheus/Cenário/Tile List'))
    lvl = level

    if lvl == 0:
        pygame.mixer.music.unload()
        pygame.mixer.music.load('InTheArmsOfMorpheus/arquivos/musicas/egito_musica.wav')
        pygame.mixer.music.play(-1, 0.0, 1000)
        pygame.mixer.music.set_volume(0.1)
        front_img = pygame.image.load('InTheArmsOfMorpheus/Cenário/Background/pyramids_and_ground.png').convert_alpha()
        altura_front = janela_height - front_img.get_height()
        back_img = pygame.image.load('InTheArmsOfMorpheus/Cenário/Background/sky.png').convert_alpha()
        altura_back = 0
        range_draw = 5

    elif lvl == 1 or lvl == 2:
        front_img = pygame.image.load('InTheArmsOfMorpheus/Cenário/Background/pyramids_and_ground.png').convert_alpha()
        altura_front = janela_height - front_img.get_height()
        back_img = pygame.image.load('InTheArmsOfMorpheus/Cenário/Background/sky.png').convert_alpha()
        altura_back = 0
        range_draw = 5

    elif lvl == 3:
        pygame.mixer.music.load('InTheArmsOfMorpheus/arquivos/musicas/medieval_musica.wav')
        pygame.mixer.music.play(-1, 0.0, 1000)
        pygame.mixer.music.set_volume(0.1)
        front_img = pygame.image.load('InTheArmsOfMorpheus/Cenário/Background/cave_front.png').convert_alpha()
        altura_front = 0
        back_img = pygame.image.load('InTheArmsOfMorpheus/Cenário/Background/cave_fundo.png').convert_alpha()
        altura_back = 0
        range_draw = 5

    elif lvl == 4:
        front_img = pygame.image.load('InTheArmsOfMorpheus/Cenário/Background/dark_forest_front.png').convert_alpha()
        altura_front = 0
        back_img = pygame.image.load('InTheArmsOfMorpheus/Cenário/Background/dark_forest_back.png').convert_alpha()
        altura_back = 0
        range_draw = 8

    else:
        pygame.mixer.music.load('InTheArmsOfMorpheus/arquivos/musicas/TheFinalBattle.wav')
        pygame.mixer.music.play(-1, 0.0, 1000)
        pygame.mixer.music.set_volume(0.1)
        front_img = pygame.image.load('InTheArmsOfMorpheus/Cenário/Background/castle_back.png').convert_alpha()
        altura_front = 0
        back_img = pygame.image.load('InTheArmsOfMorpheus/Cenário/Background/castle_front.png').convert_alpha()
        altura_back = 0
        range_draw = 8

    scroll_limite = 300
    janela_scroll = 0
    fundo_scroll = 0

    gravidade = 0.75

    mover_esquerda = False
    mover_direita = False
    fundo_pause = False
    som = True

    cor_fundo = (144, 201, 120)
    linha = (255, 0, 0)

    # Carregar música e sons
    pulo_fx = pygame.mixer.Sound('InTheArmsOfMorpheus/sons/pulo.wav')
    pulo_fx.set_volume(0.7)
    hit_fx = pygame.mixer.Sound('InTheArmsOfMorpheus/sons/espada_hit.wav')
    hit_fx.set_volume(0.1)
    andar_fx = pygame.mixer.Sound('InTheArmsOfMorpheus/sons/andar.wav')
    andar_fx.set_volume(0.03)

    # Carregar imagens
    fundo_preto = pygame.image.load('InTheArmsOfMorpheus/arquivos/fundo/tela_preta.png')
    continue_button = pygame.image.load('InTheArmsOfMorpheus/arquivos/menu/continue.png')
    continue2_button = pygame.image.load('InTheArmsOfMorpheus/arquivos/menu/continue2.png')
    restart_button = pygame.image.load('InTheArmsOfMorpheus/arquivos/menu/restart_button.png')
    restart2_button = pygame.image.load('InTheArmsOfMorpheus/arquivos/menu/restart2_button.png')
    quit_button = pygame.image.load('InTheArmsOfMorpheus/arquivos/menu/quit.png')
    quit2_button = pygame.image.load('InTheArmsOfMorpheus/arquivos/menu/quit2.png')

    # Carregar a lista de tiles
    lista_tiles = []
    for i in range(tipos_tile):
        img = pygame.image.load(f'InTheArmsOfMorpheus/Cenário/Tile List/{i}.png')
        img = pygame.transform.scale(img, (tile_size, tile_size))
        lista_tiles.append(img)

    # Carregar imagens tela de gameover
    for h in range(18):
        morte_transition = pygame.image.load(f'InTheArmsOfMorpheus/arquivos/transition/morte_transition{h}.png')
        lista_transition.append(morte_transition)

    # Desenhar fundo
    def draw_fundo():
        janela_game.fill(cor_fundo)
        width = back_img.get_width()
        for x in range(range_draw):
            ground_height = front_img.get_height()
            janela_game.blit(back_img, ((x * width) - fundo_scroll * 0.3, altura_back))
            janela_game.blit(front_img, ((x * width) - fundo_scroll * 0.8, altura_front))

    # Classe que abrange todos os personagens "vivos" do jogo
    class Personagem(pygame.sprite.Sprite):
        def __init__(self, tipo_personagem, x, y, scale, velocidade, vida,
                     dano):  # recebe posição em x, posição em y e um valor de scale, para aumentar ou diminuir a imagem
            pygame.sprite.Sprite.__init__(self)
            self.contador_passos = 0
            self.vivo = True
            self.damage = dano
            self.tipo_personagem = tipo_personagem
            self.player_bool = True
            self.velocidade = velocidade
            self.vida = vida
            self.direction = 1
            self.pulo = False
            self.ataque1 = False
            self.ataque2 = False
            self.protecao = False
            self.no_ar = True
            self.vel_y = 0
            self.virar = False
            self.contador_jump = 0
            self.contador_dano = 25
            self.dano = False
            self.contador_tempo = 0

            self.mover_contador = 0
            self.idling = False
            self.contador_idling = 0
            self.vision = pygame.Rect(0, 0, 50, 20)

            # Variáveis de config da animação
            self.lista_animacao = []
            self.index = 0
            self.action = 0
            self.update_timer = pygame.time.get_ticks()

            # Montando a lista de animações
            tipos_de_animacao = ['idle', 'correndo', 'pulo', 'ataque', 'morte', 'machucado']
            for animacao in tipos_de_animacao:
                temporaria = []
                numero_de_imagens = len(
                    os.listdir(f'InTheArmsOfMorpheus/arquivos/personagens/{self.tipo_personagem}/{animacao}'))
                for i in range(numero_de_imagens):
                    player_img = pygame.image.load(f'InTheArmsOfMorpheus/arquivos/personagens/{self.tipo_personagem}/{animacao}/{animacao}{i}.png').convert_alpha()
                    player_img = pygame.transform.scale(player_img, (
                        int(player_img.get_width() * 2), int(player_img.get_height() * 2)))
                    temporaria.append(player_img)
                self.lista_animacao.append(temporaria)

            self.player_img = self.lista_animacao[self.action][self.index]
            self.person_rect = self.player_img.get_rect()
            self.person_rect.center = (x, y)
            self.width = self.player_img.get_width()
            self.height = self.player_img.get_height()

        def move(self, mover_esquerda, mover_direita):  # Calcula o movimento a ser executado pelo personagem
            # Variáveis do movimento/variação da posição (DeltaX e DeltaY)
            dx = 0
            dy = 0

            # Variável local do scroll da janela
            janela_move = 0

            # Configurando o movimento para direita e para esquerda
            if mover_direita:
                dx = self.velocidade
                self.virar = False
                self.direction = 1
                if self.tipo_personagem == 'jogador' and not self.no_ar:
                    self.contador_passos += 1
                    if self.contador_passos >= 15:
                        andar_fx.play()
                        self.contador_passos = 0
            elif mover_esquerda:
                dx = -self.velocidade
                self.virar = True
                self.direction = -1
                if self.tipo_personagem == 'jogador' and not self.no_ar:
                    self.contador_passos += 1
                    if self.contador_passos >= 15:
                        andar_fx.play()
                        self.contador_passos = 0

            # Configurando o movimento vertical (pulo)
            if self.pulo and self.contador_jump <= 1:
                self.vel_y = -16
                self.pulo = False
                self.no_ar = True
                self.contador_jump += 1

            # Adicionando gravidade
            self.vel_y += gravidade
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Se o jogador cair na void, morre
            if self.person_rect.y + dy > janela_height:
                pygame.mixer.music.unload()
                self.vivo = False

            # checando colisão
            for tile in mundo.lista_obstaculo:
                # checando colisão eixo x
                if tile[1].colliderect(self.person_rect.x + dx, self.person_rect.y, self.width, self.height):
                    dx = 0
                    # Se for um inimigo, vira a direção
                    if not self.player_bool:
                        self.direction *= -1
                        self.mover_contador = 0

                # checando colisão eixo y
                if tile[1].colliderect(self.person_rect.x, self.person_rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:  # se o jogador estiver pulando
                        self.vel_y = 0
                        dy = tile[1].bottom - self.person_rect.top

                    elif self.vel_y >= 0:  # se o jogador estiver caindo
                        self.vel_y = 0
                        self.no_ar = False
                        self.contador_jump = 0
                        dy = tile[1].top - self.person_rect.bottom

            # Checando se o player tá ultrapassando os limites da fase
            if self.tipo_personagem == 'jogador':
                if self.person_rect.left + dx < 0 or self.person_rect.right + dx > janela_width:
                    dx = 0

            # Atualizando a variação da posição
            self.person_rect.x += dx
            self.person_rect.y += dy

            # Atualizando o scroll de acordo com a posição do player
            if self.tipo_personagem == 'jogador':
                if (
                        self.person_rect.right > janela_width - scroll_limite and fundo_scroll < mundo.tamanho_fase * tile_size - janela_width) or (
                        self.person_rect.left < scroll_limite and fundo_scroll > 0):
                    self.person_rect.x -= dx
                    janela_move = -dx

            return janela_move

        def update_animacao(self):  # Atualizando a animação do personagem de acordo com a ação que está sendo executada
            cooldown_animacao = 150  # define o quão rápido a animação ocorre
            if fundo_pause == False:
                if self.action == 3:
                    cooldown_animacao = 80
                    if self.tipo_personagem == 'jogador':
                        self.person_rect.y -= 0
                        cooldown_animacao = 40

                elif self.no_ar:
                    cooldown_animacao = 120

                self.player_img = self.lista_animacao[self.action][self.index]

                if pygame.time.get_ticks() - self.update_timer > cooldown_animacao:
                    self.update_timer = pygame.time.get_ticks()
                    if self.vivo:
                        self.index += 1
                    else:
                        if self.index < len(self.lista_animacao[self.action]) - 1:
                            self.index += 1
                if self.index >= len(self.lista_animacao[self.action]):
                    if self.vivo:
                        self.index = 0
                        self.ataque1 = False
                        self.ataque2 = False

        def ai(self):
            if self.person_rect.x >= 0 and self.person_rect.x <= 1300:
                if self.vivo and jogador.vivo and fundo_pause == False:
                    if random.randint(1, 200) == 1 and not self.idling:
                        self.update_acao(0)
                        self.idling = True
                        self.contador_idling = 50
                    if self.vision.colliderect(jogador.person_rect):
                        self.contador_dano += 1
                        self.update_acao(3)

                        if self.person_rect.colliderect(jogador.person_rect) and self.index == len(
                                self.lista_animacao[3]) - 1 and self.contador_dano >= 35 and jogador.protecao == False:
                            jogador.vida -= self.damage
                            hit_fx.play()
                            self.contador_dano = 0
                            if jogador.vida <= 0:
                                pygame.mixer.music.unload()
                                pygame.mixer.music.load('InTheArmsOfMorpheus/arquivos/musicas/Game_Over.wav')
                                pygame.mixer.music.play(1, 0.0, 5000)
                                jogador.vivo = False

                        if jogador.person_rect.colliderect(self.person_rect) and jogador.index == len(
                                jogador.lista_animacao[3]) - 1 and jogador.protecao:
                            self.vida -= jogador.damage
                            hit_fx.play()
                            jogador.protecao = False
                            if self.vida <= 0:
                                self.vivo = False
                                mundo.quant_inimigos -= 1

                    else:
                        if not self.idling:
                            if self.direction == 1:
                                ai_mover_direita = True

                            else:
                                ai_mover_direita = False
                            ai_mover_esquerda = not ai_mover_direita
                            self.move(ai_mover_esquerda, ai_mover_direita)
                            self.update_acao(1)
                            self.mover_contador += 1
                            if self.tipo_personagem != 'dark_warrior':
                                self.vision.center = (self.person_rect.centerx + 40 * self.direction, self.person_rect.centery - 5)
                            else:
                                self.vision.center = (self.person_rect.centerx + 40 * self.direction, self.person_rect.centery - 40)
                            # pygame.draw.rect(janela_game, linha, self.vision)
                            if self.mover_contador > 30:
                                self.direction *= -1
                                self.mover_contador *= -1

                        else:
                            self.contador_idling -= 1
                            if self.contador_idling <= 0:
                                self.idling = False

            # Scroll dos inimigos
            self.person_rect.x += janela_scroll

        def update_acao(self, new_action):  # atualizando a ação a ser executada de acordo com o comando
            if new_action != self.action:
                self.action = new_action
                self.index = 0
                self.update_timer = pygame.time.get_ticks()

        def draw(self):
            janela_game.blit(pygame.transform.flip(self.player_img, self.virar, False), self.person_rect)

        def draw_inimigo(self):
            if self.person_rect.x >= 0 and self.person_rect.x <= 1300:
                janela_game.blit(pygame.transform.flip(self.player_img, self.virar, False), self.person_rect)

    class BarraDeVida:
        def __init__(self, x, y, vida, vida_maxima):
            self.x = x
            self.y = y
            self.vida = vida
            self.vida_maxima = vida_maxima
            self.cabeca = pygame.image.load('InTheArmsOfMorpheus/arquivos/head.png')
            self.cabeca = pygame.transform.scale(self.cabeca,
                                                 (int(self.cabeca.get_width() * 2), int(self.cabeca.get_height() * 2)))

        def draw(self, vida):
            self.vida = vida
            razao = self.vida / self.vida_maxima
            pygame.draw.rect(janela_game, (0, 0, 0), (self.x - 2, self.y - 2, 200, 30))
            pygame.draw.rect(janela_game, (0, 0, 0), (self.x + 2, self.y + 2, 200, 30))
            pygame.draw.rect(janela_game, (255, 0, 0), (self.x, self.y, 200, 30))
            pygame.draw.rect(janela_game, (0, 255, 0), (self.x, self.y, 200 * razao, 30))
            janela_game.blit(self.cabeca, (10, 10))

    class Mundo:
        def __init__(self):
            self.lista_obstaculo = []
            self.tamanho_fase = 0
            self.quant_inimigos = 0

        def processar_dados(self, data):
            self.tamanho_fase = len(data[0])

            # Iterando sobre a matriz de dados da fase
            for index_r, row in enumerate(data):
                for index_c, tile in enumerate(row):
                    if tile != -1:
                        # Definindo as coordenadasGrid do tile a ser analisado
                        coord_tile_x = index_c * tile_size
                        coord_tile_y = index_r * tile_size

                        # Definindo a imagem e o retângulo do tile a ser analisado
                        img = lista_tiles[tile]
                        img_rect = img.get_rect()
                        img_rect.x = coord_tile_x
                        img_rect.y = coord_tile_y
                        tile_info = (img, img_rect)

                        # Analisando o tile e o classificando numa das categorias
                        if 0 <= tile <= 24:  # Tiles de colisão
                            self.lista_obstaculo.append(tile_info)
                        elif 25 <= tile <= 40:  # Tiles decorativos
                            decoracao = Decoracao(img, img_rect, coord_tile_x, coord_tile_y)
                            decoracao_grupo.add(decoracao)
                        elif 41 <= tile <= 45:  # Armadilhas (lava, água, espinho)
                            armadilha = Armadilha(img, img_rect, coord_tile_x, coord_tile_y)
                            armadilha_grupo.add(armadilha)
                        elif 46 <= tile <= 56:  # Inimigos
                            if tile == 46:
                                pass  # correndo muito rápido; morre no ar
                                skeleton = Personagem('skeleton', coord_tile_x, coord_tile_y, 3, 7, 25, 10)
                                inimigo_grupo.add(skeleton)
                                self.quant_inimigos += 1
                                skeleton.player_bool = False
                            elif tile == 47:
                                pass
                                '''golem = Personagem('golem', coord_tile_x, coord_tile_y, 3, 5, 200)
                                inimigo_grupo.add(golem)'''
                            elif tile == 48:
                                pass  # Inverter imagens
                                farao = Personagem('farao', coord_tile_x, coord_tile_y, 3, 3, 50, 25)
                                inimigo_grupo.add(farao)
                                self.quant_inimigos += 1
                                farao.player_bool = False
                            elif tile == 49:
                                bandido = Personagem('bandido', coord_tile_x, coord_tile_y, 3, 3, 50, 25)
                                inimigo_grupo.add(bandido)
                                self.quant_inimigos += 1
                                bandido.player_bool = False
                            elif tile == 50:
                                pass  # inverter imagem; andando no ar; batendo afundado; morre no ar
                                heavy_bandido = Personagem('heavy bandido', coord_tile_x, coord_tile_y, 3, 2, 80, 15)
                                inimigo_grupo.add(heavy_bandido)
                                self.quant_inimigos += 1
                                heavy_bandido.player_bool = False
                            elif tile == 51:
                                pass  # inverter imagem; não consegue acertar o hit direito; morre no ar
                                mumia = Personagem('mumia', coord_tile_x, coord_tile_y, 3, 3, 50, 25)
                                inimigo_grupo.add(mumia)
                                self.quant_inimigos += 1
                                mumia.player_bool = False
                            elif tile == 52:
                                pass  # não consegue acertar o hit direito; morre ajoelhado no ar
                                knight1 = Personagem('knight1', coord_tile_x, coord_tile_y, 3, 3, 70, 18)
                                inimigo_grupo.add(knight1)
                                self.quant_inimigos += 1
                                knight1.player_bool = False
                            elif tile == 53:
                                pass
                                dark_warrior = Personagem('dark_warrior', coord_tile_x, coord_tile_y, 4, 2, 250, 69)
                                inimigo_grupo.add(dark_warrior)
                                self.quant_inimigos += 1
                                dark_warrior.player_bool = False
                            elif tile == 54:
                                pass
                                knight2 = Personagem('knight2', coord_tile_x, coord_tile_y, 3, 4, 50, 20)
                                inimigo_grupo.add(knight2)
                                self.quant_inimigos += 1
                                knight2.player_bool = False
                            elif tile == 55:
                                pass
                                viking = Personagem('viking', coord_tile_x, coord_tile_y, 3, 4, 70, 15)
                                inimigo_grupo.add(viking)
                                self.quant_inimigos += 1
                                viking.player_bool = False
                            elif tile == 56:
                                pass
                                '''demon = Personagem('demon', coord_tile_x, coord_tile_y, 3, 2, 200)
                                inimigo_grupo.add(demon)'''

                        elif tile == 57:  # Player
                            jogador = Personagem('jogador', coord_tile_x, coord_tile_y, 3, 5, 200, 25)
                            jogador.player_bool = True
                            barra_de_vida_player = BarraDeVida(33, 10, jogador.vida, jogador.vida)

                        elif tile == 58:  # Heal (recuperar vida)
                            heal = Heal(img, img_rect, coord_tile_x, coord_tile_y)
                            heal_grupo.add(heal)

                        elif tile == 59:  # Chegada (fim da fase)
                            chegada = Chegada(img, img_rect, coord_tile_x, coord_tile_y)
                            chegada_grupo.add(chegada)

            return jogador, barra_de_vida_player

        def draw(self):
            for tile in self.lista_obstaculo:
                tile[1].x += janela_scroll
                if -35 < tile[1].x <= 1335:  # Desenha só os tiles que têm que aparecer na tela
                    janela_game.blit(tile[0], tile[1])

    class Decoracao(pygame.sprite.Sprite):
        def __init__(self, img, rect, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = rect
            self.rect.x = x
            self.rect.y = y

        def update(self):
            self.rect.x += janela_scroll

    class Armadilha(pygame.sprite.Sprite):
        def __init__(self, img, rect, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = rect
            self.rect.x = x
            self.rect.y = y

        def update(self):
            self.rect.x += janela_scroll
            if self.rect.colliderect(jogador.person_rect):
                jogador.vivo = False
                pygame.mixer.music.unload()

    class Chegada(pygame.sprite.Sprite):
        def __init__(self, img, rect, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = rect
            self.rect.x = x
            self.rect.y = y

        def update(self):
            self.rect.x += janela_scroll

    class Heal(pygame.sprite.Sprite):
        def __init__(self, img, rect, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = rect
            self.rect.x = x
            self.rect.y = y

        def update(self):
            self.rect.x += janela_scroll

    inimigo_grupo = pygame.sprite.Group()
    decoracao_grupo = pygame.sprite.Group()
    armadilha_grupo = pygame.sprite.Group()
    heal_grupo = pygame.sprite.Group()
    chegada_grupo = pygame.sprite.Group()

    # Criando lista do mundo vazia (-1)
    mundo_data = []
    for q_ in range(quant_linhas + 1):
        row = [-1] * quant_colunas
        mundo_data.append(row)

    # Carregando o mundo correspondente ao level
    pickle_in = open(f'InTheArmsOfMorpheus/level data/level{lvl}_data', 'rb')
    mundo_data = pickle.load(pickle_in)
    'print(mundo_data)'

    mundo = Mundo()
    jogador, barra_de_vida_player = mundo.processar_dados(mundo_data)

    on = True
    while on:

        clock.tick(fps)
        '''print("clock.tick:", clock.tick())
        print("clock.get_fps", clock.get_fps())'''

        # Atualizar o fundo
        draw_fundo()

        # Desenhar os tiles de caráter "obstáculo"
        mundo.draw()

        barra_de_vida_player.draw(jogador.vida)

        decoracao_grupo.update()
        decoracao_grupo.draw(janela_game)
        armadilha_grupo.update()
        armadilha_grupo.draw(janela_game)
        heal_grupo.update()
        heal_grupo.draw(janela_game)
        chegada_grupo.update()
        chegada_grupo.draw(janela_game)

        if not jogador.vivo:
            janela_game.blit(lista_transition[index_transition], lista_transition[index_transition].get_rect())
            jogador.update_acao(4)
            if index_transition < 14:
                index_transition += 1
            if index_transition >= 14:
                contador_transition += 1
                if contador_transition == 25:
                    index_transition += 1
                    contador_transition = 0
            if index_transition > 16:
                index_transition = 17

            # update Ações do Personagem
        elif jogador.vivo and fundo_pause == False:
            if jogador.ataque2 and jogador.ataque1:
                jogador.update_acao(3)  # 3: atacando

            elif jogador.no_ar:
                jogador.update_acao(2)  # 2: pulando

            elif mover_direita or mover_esquerda:
                jogador.update_acao(1)  # 1: correndo

            else:
                if not jogador.ataque2 and not jogador.dano:
                    jogador.update_acao(0)  # 0: idle

            inimigo_grupo.update()
            if jogador.vivo == True:
                for inimigo in inimigo_grupo:
                    inimigo.ai()
                    inimigo.update_animacao()
                    inimigo.draw_inimigo()
                    if not inimigo.vivo:
                        inimigo.update_acao(4)

            janela_scroll = jogador.move(mover_esquerda, mover_direita)
            fundo_scroll -= janela_scroll

            draw_text.drawText(janela_game, f'Inimigos restantes: {mundo.quant_inimigos}', 'Times New Roman', 20,(120, 0, 0), 10, janela_height // 16)

        for chegada in chegada_grupo:
            if chegada.rect.colliderect(jogador.person_rect) and mundo.quant_inimigos == 0:
                on = False
                return lvl + 1

        jogador.update_animacao()
        jogador.draw()

        '''print('Inimigos restantes', mundo.quant_inimigos)'''

        if fundo_pause == True:

            janela_game.blit(fundo_preto, (0, 0))
            janela_game.blit(continue_button, (550, 250))
            janela_game.blit(restart_button, (550, 350))
            janela_game.blit(quit_button, (550, 450))
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 250 <= mouse_y <= 320 and 550 <= mouse_x <= 750:
                janela_game.blit(continue2_button, (550, 250))

            if 350 <= mouse_y <= 420 and 550 <= mouse_x <= 750:
                janela_game.blit(restart2_button, (550, 350))

            if 450 <= mouse_y <= 520 and 550 <= mouse_x <= 750:
                janela_game.blit(quit2_button, (550, 450))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 250 <= mouse_y <= 320 and 550 <= mouse_x <= 750:
                        fundo_pause = False

                    if 350 <= mouse_y <= 420 and 550 <= mouse_x <= 750:
                        return lvl

                    if 450 <= mouse_y <= 520 and 550 <= mouse_x <= 750:
                        return -2

        # Manejando os eventos do pygame
        for event in pygame.event.get():

            # Fechar Jogo
            if event.type == pygame.QUIT:
                on = False
                return -2

            # Teclado pressionado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    mover_esquerda = True

                if event.key == pygame.K_SPACE and jogador.vivo:
                    jogador.ataque1 = True

                if event.key == pygame.K_d:
                    mover_direita = True

                if event.key == pygame.K_w and jogador.vivo:
                    if not jogador.no_ar and jogador.contador_jump <= 1:
                        pulo_fx.play()
                        jogador.pulo = True

                if event.key == pygame.K_ESCAPE:
                    fundo_pause = True

            # Teclado solto
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mover_esquerda = False

                if event.key == pygame.K_d:
                    mover_direita = False

                if jogador.ataque1:
                    if event.key == pygame.K_SPACE:
                        jogador.ataque2 = True
                        jogador.protecao = True

        pygame.display.update()
