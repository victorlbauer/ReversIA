# encoding: utf-8
import sys
import time
from Agents import *
import board
import rulebook

class Console():
	def __init__(self):
		self.board_size = 8
		self.board = self.initializeBoard()
		self.rulebook = self.initializeRuleBook()
		
		print "Player[1](black) option - ['human', 'random', 'greedy', 'pro']"
		p1 = raw_input("> ")
		self.player1 = self.initializePlayer(p1, self.rulebook.black)
		
		print "Player[2](white) option - ['human', 'random', 'greedy', 'pro']"
		p2 = raw_input("> ")
		self.player2 = self.initializePlayer(p2, self.rulebook.white)
		
	def initializePlayer(self, name, color):
		if(name == 'human'):
			player = humanplayer.HumanPlayer(name, color, self.board, self.rulebook)
		
		elif(name == 'random'):
			player = randomplayer.RandomPlayer(name, color, self.board, self.rulebook)
			
		elif(name == 'greedy'):
			player = greedyplayer.GreedyPlayer(name, color, self.board, self.rulebook)
		
		elif(name == 'pro'):
			player = proplayer.ProPlayer(name, color, self.board, self.rulebook)
				
		elif(name == 'neural'):
			player = neuralplayer.NeuralPlayer(name, color, self.board, self.rulebook)
			
		return player
	
	def initializeBoard(self):
		b = board.Board()
		return b

	def initializeRuleBook(self):
		r = rulebook.RuleBook(self.board, self.board_size)
		return r
		
	def playMatch(self):
		jogada = 1
		self.board.printBoard()
		time.sleep(2)
		while not(self.rulebook.end_game):
			#Player1 joga
			print "Jogada:", jogada
			move_p1 = self.player1.play()
			self.board.printBoard()
			jogada += 1
			
			#Player2 joga
			print "Jogada:", jogada
			move_p2 = self.player2.play()
			self.board.printBoard()
			jogada += 1
		time.sleep(3)
		self.rulebook.countPoints()

if __name__ == "__main__":
	Console = Console()
	Console.playMatch()
