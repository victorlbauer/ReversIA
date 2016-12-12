import random
import time

class RandomPlayer(object):
	def __init__(self, name, color, board, rulebook):
		self.name = name
		self.color = color
		self.board = board
		self.rulebook = rulebook
		
	def play(self):
		if(self.board.isBoardFull() or self.board.noMoreMoves() or self.rulebook.pass_turn == 2):
			self.rulebook.end_game = True
		else:
			valid_moves = self.rulebook.getValidMoves(self.color, self.board)
			if not valid_moves:
				print "No moves available, player must pass"
				self.rulebook.pass_turn += 1	
			else:
				random_move = random.choice(valid_moves)
				flip_directions = []
				for move in valid_moves:
					if (move[0] == random_move[0]):
						flip_directions.append(move[1])
		
				self.board.placePieceInPosition(self.color, random_move[0][0], random_move[0][1])
				self.rulebook.pass_turn = 0
				self.board.flipPieces(self.color, random_move[0], flip_directions)
	
				return random_move[0]
