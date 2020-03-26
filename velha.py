# Módulo contendo a classe usada para guardar os atributos de um jogo da velha.

import random
import uuid

# Classe representando um jogo da velha e seus atributos.
class Game:
    def __init__(self):
        self.tabuleiro = [[None, None, None], [None, None, None], [None, None, None]]
        self.turno = random.choice(['X', 'O'])
        self.id = str(uuid.uuid4())
        self.vencedor = False
        self.empate = False

# Método para determinar se um jogo da velha terminou, em vitória ou empate (velha).
def fimDoJogo(tabuleiro):
	# Checa as linhas do tabuleiro
	for i in range(len(tabuleiro)):
		if (tabuleiro[i][0] != None and tabuleiro[i][0] == tabuleiro[i][1] and tabuleiro[i][0] == tabuleiro[i][2]):
			return [True, tabuleiro[i][0]]
	# Checa as colunas do tabuleiro
	for i in range(len(tabuleiro)):
		if (tabuleiro[0][i] != None and tabuleiro[0][i] == tabuleiro[1][i] and tabuleiro[0][i] == tabuleiro[2][i]):
			return [True, tabuleiro[0][i]]
	# Checa a diagonal principal
	if(tabuleiro[0][0] == tabuleiro[1][1] and tabuleiro[0][0] == tabuleiro[2][2]):
		if(tabuleiro[0][0] != None):
			return [True, tabuleiro[0][0]]
	# Checa a diagonal secundária
	if(tabuleiro[2][0] == tabuleiro[1][1] and tabuleiro[2][0] == tabuleiro[0][2]):
		if(tabuleiro[2][0] != None):
			return [True, tabuleiro[2][0]]
	# Checa se o jogo terminou em velha
	for i in range(len(tabuleiro)):
		for j in range(len(tabuleiro)):
			if(tabuleiro[i][j] == None):
				return [False, tabuleiro[0][0]]

	return [False, "velha"]