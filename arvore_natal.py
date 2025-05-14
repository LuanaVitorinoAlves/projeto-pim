import random
import time
import os

"""
EXERCÍCIO 1 - ÁRVORE DE NATAL

Dado o código da árvore de natal, escreva em cada linha que achar necessário o que ela faz.
"""

linhas = []
#definição dos galhos e enfeeites da árvore
def arvore(n):
    espacos = n // 2
    for i in range(1, n + 1, 2):
        linha = ' ' * espacos
        if i == 1:
            linha += '✫' #estrela do topo
        else:
            decoracao = '--==◉◎◉◎'
            for j in range(i):
                linha += random.choice(decoracao)
        linhas.append(linha)
        espacos -= 1
    espacos = n // 2
    linhas.append(' ' * espacos + '|')
    linhas.append(' ' * (espacos - 1) + '_|_')

#luzes piscando e alternando
def piscar():
    for linha in linhas:
        copia = ''
        for caractere in linha:
            if caractere == '◉' or caractere == '◎':
                copia += random.choice('◉◎')
            else:
                copia += caractere
        print(copia)

#ilusão de piscar, limpa a árvore e adiciona outra em 0.6 milésimos de segundo
def limpar():
    # for i in range(50):
    #     print()
    os.system('cls' if os.name == 'nt' else 'clear')

tamanho = int(input('Tamanho da árvore: '))
arvore(tamanho)

#enquanto o código estiver rodando, repetir o código
while True:
    limpar()
    piscar()
    time.sleep(0.6)