#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 14:49:06 2021

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

Este código implementa o algoritmo minimax para o jogo da velha. Ele será
importado para o código principal. 

"""

import copy

class JogoDaVelha:
    def __init__(self, quem):
        """
        Inicialização do jogo
        
        Estado: representa a situação corrente do jogo
            - 0 --> casa vazia
            - 1 --> casa ocupada pelo jogador 1 (X)
            - 2 --> casa ocupada pelo jogador 2 (O)
            
        Quem: indica se a IA é o X (quem = 1) ou O (quem = 2)
        
        Jogador: indica qual o jogador da vez. O X (1) sempre começa
        
        Resultado: indica o resultado do jogo
            - None --> o jogo não acabou
            - 1 --> o X venceu
            - 2 --> a O venceu
            - 3 --> Deu velha
        """
        self.estado = [[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]]
        self.quem = quem
        self.jogador = 1
        self.resultado = None
    
    def acoes(self, estado = None):
        """
        Retorna as possíveis ações em um determinado estado de jogo
        Cada ação é representada por uma tupla (linha, coluna)
        
        Se não for passado um estado como parâmetro, são retornadas as ações
        para o estado corrente do jogo
        """
        estado = self.estado if not estado else estado
        l_acoes = []
        for linha in range(3):
            for coluna in range(3):
                if not estado[linha][coluna]:
                    l_acoes.append((linha, coluna))
        return l_acoes
    
    def novoEstado(self, acao, jogador, estado = None):
        """
        Retorna o estado do jogo resultante de uma dada ação
        
        Se não for passado um estado como parâmetro, a ação é tomada sobre o 
        estado corrente do jogo
        """
        #O deepcopy foi usado para clonar uma lista aninhada
        n_estado = copy.deepcopy(self.estado) if not estado else copy.deepcopy(estado)
        n_estado[acao[0]][acao[1]] = jogador
        return n_estado
    
    def fim(self, estado = None):
        """
        Indica o resultado do jogo (None, 1, 2 ou 3 - Explicado no __init__)
        
        Se não for passado um estado como parâmetro, considera-se o estado
        corrente do jogo
        """
        estado = self.estado if not estado else estado
        for i in range(3):
            #Checa resultados nas linhas e colunas
            if (estado[i][0] == estado[i][1] == estado[i][2]) and estado[i][0] != 0:
                return estado[i][0]
            elif (estado[0][i] == estado [1][i] == estado[2][i]) and estado[0][i] != 0:
                return estado[0][i]
            
        #Checa resultado nas diagonais   
        if (estado[0][0] == estado[1][1] == estado[2][2]) and estado[0][0] !=0:
            return estado[0][0]
        elif (estado[0][2] == estado[1][1] == estado[2][0]) and estado[0][2] != 0:
            return estado[0][2]
        
        else:
            if not self.acoes(estado):
                #Se não há mais ações possíves e ninguém ganhou, então deu velha
                return 3
            
        return None #Jogo não acabou
    
    def minimo(self, estado):
        """
        Retorna a mínima utilidade de um determinado estado de jogo 
        """
        val_fim = self.fim(estado)
        if val_fim:
            #Se o estado é terminal, é atribuida uma utilidade de acordo com o resultado
            if val_fim == self.quem:
                #IA ganhou
                return 1
            elif val_fim == 3:
                #Deu velha
                return 0
            else:
                #Oponente ganhou
                return -1     
        else:
            #Enquanto o estado não for terminal, será feita uma recursão
            util = 10
            for acao in self.acoes(estado):
                val_max = self.maximo(self.novoEstado(acao,1 if self.quem == 2 else 2, estado))
                util = min(util, val_max)
                if util == -1:
                    #Não tem como ser menor que -1, então não há necessidade 
                    #de checar as outras possibilidades. 
                    return util
            return util
        
    def maximo(self, estado):
        """
        Retorna a máxima utilidade de um determinado estado de jogo 
        """

        val_fim = self.fim(estado)
        if val_fim:
            if val_fim == self.quem:
                return 1
            elif val_fim == 3:
                return 0
            else:
                return -1
        else:
            util = -10
            for acao in self.acoes(estado):
                val_min = self.minimo(self.novoEstado(acao, self.quem,  estado))
                util = max(util, val_min)
                if util == 1:
                    return util
            return util    
        
    def minimax(self):
        """
        Retorna a melhor ação possível para o estado corrente do jogo
        IA sempre busca maximizar --> 1
        O oponente sempre busca minimizar --> -1
        """
        
        possiveis = {} #Dicionário para relacionar utilidades a ações
        if not self.fim(self.estado):
            for acao in self.acoes():
                #Calcula a utilidade para os estados resultantes de cada ação
                #possível no estado corrente
                melhor = self.minimo(self.novoEstado(acao, self.quem))
                if melhor == 1:
                    return acao
                
                #Essa solução faz com que apenas uma ação (a última) seja 
                #armazenada para cada utilidade
                possiveis[melhor] = acao 
                
            if 0 in possiveis.keys():   
                return possiveis[0]
            else:
                return possiveis[-1]    
                    
    def atualiza(self, acao):
        """
        Atualiza o estado do jogo dada uma ação
        """
        if not self.resultado:
            self.estado = self.novoEstado(acao, self.jogador)
            self.jogador = 1 if self.jogador == 2 else 2 
            val_fim = self.fim()
            if val_fim:
                self.resultado = val_fim
        #Nada será atualizado se o jogo já tiver acabado   
        
        
if __name__ == "__main__":    
    """
    Teste da lógica do jogo sem a interface gráfica
    """     
    jogo = JogoDaVelha(1)       
    while not jogo.resultado:
        for i in jogo.estado:
            print (i)       
        print (jogo.jogador, "joga")
        if jogo.quem == jogo.jogador:          
            jogada = jogo.minimax()
            print(f"Minha vez, sou o {jogo.quem}\n")          
        else:
            print ("Tua vez\n")
            linha = input("Linha: ")
            coluna = input("Coluna: ")
            jogada = (int(linha), int(coluna))           
        jogo.atualiza(jogada)        
    print ("Resultado: ", jogo.resultado)
    for i in jogo.estado:
        print (i)
