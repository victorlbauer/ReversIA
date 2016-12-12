# encoding: utf-8

class RuleBook(object):
	def __init__(self, board, board_size):
		self.board = board
		self.board_size = board_size
		self.empty = 0
		self.white = 1
		self.black = -1

		self.pass_turn = 0
		self.end_game = False

	def getNeighbours(self, i, j):
		#Verifica os vizinhos da casa visitada, retornando seus valores
		neighbours = []

		neighbourNW = [[[i-1, j-1], 'NW']]
		neighbourN = [[[i-1, j], 'N']]
		neighbourNE = [[[i-1, j+1], 'NE']]
		neighbourW = [[[i, j-1], 'W']]
		neighbourE = [[[i, j+1], 'E']]
		neighbourSW = [[[i+1, j-1], 'SW']]
		neighbourS = [[[i+1, j], 'S']]
		neighbourSE = [[[i+1, j+1], 'SE']]

		#Canto superior esquerdo
		if((i - 1) < 0 and (j - 1) < 0):
			neighbours = neighbourE + neighbourS + neighbourSE			
 
		#Borda superior
		elif((i - 1) < 0 and (j + 1) < self.board_size):
			neighbours = neighbourW + neighbourE + neighbourSW + neighbourS + neighbourSE			

		#Canto superior direito
		elif((i - 1) < 0 and (j + 1) >= self.board_size):
			neighbours = neighbourW + neighbourSW + neighbourS 

		#Borda esquerda
		elif((i - 1) >= 0 and (i + 1) < self.board_size and (j - 1) < 0):		
			neighbours = neighbourN + neighbourNE + neighbourE + neighbourS + neighbourSE

		#Borda direita
		elif((i - 1) >= 0 and (i + 1) < self.board_size and (j + 1) >= self.board_size):
			neighbours = neighbourNW + neighbourN + neighbourW + neighbourSW + neighbourS

		#Canto inferior esquerdo
		elif((i + 1) >= 8 and (j - 1) < 0):
			neighbours = neighbourN + neighbourNE + neighbourE

		#Borda inferior
		elif((i + 1) >= 8 and (j + 1) < self.board_size):
			neighbours = neighbourNW + neighbourN + neighbourNE + neighbourW + neighbourE

		#Canto inferior direito
		elif((i + 1) >= 8 and (j + 1) >= self.board_size):
			neighbours = neighbourNW + neighbourN + neighbourW

		#Qualquer otra posição que não estiver nas bordas
		else:
			neighbours = neighbourNW + neighbourN + neighbourNE + neighbourW + neighbourE + neighbourSW + neighbourS + neighbourSE

		return neighbours

	
	def validPosition(self, board, turn, i, j, x, y):
		#Descobre é possivel realizar um movimento na posição
		
		#Vizinho à diagonal superior esquerda
		if((x == i-1) and (y == j-1)):
			for line, column in zip(xrange(x + 2, self.board_size), xrange(y + 2, self.board_size)):			
				if(board.board[line][column] == turn):
					return True
				elif(board.board[line][column] == self.empty):
					return False

		#Vizinho em cima		
		elif((x == i-1) and (y == j)):
			for line in xrange(x + 2, self.board_size):
				if(board.board[line][y] == turn):
					return True
				elif(board.board[line][y] == self.empty):
					return False
		
		#Vizinho à diagonal superior direita
		elif((x == i-1) and (y == j+1)):
			for line, column in zip(xrange(x + 2, self.board_size), xrange(y - 2, -1, -1)):			
				if(board.board[line][column] == turn):
					return True
				elif(board.board[line][column] == self.empty):
					return False
		
		#Vizinho à esquerda
		elif((x == i) and (y == j-1)):
			for column in xrange(y + 2, self.board_size):
				if(board.board[x][column] == turn):
					return True
				elif(board.board[x][column] == self.empty):
					return False

		#Vizinho à direita
		elif((x == i) and (y == j+1)):
			for column in xrange(y - 2, -1, -1):
				if(board.board[x][column] == turn):
					return True
				elif(board.board[x][column] == self.empty):
					return False
					
		#Vizinho à diagonal inferior esquerda
		elif((x == i+1) and (y == j-1)):
			for line, column in zip(xrange(x - 2, -1, -1), xrange(y + 2, self.board_size)):			
				if(board.board[line][column] == turn):
					return True
				elif(board.board[line][column] == self.empty):
					return False
	
		#Vizinho em baixo
		elif((x == i+1) and (y == j)):
			for line in xrange(x - 2, -1, -1):
				if(board.board[line][y] == turn):
					return True
				elif(board.board[line][y] == self.empty):
					return False

		#Vizinho à diagonal inferior direita
		elif((x == i+1) and (y == j+1)):
			for line, column in zip(xrange(x - 2, -1, -1), xrange(y - 2, -1, -1)):			
				if(board.board[line][column] == turn):
					return True
				elif(board.board[line][column] == self.empty):
					return False
		
		return False


	def verifyMoves(self, board, turn, neighbours, i, j):
		#Dados os vizinho vazios da peça adversaria, retorna uma lista com todas as casas possíveis de se realizar um movimento valido
		valid_positions = []
		for neighbour in neighbours:
			x, y = neighbour[0][0], neighbour[0][1]
			if(board.board[x,y] == self.empty):
				if(self.validPosition(board, turn, i, j, x, y)):
					valid_positions.append(neighbour)
		return valid_positions


	def getValidMoves(self, turn, board):
		#Retorna todos os movimentos validos possiveis no turno

		#whose_turn = turn - De quem é o turno?
		#opponent_color = - whose_turn - Cor do oponente
		valid_moves = []
		opponent_color = - turn
		
		i = 0
		for row in board.board:
			j = 0
			for column in row:
				if(column == opponent_color):
					neighbours = self.getNeighbours(i, j)
					valid_moves += (self.verifyMoves(board, turn, neighbours, i, j))
				j += 1
			i += 1
		
		return valid_moves

	
	def countPoints(self):
		w = 0
		b = 0
		for row in self.board.board:
			for column in row:
				if(column == self.white):
					w += 1
				elif(column == self.black):
					b += 1
		print 'white:', w, '\t/\tblack:', b
		if(w > b):
			print "WHITE WINS!"
		elif(b > w):
			print "BLACK WINS!"
		else:
			print "DRAW!"
			
	def countPointsWindow(self):
		w = 0
		b = 0
		for row in self.board.board:
			for column in row:
				if(column == self.white):
					w += 1
				elif(column == self.black):
					b += 1
		if(w > b):
			return 'white'	
		elif(b > w):
			return 'black'
		else:
			return 'draw'		
