from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from pygame import sprite
from pygame.locals import *
from pygame import mixer

def menu():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()  # música

    pygame.mixer.music.load('InTheArmsOfMorpheus/arquivos/musicas/menu.mp3')
    pygame.mixer.music.play(-1, 0.0, 30000)

    # Game Objects
    janela = Window(1500, 800)
    janela.set_title("In the Arms of Morpheus")
    mouse = Window.get_mouse()
    teclado = Window.get_keyboard()
    nivel = 0

    fundo = GameImage("InTheArmsOfMorpheus/arquivos/menu/menuprincipal.png")
    titulo = Sprite("InTheArmsOfMorpheus/arquivos/menu/titulo.png", 1)

    new_game = Sprite("InTheArmsOfMorpheus/arquivos/menu/newgame.png", 1)
    new_game2 = Sprite("InTheArmsOfMorpheus/arquivos/menu/newgame2.png")

    continuar = Sprite("InTheArmsOfMorpheus/arquivos/menu/continue.png", 1)
    continuar2 = Sprite("InTheArmsOfMorpheus/arquivos/menu/continue2.png", 1)

    '''settings = Sprite("InTheArmsOfMorpheus/arquivos/menu/settings.png", 1)
    settings2 = Sprite("InTheArmsOfMorpheus/arquivos/menu/settings2.png", 1)'''

    sair = Sprite("InTheArmsOfMorpheus/arquivos/menu/quit.png", 1)
    sair2 = Sprite("InTheArmsOfMorpheus/arquivos/menu/quit2.png", 1)

    # Posições iniciais
    new_game.x = janela.width / 2 - new_game.width / 2
    new_game.y = janela.height / 1.83 - new_game.height / 2
    new_game2.x = new_game.x
    new_game2.y = new_game.y

    continuar.x = janela.width / 2 - continuar.width / 2
    continuar.y = janela.height / 1.47 - continuar.height / 2
    continuar2.x = continuar.x
    continuar2.y = continuar.y

    '''settings.x = janela.width / 2 - settings.width / 2
    settings.y = janela.height / 1.38 - settings.height / 2
    settings2.x = settings.x
    settings2.y = settings.y'''

    sair.x = janela.width / 2 - sair.width / 2
    sair.y = janela.height / 1.24 - sair.height / 2
    sair2.x = sair.x
    sair2.y = sair.y

    titulo.x = janela.width / 2 - titulo.width / 2
    titulo.y = janela.height / 2.6 - titulo.height / 2

    # Game Loop
    on = True
    while on:
        # desenho
        fundo.draw()
        titulo.draw()
        new_game.draw()
        if mouse.is_over_object(new_game):
            new_game2.draw()
            if mouse.is_button_pressed(1):
               return -1

        continuar.draw()
        if mouse.is_over_object(continuar):
            continuar2.draw()
            '''if mouse.is_button_pressed(1):'''
        '''settings.draw()
        if mouse.is_over_object(settings):
            settings2.draw()'''
        sair.draw()
        if mouse.is_over_object(sair):
            sair2.draw()
            if mouse.is_button_pressed(1):
                return -10
        janela.update()