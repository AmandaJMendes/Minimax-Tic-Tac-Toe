#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 08:53:03 2021

@author: amanda
"""

"""
Projeto 1 - Algoritmos e Estruturas de Dados

Autora: Amanda Jorge Mendes
Matrícula: 149344

O projeto proposto consiste em um jogo da velha em que o usuário jogará
contra um algoritmo de inteligência artificial. A estrutura gráfica do jogo
será a mesma de um jogo da velha convencional. Para o projeto, será implementada
uma interface gráfica para que o jogador possa definir suas ações através de
comandos no teclado. Além disso, para que o computador possa conduzir suas
jogadas contra o usuário de forma ótima, será implementado um código de tomada
de decisão baseado no algoritmo minimax.

Este é o código principal. 

"""

from graphics import *
from MinimaxTicTacToe import JogoDaVelha


def X(janela, x, y):
    """
    Retorna os elementos de um X em um ponto (x,y)
    """
    l1 = Line(Point(x-25, y-25), Point (x+25, y+25))
    l1.setOutline("white")
    l1.setWidth(5)
    l2 = Line(Point(x-25, y+25), Point (x+25, y-25))
    l2.setOutline("white")
    l2.setWidth(5)
    return l1, l2

def O(janela, x, y):
    """
    Retorna o elemento de uma O em um ponto (x,y)
    """
    c = Circle(Point(x, y), 25)
    c.setOutline("white")
    c.setWidth(5)
    return c
 
def move(direcao):
    """
    Altera a variável de posição i de acordo com a tecla pressionada
    pelo usuário. Qualquer outra tecla será ignorada.
    """
    global i #Representa a posição na tela. É modificado pelos cliques nas setas do teclado.  
    #Durante o jogo essa variável varia entre 0 e 8 (9 casas). 
    #No início, varia entre 0 e 1 (seleção de X ou O)
    
    if len(ocupados) == 9:
        return None
    
    if direcao == "Left":
        itens_jogo[i].setFill("black")
        if i > 0:                   
            i -= 1
        else:
            i = 8
            
    elif direcao == "Right":
        itens_jogo[i].setFill("black")
        if i < 8:
            i += 1
        else:
            i = 0
            
    elif direcao == "Up":
        itens_jogo[i].setFill("black")
        if i > 2:     
            i -= 3
        else:
            i += 6
            
    elif direcao == "Down":
        itens_jogo[i].setFill("black")
        if i < 6:
            i += 3   
        else:
            i -= 6
            
    if i in ocupados:
        move (direcao)
        
    else:
        itens_jogo[i].setFill("white")
    

janela = GraphWin("Jogo da Velha", 600, 600)
janela.setBackground("black")
t_fechar=Text(Point(300, 585),"Click on the screen to exit the game.") 
t_fechar.setTextColor("white")
t_fechar.draw(janela)

titulo = Text(Point (300, 100), "TIC-TAC-TOE")
titulo.setFill("white")
titulo.setSize(36) 

instru = Text(Point (300, 250), "X begins. Select your player (X or O)")
instru.setFill("white")
instru.setSize(20)

tecl = Text(Point (300, 500),"Use arrows and enter to play")
tecl.setFill("white")
tecl.setSize(15)

rx = Rectangle(Point(75, 300), Point (275, 400))
rx.setOutline("white")
rx.setWidth(0)

ro = Rectangle(Point(325, 300), Point (525, 400))
ro.setOutline("white")
ro.setWidth(0)

x1, x2 = X(janela, 175, 350)
x1.setOutline("black")
x2.setOutline("black")

o = O (janela, 425, 350)
o.setOutline("black")
#Armazena os elementos gráficos da tela inicial. Assim, eles podem só ser 
#desenhados e apagados, não precisam ser recriados. 
itens_inicio= [titulo, instru, tecl,  rx, ro, x1, x2, o]  

 
itens_jogo = [] #Armazena os elementos gráficos da tela de jogo.
for y in range(150, 351, 100):
       for x in range(150, 351, 100):
           rect = Rectangle(Point(x, y), Point (x+100, y+100))
           rect.setOutline("white")
           rect.setWidth(3)            
           itens_jogo.append(rect)


resultado = Text(Point(300, 100), "")
resultado.setSize(30)
resultado.setTextColor("white")

novo = Text(Point(300, 550),"Press enter to play again")
novo.setSize(20)
novo.setTextColor("white")

itens_fim = [resultado, novo] #Armazena os elementos gráficos da tela final.

#t indica a situação corrente do jogo
#i: início; ij: transição início-jogo; j: jogo; r: resultado 
t = "i"  
fecha = janela.checkMouse()

while not fecha:     
    key = janela.checkKey()
    if t == "i":   
        for item in itens_inicio:
            item.draw(janela)                     
        i = 1  
        rx.setFill("rosybrown1")
        ro.setFill("white")         
        t = "ij" #Passa para a fase de transição entre tela inicial e jogo     
        
    elif t == "ij":        
        if key == "Left" or key == "Right" or key == "Up" or key == "Down":
            i = 1 if not i else 0           
            if i:
                rx.setFill("rosybrown1")
                ro.setFill("white")              
            else:
                rx.setFill("white")
                ro.setFill("rosybrown1")               
        elif key == "Return":         
            for item in itens_inicio:
                item.undraw()                
            for item in itens_jogo:
                item.draw(janela)               
            itens_jogo[0].setFill("white")
            #Para JogoDaVelha:
            #2 --> IA é O e 1 --> IA é X 
            #i=1 --> Usuário X / IA O e i=0 --> Usuário O / IA X
            jogo = JogoDaVelha(i+1) 
            ocupados = [] #Armazena os índices das casas ocupadas
            formas = [] #Armazena os elementos de X e O para que possam ser apagados depois
            i = 0
            t = "j" #Passa para a fase de jogo
        
    elif t == "j":        
        if jogo.resultado:
            itens_jogo[i].setFill("black")           
            if jogo.resultado == 3:
                itens_fim[0].setText("Draw!")
            elif jogo.resultado == jogo.quem:
                itens_fim[0].setText("AI won!")
            else:
                itens_fim[0].setText("Congrats, you're the winner!")            
            for item in itens_fim:
                item.draw(janela)
            t = "r" #Passa para a fase de resultado     
        else:
            if jogo.jogador == jogo.quem:
                #Vez da IA
                jogada = jogo.minimax() #Tupla (linha (0 a 3), coluna (0 a 3))
                
                if jogo.quem == 1:
                    x1, x2 = X(janela, jogada[1] * 100 + 200, jogada[0] * 100 + 200)
                    formas += [x1, x2]
                    x1.draw(janela)
                    x2.draw(janela)
                else:
                    o = O(janela, jogada[1] * 100 + 200, jogada[0] * 100 + 200) 
                    formas.append(o)
                    o.draw(janela)
                jogo.atualiza(jogada)
                ocupados.append(jogada[0] * 3 + jogada[1])
                #jogada[0] * 3 + jogada[1] é a maneira de converter uma 
                #tupla (linha, coluna) para um índice (0-8)
                if i == jogada[0]*3+jogada[1]:
                    #Se a casa em que a IA jogou estiver "selecionada" 
                    #pelo usuário (casa branca), passa a seleção para a próxima casa
                    move("Right")           
            else: 
                #Vez do usuário                    
                if key == "Return":                  
                    itens_jogo[i].setFill("black")
                    ocupados.append(i)
                    #(int(i/3), i % 3) é a maneira de converter um índice (0-8)
                    #para uma tupla (linha, coluna)
                    if jogo.quem == 2:
                        x1, x2 = X(janela, (i % 3) * 100 + 200, int(i/3) * 100 + 200)
                        formas += [x1, x2]
                        x1.draw(janela)
                        x2.draw(janela)
                    else:
                        o = O(janela, (i % 3) * 100 + 200, int(i/3) * 100 + 200) 
                        formas.append(o)
                        o.draw(janela)
                    jogo.atualiza((int(i/3), i % 3))
                    move("Right")
                    
                elif key == "Left" or key == "Right" or key == "Up" or key == "Down":
                    move(key)
    
    elif t == "r":
        #Para reiniciar, o usuário deve pressionar Enter
        if key == "Return":            
            #Apaga os elementos para reiniciar           
            for item in itens_jogo:
                item.undraw()
            for item in itens_inicio + itens_fim + formas:
                item.undraw()
            t = "i" #Reinicia o jogo

    fecha = janela.checkMouse()
    
janela.close()
         
         
         
    