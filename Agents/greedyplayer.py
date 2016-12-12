# encoding: utf-8
import copy


class GreedyPlayer(object):
	def __init__(self, name, color, board, rulebook):
		self.name = name
		self.color = color
		self.board = board
		self.rulebook = rulebook
	
	def totalPieces(self, board, color):
		total_my_color = 0
		total_opponent_color = 0
		for row in board:
			for column in row:
				if(column == color):
					total_my_color += 1
				elif(column == -color):
					total_opponent_color += 1
		return total_my_color - total_opponent_color

	def minimax(self, current_board, depth, color, maximizingPlayer, x, y, alpha, beta):
		if(depth == 0 or current_board.isBoardFull()):
			heuristic = self.totalPieces(current_board.board, color)
			return heuristic, x, y
		
		if(maximizingPlayer):
			bestValue = float("-inf")
			best_i = 0
			best_j = 0
			
			available_tiles = []
			valid_moves = self.rulebook.getValidMoves(color, current_board)
			
			if not valid_moves:
				heuristic = self.totalPieces(current_board.board, color)
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
				heuristic = self.totalPieces(current_board.board, color)
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
		
	def copyBoard(self, board):
		return copy.deepcopy(board)
		
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
				bestValue, best_i, best_j = self.minimax(board_copy, 6, self.color, True, 0, 0, float("-inf"), float("inf"))
				greedy_move = [best_i, best_j]
				
				flip_directions = []
				for move in valid_moves:
					if (greedy_move == move[0]):
						flip_directions.append(move[1])
		
				self.board.placePieceInPosition(self.color, best_i, best_j)
				self.rulebook.pass_turn = 0
				self.board.flipPieces(self.color, greedy_move, flip_directions)
	
				return greedy_move
