from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
import NewArmsOfMorpheus
import pygame
from pygame import sprite
from pygame.locals import *
from pygame import mixer

def livro():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()  # música

    pygame.mixer.music.load('InTheArmsOfMorpheus/arquivos/musicas/historia_musica.wav')
    pygame.mixer.music.play(-1, 0.0, 15000)
    pygame.mixer.music.set_volume(0.3)

    janela = Window(1300, 700)
    janela.set_title("In the Arms of Morpheus")
    mouse = Window.get_mouse()
    teclado = Window.get_keyboard()

    fundo = GameImage("InTheArmsOfMorpheus/cenário/historia/livro_fechado.png")
    fundo2 = GameImage("InTheArmsOfMorpheus/cenário/historia/livro_aberto.png")

    variavel = False

    # Game Loop
    on = True
    while on:

        fundo.draw()
        if variavel == False:
            janela.draw_text(f"Pressione Enter para ler", (800) , (570), size=40, color=(218, 165, 32), font_name='pixel-art')

        if(teclado.key_pressed("ENTER")):
            variavel = True
        if variavel == True:
            fundo2.draw()
            janela.draw_text(f"Pressione espaço para começar sua aventura", (700) , (570), size=33, color=(0, 0, 0), font_name='pixel-art')
            if (teclado.key_pressed("SPACE")):
                pygame.mixer.music.unload()
                return 0
                

        janela.update()

