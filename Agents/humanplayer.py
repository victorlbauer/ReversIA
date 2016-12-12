# encoding: utf-8
import time
import sys
import copy

class HumanPlayer(object):
	def __init__(self, name, color, board, rulebook):
		self.name = name
		self.color = color
		self.board = board
		self.rulebook = rulebook
		self.highlightBoard = 0
	
	def copyBoard(self):
		return copy.deepcopy(self.board)
	
	def getHighlight(self, board):
		valid_moves = self.rulebook.getValidMoves(self.color, self.board)
		if not valid_moves:
			self.rulebook.pass_turn += 1
			return board, 1 
		else:	
			board_copy = self.copyBoard()
			for move in valid_moves:
				i, j = move[0][0], move[0][1]
				board_copy.placePieceInPosition(board_copy.highlight, i, j)
			return board_copy, 0
	
	def highlightValidMoves(self, valid_moves, board):
		for move in valid_moves:
			i, j = move[0][0], move[0][1]
			board.placePieceInPosition(self.board.highlight, i, j)
		self.highlightBoard = board
	
	def chooseMove(self, valid_moves):
		print '\nEscolha uma casa: [linha, coluna]'
		choice = raw_input("> ").strip().split()
		choice = [int(x) for x in choice]
			
		invalid_move = False
		for move in valid_moves:
			if (choice == move[0]):
				invalid_move = False
				
		if((len(choice) == 2) and not invalid_move):
			return choice
		else:
			print "Movimento inválido"
			return self.chooseMove(valid_moves)	
		
	def play(self):
		if(self.board.isBoardFull() or self.board.noMoreMoves() or self.rulebook.pass_turn == 2):
			self.rulebook.end_game = True
		else:
			valid_moves = self.rulebook.getValidMoves(self.color, self.board)
			if not valid_moves:
				print "No moves available, player must pass"
				self.rulebook.pass_turn += 1	
			else:
				board_copy = self.copyBoard()
				self.highlightValidMoves(valid_moves, board_copy)
				board_copy.printBoard()
				human_move = self.chooseMove(valid_moves)
				
				flip_directions = []
				for moves in valid_moves:
					if (moves[0] == human_move):
						flip_directions.append(moves[1])
						
				self.board.placePieceInPosition(self.color, human_move[0], human_move[1])
				self.rulebook.pass_turn = 0
				self.board.flipPieces(self.color, human_move, flip_directions)
		
				return human_move	

	def playWindow(self, human_move):
		if(self.board.isBoardFull() or self.board.noMoreMoves() or self.rulebook.pass_turn == 2):
			self.rulebook.end_game = True
		else:
			valid_moves = self.rulebook.getValidMoves(self.color, self.board)
			if not valid_moves:
				print "No moves available, player must pass"	
			else:
				flip_directions = []
				for moves in valid_moves:
					if (moves[0] == human_move):
						flip_directions.append(moves[1])
						
				self.board.placePieceInPosition(self.color, human_move[0], human_move[1])
				self.rulebook.pass_turn = 0
				self.board.flipPieces(self.color, human_move, flip_directions)
		
				return human_move	

