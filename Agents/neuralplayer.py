# encoding: utf-8
import copy
import numpy as np

class NeuralPlayer(object):
	def __init__(self, name, color, board, rulebook):
		self.name = name
		self.color = color
		self.board = board
		self.rulebook = rulebook
		self.depth = 4
		
		#Default values
		self.neurons_IL = 64
		self.neurons_HL = 64
		self.neurons_OL = 1
		
		self.W1, self.W2, self.W3 = self.initializeWeights()
		self.b1, self.b2, self.b3 = self.initializeBias()

		print "Neural player incializado"
	
	def copyBoard(self, board):
		return copy.deepcopy(board)	
		
	def initializeWeights(self):
		W1 = np.random.rand(self.neurons_HL, self.neurons_IL)
		W2 = np.random.rand(self.neurons_HL, self.neurons_HL)
		W3 = np.random.rand(self.neurons_OL, self.neurons_HL)
		return W1, W2, W3	
		
	def initializeBias(self):
		b1 = np.random.rand(1, self.neurons_HL)
		b2 = np.random.rand(1, self.neurons_HL)
		b3 = np.random.rand(1, self.neurons_OL)
		return b1[0], b2[0], b3[0]

		
	def feedforward(self, board):
		z1 = np.dot(self.W1, board) + self.b1
		a2 = self.tanh(z1)
		
		z2 = np.dot(self.W2, a2) + self.b2
		a3 = self.tanh(z2)
			
		z3 = np.dot(self.W3, a3) + self.b3
		a4 = self.tanh(z3)
			
		return a4[0]
	
	def tanh(self, x):
		return np.tanh(x)

	def neuralHeuristic(self, board):
		x = np.empty((0, 8))
		for row in board:
			x = np.append(x, row)
		evaluation = self.feedforward(x)
		
		return evaluation
				
	def minimax(self, current_board, depth, color, maximizingPlayer, x, y, alpha, beta):
		if(depth == 0 or current_board.isBoardFull()):
			heuristic = self.neuralHeuristic(current_board.board)
			return heuristic, x, y
		
		if(maximizingPlayer):
			bestValue = float("-inf")
			best_i = 0
			best_j = 0
			
			available_tiles = []
			valid_moves = self.rulebook.getValidMoves(color, current_board)
			
			if not valid_moves:
				heuristic = self.neuralHeuristic(current_board.board)
				return heuristic, x, y
				
			for move in valid_moves:
				if move[0] not in available_tiles:
					available_tiles.append(move[0])
					
			#Para cada filho do nó
			for tile in available_tiles:
				flip_directions = []
				#Verifica por movimentos repitidos
				for moves in valid_moves:
					if (moves[0] == tile):
						flip_directions.append(moves[1])
				#Filho criado
				node = self.copyBoard(current_board)
				i, j = tile[0], tile[1]
				node.placePieceInPosition(color, i, j)
				node.flipPieces(color, tile, flip_directions)
				value, child_i, child_j = self.minimax(node, depth-1, color, False, i, j, alpha, beta)
				if(value > bestValue):
					best_i = i
					best_j = j
					bestValue = value
				alpha = max(alpha, bestValue)
				if(beta <= alpha):
					break
			return bestValue, best_i, best_j
							
		else:
			bestValue = float("inf")
			best_i = 0
			best_j = 0
			
			available_tiles = []
			valid_moves = self.rulebook.getValidMoves(-color, current_board)
			
			if not valid_moves:
				heuristic = self.neuralHeuristic(current_board.board)
				return heuristic, x, y
				
			for move in valid_moves:
				if move[0] not in available_tiles:
					available_tiles.append(move[0])
				
			for tile in available_tiles:
				flip_directions = []
				#Verifica por movimentos repitidos
				for moves in valid_moves:
					if (moves[0] == tile):
						flip_directions.append(moves[1])
				#Filho criado
				node = self.copyBoard(current_board)
				i, j = tile[0], tile[1]
				node.placePieceInPosition(-color, i, j)
				node.flipPieces(-color, tile, flip_directions)
				value, child_i, child_j = self.minimax(node, depth-1, color, True, i, j, alpha, beta)
				if(value < bestValue):
					best_i = i
					best_j = j
					bestValue = value			
				beta = min(beta, bestValue)
				if(beta <= alpha):
					break
			return bestValue, best_i, best_j
			
	def play(self):
		if(self.board.isBoardFull() or self.board.noMoreMoves() or self.rulebook.pass_turn == 2):
			self.rulebook.end_game = True
		else:
			valid_moves = self.rulebook.getValidMoves(self.color, self.board)
			if not valid_moves:
				print "No moves available, player must pass"
				self.rulebook.pass_turn += 1	
			else:
				board_copy = self.copyBoard(self.board)
				bestValue, best_i, best_j = self.minimax(board_copy, self.depth, self.color, True, 0, 0, float("-inf"), float("inf"))
				print bestValue
				neural_move = [best_i, best_j]
				
				flip_directions = []
				for move in valid_moves:
					if (neural_move == move[0]):
						flip_directions.append(move[1])
		
				self.board.placePieceInPosition(self.color, best_i, best_j)
				self.rulebook.pass_turn = 0
				self.board.flipPieces(self.color, neural_move, flip_directions)
	
				return neural_move

