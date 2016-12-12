# Encoding: utf-8
import copy

class ProPlayer(object):
	def __init__(self, name, color, board, rulebook):
		self.name = name
		self.color = color
		self.board = board
		self.rulebook = rulebook
		self.weight_board = self.weightBoard()
		self.depth = 5
	
	def weightBoard(self):
		board = [[4, -3, 2, 2, 2, 2, -3, 4],
			 [-3, -4, -1, -1, -1, -1, -4, -3],
			 [2, -1, 1, 0, 0, 1, -1, 2],
			 [2, -1, 0, 1, 1, 0, -1, 2],
			 [2, -1, 0, 1, 1, 0, -1, 2],
			 [2, -1, 1, 0, 0, 1, -1, 2],
			 [-3, -4, -1, -1, -1, -1, -4, -3],
			 [4, -3, 2, 2, 2, 2, -3, 4]]
		return board
		
	def coinParity(self, board, color):
		total_my_color = 0
		total_opponent_color = 0
		for row in board:
			for column in row:
				if(column == color):
					total_my_color += 1
				elif(column == -color):
					total_opponent_color += 1
		heuristic = 100.0*(float(total_my_color - total_opponent_color)/float(total_my_color + total_opponent_color))
		return heuristic
	
	def mobility(self, board, color):
		my_valid_moves = self.rulebook.getValidMoves(color, board)
		opponent_valid_moves = self.rulebook.getValidMoves(-color, board)
		my_moves = len(my_valid_moves)
		opponent_moves = len(opponent_valid_moves)
		
		if(my_moves + opponent_moves != 0):
			heuristic = 100.0*(float(my_moves - opponent_moves)/float(my_moves + opponent_moves))
			return heuristic
		else:
			return 0
	
	def corners(self, board, color):
		my_corners = self.getCorners(board, color)
		opponent_corners = self.getCorners(board, -color)
		
		if(my_corners + opponent_corners != 0):
			heuristic = 100.0*(float(my_corners - opponent_corners)/float(my_corners + opponent_corners))
			return heuristic
		else:
			return 0
					
	def getCorners(self, board, color):
		total_corners = 0
		if(board[0][0] == color):
			total_corners += 1
		if(board[0][7] == color):
			total_corners += 1
		if(board[7][0] == color):
			total_corners += 1
		if(board[7][7] == color):
			total_corners += 1	
		return total_corners
					
	def stability(self, board, color):				
		my_stability = 0
		opponent_stability = 0
		i = 0
		for row in board:
			j = 0
			for column in row:
				if(column == color):
					my_stability = self.weight_board[i][j]
				elif(column == -color):
					opponent_stability = self.weight_board[i][j]
				j += 1	
			i += 1
		if(my_stability + opponent_stability != 0):
			heuristic = 100.0*(float(my_stability - opponent_stability)/float(my_stability + opponent_stability))
			return heuristic
		else:
			return 0	
	
	def stateValue(self, board, color):
		coin = self.coinParity(board.board, color)
		mobility = self.mobility(board, color)
		corner = self.corners(board.board, color)
		stab = self.stability(board.board, color)
		
		return 30*corner + 5*mobility + 10*stab + 2*coin
		
	def cornerImmediatly(self, board, color):
		pass
		
		
	def copyBoard(self, board):
		return copy.deepcopy(board)
		
	def minimax(self, current_board, depth, color, maximizingPlayer, x, y, alpha, beta):
		if(depth == 0 or current_board.isBoardFull()):
			heuristic = self.stateValue(current_board, color)
			return heuristic, x, y
		
		if(maximizingPlayer):
			bestValue = float("-inf")
			best_i = 0
			best_j = 0
			
			available_tiles = []
			valid_moves = self.rulebook.getValidMoves(color, current_board)
			
			if not valid_moves:
				heuristic = self.stateValue(current_board, color)
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
				
				#captura diagonal imediatamente
				#if(depth == self.depth):
				#	if(i == 0 and j == 0):
				#		return 100, i, j
				#	elif(i == 0 and j == 7):
				#		return 100, i, j
				#	elif(i == 7 and j == 0):
				#		return 100, i, j					
				#	elif(i == 7 and j == 7):
				#		return 100, i, j
										
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
				heuristic = self.stateValue(current_board, color)
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
				pro_move = [best_i, best_j]
				
				flip_directions = []
				for move in valid_moves:
					if (pro_move == move[0]):
						flip_directions.append(move[1])
		
				self.board.placePieceInPosition(self.color, best_i, best_j)
				self.rulebook.pass_turn = 0
				self.board.flipPieces(self.color, pro_move, flip_directions)
	
				return pro_move
