# encoding: utf-8
import numpy as np

class Board(object):
	def __init__(self):
		#branco = 1, preto = -1
		self.empty = 0
		self.white = 1
		self.black = -1
		self.highlight = 2
		
		self.board_size = 8
		self.board = np.zeros((8,8), dtype = np.int)
		self.startingPosition()
	
	def startingPosition(self):
		#Posição inicial usualmente utilizada
		self.board[3][3] = self.white
		self.board[3][4] = self.black
		self.board[4][3] = self.black
		self.board[4][4] = self.white	

	def placePieceInPosition(self, color, i, j):
		self.board[i][j] = color
		
	def getElementInPosition(self, i, j):
		return self.board[i][j]

	def isBoardFull(self):
		for row in self.board:
			for colum in row:
				if (colum == self.empty):
					return False
		return True

	def flipPieces(self, color, position, flip_directions):
		i, j = position[0], position[1]
		
		for direction in flip_directions:
			if(direction == 'NW'):
				for line, column in zip(xrange(i + 1, self.board_size), xrange(j+1, self.board_size)):
					if(self.board[line][column] == color):
						break
					else:
						self.board[line][column] = color
			
			elif(direction == 'N'):
				for line in xrange(i + 1, self.board_size):
					if(self.board[line][j] == color):
						break
					else:
						self.board[line][j] = color
			
			elif(direction == 'NE'):
				for line, column in zip(xrange(i + 1, self.board_size), xrange(j-1, 0, -1)):
					if(self.board[line][column] == color):
						break
					else:
						self.board[line][column] = color
			
			elif(direction == 'W'):
				for column in xrange(j + 1, self.board_size):
					if(self.board[i][column] == color):
						break
					else:
						self.board[i][column] = color
			
			elif(direction == 'E'):
				for column in xrange(j-1, 0, -1):
					if(self.board[i][column] == color):
						break
					else:
						self.board[i][column] = color
			
			elif(direction == 'SW'):
				for line, column in zip(xrange(i-1, 0, -1), xrange(j+1, self.board_size)):
					if(self.board[line][column] == color):
						break
					else:
						self.board[line][column] = color
			
			elif(direction == 'S'):
				for line in xrange(i-1, 0, -1):
					if(self.board[line][j] == color):
						break
					else:
						self.board[line][j] = color
				
			elif(direction == 'SE'):
				for line, column in zip(xrange(i-1, 0, -1), xrange(j-1, 0, -1)):
					if(self.board[line][column] == color):
						break
					else:
						self.board[line][column] = color

	def noMoreMoves(self):
		if(self.white not in self.board or self.black not in self.board):
			print "No more moves"
			return True
		else:
			return False

	def printBoard(self):
		GREEN = '\033[92m' 
		WHITE = '\033[60m'
		BLACK = '\033[91m'
		YELLOW = '\033[96m'
		END = '\033[0m'
		count = 0
		print "  0 1 2 3 4 5 6 7"
		for row in self.board:
			print count,
			for column in row:
				if(column == self.empty):
					 print GREEN + '0' + END,
				elif(column == self.black):
					print BLACK + '0' + END,
				elif(column == self.white):
					print WHITE + '0' + END,
				elif(column == self.highlight):
					print YELLOW + '0' + END,
			count += 1
			print
		print
