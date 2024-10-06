# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 21:45:28 2024

@author: User
"""

import pygame
import random
import sys

# Inicializar o Pygame
pygame.init()

# Definir cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Configurar a tela
LARGURA, ALTURA = 1000, 800
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Space Invader")

# Definir o tamanho padrão das naves
TAMANHO_NAVE = (64, 64)

# Carregar e redimensionar imagens
nave_img = pygame.image.load("F:/Anaconda/socorro/Spacenasci1.jpg")  # Substitua por um caminho válido para a nave
nave_img = pygame.transform.scale(nave_img, TAMANHO_NAVE)  # Redimensionar para 64x64

inimigo_img = pygame.image.load("F:/Anaconda/socorro/naveinimega.jpeg")  # Substitua por um caminho válido para o inimigo
inimigo_img = pygame.transform.scale(inimigo_img, TAMANHO_NAVE)  # Redimensionar para 64x64

fundo = pygame.image.load("F:/Anaconda/socorro/fundo.jpeg")  # Substitua por um caminho válido para o fundo

# Definir parâmetros da nave
nave_largura, nave_altura = TAMANHO_NAVE
nave_x = LARGURA // 2 - nave_largura // 2
nave_y = ALTURA - nave_altura - 10
velocidade_nave = 5

# Propriedades do projétil
velocidade_projeteis = 7

# Propriedades dos inimigos
inimigos = []
velocidade_inimigos = 2
numero_inimigos = 5

# Contador de naves destruídas
naves_destruidas = 0

# Função para desenhar a nave
def desenhar_nave(x, y):
    tela.blit(nave_img, (x, y))

# Função para desenhar o projétil
def desenhar_projeteis(projeteis):
    for proj in projeteis:
        pygame.draw.rect(tela, VERMELHO, proj)

# Função para criar novos inimigos
def criar_inimigos():
    for i in range(numero_inimigos):
        inimigos.append(pygame.Rect(random.randint(0, LARGURA - nave_largura), random.randint(-100, -40), nave_largura, nave_altura))

# Função para desenhar inimigos
def desenhar_inimigos(inimigos):
    for inimigo in inimigos:
        tela.blit(inimigo_img, (inimigo.x, inimigo.y))

# Função para detectar colisão entre projéteis e inimigos
def detectar_colisao(proj, inimigo):
    return proj.colliderect(inimigo)

# Função para detectar colisão entre inimigos e nave do jogador
def detectar_colisao_nave(inimigo, nave):
    return inimigo.colliderect(nave)

# Função principal do jogo
def game_loop():
    global naves_destruidas, velocidade_inimigos
    
    # Variáveis principais do jogo
    rodando = True
    pontuacao = 0

    # Inicializar projéteis como uma lista vazia
    projeteis = []

    # Nave do jogador
    nave_rect = pygame.Rect(nave_x, nave_y, nave_largura, nave_altura)

    criar_inimigos()

    while rodando:
        tela.blit(fundo, (0, 0))  # Desenhar o fundo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            # Verificar se a tecla "ESC" foi pressionada para sair do jogo
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

        # Movimento da nave com o mouse
        nave_rect.x = pygame.mouse.get_pos()[0] - nave_largura // 2

        # Disparo de projéteis (clique do mouse)
        if pygame.mouse.get_pressed()[0]:
            if len(projeteis) < 5:  # Limite de projéteis na tela
                projeteis.append(pygame.Rect(nave_rect.x + nave_largura // 2 - 5, nave_rect.y, 10, 20))

        # Movimento dos projéteis
        projeteis = [proj for proj in projeteis if proj.y > 0]  # Remover projéteis fora da tela
        for proj in projeteis:
            proj.y -= velocidade_projeteis

        # Movimento dos inimigos
        for inimigo in inimigos:
            inimigo.y += velocidade_inimigos
            if inimigo.y > ALTURA:
                inimigo.x = random.randint(0, LARGURA - nave_largura)
                inimigo.y = random.randint(-100, -40)
                pontuacao -= 1  # Perder pontos se inimigos escaparem

        # Verificar colisões de projéteis com inimigos
        for proj in projeteis:
            for inimigo in inimigos:
                if detectar_colisao(proj, inimigo):
                    projeteis.remove(proj)
                    inimigo.x = random.randint(0, LARGURA - nave_largura)
                    inimigo.y = random.randint(-100, -40)
                    naves_destruidas += 1
                    pontuacao += 1  # Ganhar pontos ao acertar inimigos
                    
                    # Aumentar a velocidade dos inimigos ao destruir 20 naves
                    if naves_destruidas % 20 == 0:
                        velocidade_inimigos += 1

        # Verificar colisões entre inimigos e a nave do jogador
        for inimigo in inimigos:
            if detectar_colisao_nave(inimigo, nave_rect):
                rodando = False  # Terminar o jogo ao colidir com a nave do jogador

        # Desenhar elementos na tela
        desenhar_nave(nave_rect.x, nave_rect.y)
        desenhar_projeteis(projeteis)
        desenhar_inimigos(inimigos)

        # Mostrar pontuação
        fonte = pygame.font.Font(None, 36)
        texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, BRANCO)
        tela.blit(texto_pontuacao, (10, 10))

        pygame.display.flip()  # Atualizar tela

        # Limitar a taxa de quadros
        pygame.time.Clock().tick(60)

    # Exibir mensagem de fim de jogo
    fonte_fim = pygame.font.Font(None, 72)
    texto_fim = fonte_fim.render("Game Over", True, VERMELHO)
    tela.blit(texto_fim, (LARGURA // 2 - 150, ALTURA // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(2000)  # Esperar 2 segundos antes de sair

    pygame.quit()
    sys.exit()

# Executar o jogo
game_loop()
