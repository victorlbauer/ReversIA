# encoding: utf-8
import sys
from PIL import ImageTk, Image
from Tkinter import *
from Agents import *
import time
import board
import rulebook


class Window(object):
	def __init__(self, width, height):
		self.board_size = 8
		self.board = self.initializeBoard()
		self.rulebook = self.initializeRuleBook()
		self.root, self.canvas = self.initializeWindow(width, height)
		self.canvas.bind("<Button-1>", self.click)
		
		self.RR_flag = 0
		self.robot_vs_robot = False
		self.human_playing = IntVar()
		
		self.c_empty = 0
		self.c_black = -1
		self.c_white = 1
		self.c_highlight = 2
		
########################################################################################################################
		self.background = ImageTk.PhotoImage(file='./Images/background.jpg')
		self.board_edge = ImageTk.PhotoImage(file='./Images/board_edge.jpg')

		self.reversia = ImageTk.PhotoImage(file='./Images/reversia.gif')		
		self.human_human = ImageTk.PhotoImage(file='./Images/humanvshuman.jpg')
		self.human_robot = ImageTk.PhotoImage(file='./Images/humanvsrobot.jpg')
		self.robot_robot = ImageTk.PhotoImage(file='./Images/robotvsrobot.jpg')
	
		self.human_option = ImageTk.PhotoImage(file='./Images/human_option.jpg')
		self.random_option = ImageTk.PhotoImage(file='./Images/random_option.jpg')
		self.greedy_option = ImageTk.PhotoImage(file='./Images/greedy_option.jpg')
		self.pro_option = ImageTk.PhotoImage(file='./Images/pro_option.jpg')

		self.empty = ImageTk.PhotoImage(file='./Images/empty.jpg')
		self.white = ImageTk.PhotoImage(file='./Images/white.jpg')
		self.black = ImageTk.PhotoImage(file='./Images/black.jpg')
		self.highlight = ImageTk.PhotoImage(file='./Images/highlight.jpg')
########################################################################################################################
		
	def initializeBoard(self):
		b = board.Board()
		return b

	def initializeRuleBook(self):
		r = rulebook.RuleBook(self.board, self.board_size)
		return r

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

	def deleteMenu(self):
		self.canvas.delete('human_human')
		self.canvas.delete('human_robot')
		self.canvas.delete('robot_robot')
	
	def chooseColor(self):
		self.canvas.create_text(248, 202, anchor=W, fill='black', font=('Arial', 18, "bold"), tags='text', text='First player color:', width=500)
		self.canvas.create_text(250, 200, anchor=W, fill='white', font=('Arial', 18, "bold"), tags='text', text='First player color:', width=500)	
		self.canvas.create_rectangle(250, 230, 300, 280, fill='white', tags='choice_white')
		self.canvas.create_rectangle(398, 228, 452, 282, fill='white', tags='choice')
		self.canvas.create_rectangle(400, 230, 450, 280, fill='black', tags='choice_black')
	
	def chooseDifficultyHR(self):
		self.canvas.create_text(188, 132, anchor=W, fill='black', font=('Arial', 18, "bold"), tags='text', text='Choose computer difficulty:', width=500)
		self.canvas.create_text(190, 130, anchor=W, fill='white', font=('Arial', 18, "bold"), tags='text', text='Choose computer difficulty:', width=500)
		self.canvas.create_image(180, 160, image=self.random_option, anchor=NW, tags='random_option')	
		self.canvas.create_image(310, 160, image=self.greedy_option, anchor=NW, tags='greedy_option')	
		self.canvas.create_image(440, 160, image=self.pro_option, anchor=NW, tags='pro_option')	
		
		self.canvas.create_text(228, 302, anchor=W, fill='black', font=('Arial', 18, "bold"), tags='text', text='Your current difficulty:', width=500)
		self.canvas.create_text(230, 300, anchor=W, fill='white', font=('Arial', 18, "bold"), tags='text', text='Your current difficulty:', width=500)
		self.canvas.create_image(310, 330, image=self.human_option, anchor=NW, tags='human_option')	
	
	def chooseDifficultyRR(self):
		self.canvas.create_text(188, 172, anchor=W, fill='black', font=('Arial', 18, "bold"), tags='text', text='Choose computer difficulty:', width=500)
		self.canvas.create_text(190, 170, anchor=W, fill='white', font=('Arial', 18, "bold"), tags='text', text='Choose computer difficulty:', width=500)
		self.canvas.create_image(180, 200, image=self.random_option, anchor=NW, tags='random_option')	
		self.canvas.create_image(310, 200, image=self.greedy_option, anchor=NW, tags='greedy_option')	
		self.canvas.create_image(440, 200, image=self.pro_option, anchor=NW, tags='pro_option')	
	
	def robotRedraw(self):
		self.canvas.delete('text')
		self.canvas.create_text(218, 172, anchor=W, fill='black', font=('Arial', 18, "bold"), tags='text', text='Choose P(2) difficulty:', width=500)
		self.canvas.create_text(220, 170, anchor=W, fill='white', font=('Arial', 18, "bold"), tags='text', text='Choose P(2) difficulty:', width=500)
	
	def deleteDifficulty(self):
		self.canvas.delete('text')
		self.canvas.delete('random_option')
		self.canvas.delete('greedy_option')
		self.canvas.delete('pro_option')
		self.canvas.delete('human_option')
		
	def cleanBoard(self):
		self.canvas.delete('choice_white')
		self.canvas.delete('choice_black')
		self.canvas.delete('choice')
		self.canvas.delete('reversia')
		self.canvas.delete('text')
	
	def whoseTurn(self, jogada):
		#pretas jogam
		self.canvas.delete('whoseturn')
		if(jogada & 1):
			self.canvas.create_rectangle(468, 123, 522, 177, fill='white', tags='whoseturn')
			self.canvas.create_rectangle(470, 125, 520, 175, fill='black', tags='whoseturn')
		else:
			self.canvas.create_rectangle(470, 125, 520, 175, fill='white', tags='whoseturn')
	
	def drawScores(self):
		self.canvas.create_rectangle(468, 273, 522, 327, fill='white', tags='score_bg')
		self.canvas.create_rectangle(470, 275, 520, 325, fill='black', tags='score_bg')
		self.canvas.create_rectangle(570, 275, 620, 325, fill='white', tags='score_bg')
	
	def updateScores(self):
		self.canvas.delete('score')
		white = 0
		black = 0
		for row in self.board.board:
			for column in row:
				if(column == self.c_white):
					white += 1
				elif(column == self.c_black):
					black += 1
		self.canvas.create_text(495, 300, anchor=CENTER, fill='white', font=('Arial', 18, "bold"), tags='score', text='%s' % black, width=500)
		self.canvas.create_text(595, 300, anchor=CENTER, fill='black', font=('Arial', 18, "bold"), tags='score', text='%s' % white, width=500)
	
	def victory(self, who):
		if(who == 'white'):
			self.canvas.create_text(60, 220, anchor=W, fill='white', font=('Arial', 40, "bold"), text='WHITE WINS!', width=600)
		elif(who == 'black'):
			self.canvas.create_text(50, 225, anchor=W, fill='black', font=('Arial', 40, "bold"), text='BLACK WINS!', width=600)
		else:
			self.canvas.create_text(100, 200, anchor=W, fill='red', font=('Arial', 60, "bold"), text='DRAW!', width=600)
			
	def human_human_handler(self):
		self.deleteMenu()
		self.player1 = self.initializePlayer('human', self.rulebook.black)
		self.player2 = self.initializePlayer('human', self.rulebook.white)
		self.cleanBoard()
		self.tile_tags, self.tile_positions = self.drawBoard()	
		self.playMatch()
				
	def human_robot_handler(self):
		self.deleteMenu()
		self.chooseDifficultyHR()
		
	def robot_robot_handler(self):
		self.deleteMenu()
		self.RR_flag +=1
		self.chooseDifficultyRR()
		
	def click(self, event):
		obj_id = self.canvas.find_closest(event.x, event.y)
		tag = self.canvas.gettags(obj_id[0])
		obj_id = obj_id[0]
		tag = tag[0]
		
		if(tag == 'human_human'):
			self.human_human_handler()
		if(tag == 'human_robot'):
			self.human_robot_handler()
		if(tag == 'robot_robot'):
			self.robot_vs_robot = True
			self.robot_robot_handler()
		
		if(tag == 'random_option'):
			self.RR_flag +=1
			if(self.RR_flag == 2):
				self.pc1 = 'random'
				self.robotRedraw()
			else:	
				self.pc2 = 'random'				
				self.deleteDifficulty()
				self.chooseColor()

		if(tag == 'greedy_option'):
			self.RR_flag +=1
			if(self.RR_flag == 2):
				self.pc1 = 'greedy'
				self.robotRedraw()
			else:	
				self.pc2 = 'greedy'				
				self.deleteDifficulty()
				self.chooseColor()
			
		if(tag == 'pro_option'):
			self.RR_flag +=1
			if(self.RR_flag == 2):
				self.pc1 = 'pro'
				self.robotRedraw()
			else:	
				self.pc2 = 'pro'				
				self.deleteDifficulty()
				self.chooseColor()
			
		if(tag == 'choice_white'):
			if(self.robot_vs_robot):
				self.player1 = self.initializePlayer(self.pc2, self.rulebook.black)
				self.player2 = self.initializePlayer(self.pc1, self.rulebook.white)
			else:	
				self.player1 = self.initializePlayer(self.pc2, self.rulebook.black)
				self.player2 = self.initializePlayer('human', self.rulebook.white)
			self.cleanBoard()
			self.tile_tags, self.tile_positions = self.drawBoard()	
			self.playMatch()

		if(tag == 'choice_black'):
			if(self.robot_vs_robot):
				self.player1 = self.initializePlayer(self.pc1, self.rulebook.black)
				self.player2 = self.initializePlayer(self.pc2, self.rulebook.white)
			else:
				self.player1 = self.initializePlayer('human', self.rulebook.black)
				self.player2 = self.initializePlayer(self.pc2, self.rulebook.white)
			self.cleanBoard()
			self.tile_tags, self.tile_positions = self.drawBoard()	
			self.playMatch()

		img = self.canvas.itemcget(obj_id, 'image')
		if(img == 'pyimage14'):
			i = 0
			for row in self.tile_tags:
				j = 0
				for column in row:
					if(column == tag):
						pos = [i, j]
						break
					j += 1
				i += 1
			self.move = pos
			self.human_playing.set(1)
		
	def initializeMenu(self):
		self.canvas.create_image(0, 0, image=self.background, anchor=NW, tags='background')
		self.canvas.create_image(200, 30, image=self.reversia, anchor=NW, tags='reversia')
		self.canvas.create_image(225, 150, image=self.human_human, anchor=NW, tags='human_human')
		self.canvas.create_image(225, 250, image=self.human_robot, anchor=NW, tags='human_robot')
		self.canvas.create_image(225, 350, image=self.robot_robot, anchor=NW, tags='robot_robot')
							
	def initializeWindow(self, w, h):
		#Root
		root = Tk()
		root.title("ReversIA")
		root.geometry("%ix%i" % (w, h))
		root.resizable(width=False, height=False)

		#Canvas
		canvas = Canvas(root, bg='white', width=w, height=h, cursor='hand1') 		
		canvas.pack()
		
		return root, canvas
	
	def drawBoard(self):
		self.canvas.create_image(15, 15, image=self.board_edge, anchor=NW, tags='board_edge')
		
		tile_tags = []
		tile_positions = []
		
		temp_tag_list = []
		temp_pos_list = []
		
		offset_x = 25
		offset_y = 25
		tile_width = 50
		i = 0
		for row in self.board.board:
			j = 0
			for column in row:
				tile_tag = "tile" + str(i) + str(j)
				temp_pos_list.append([offset_x, offset_y])
				temp_tag_list.append(tile_tag)
				if(column == self.board.empty):
					self.canvas.create_image(offset_x, offset_y , image=self.empty, anchor=NW, tags=tile_tag)
					offset_x += tile_width
				elif(column == self.board.white):
					self.canvas.create_image(offset_x, offset_y , image=self.white, anchor=NW, tags=tile_tag)
					offset_x += tile_width
				elif(column == self.board.black):
					self.canvas.create_image(offset_x, offset_y , image=self.black, anchor=NW, tags=tile_tag)
					offset_x += tile_width
				elif(column == self.board.highlight):
					self.canvas.create_image(offset_x, offset_y , image=self.highlight, anchor=NW, tags=tile_tag)
					offset_x += tile_width
				j += 1
			i += 1
			tile_tags.append(temp_tag_list)
			tile_positions.append(temp_pos_list)
			temp_tag_list = []
			temp_pos_list = []
			offset_x = 25			
			offset_y += tile_width
		
		self.canvas.create_oval((170, 170), (180, 180), fill='black', tags='dot')
		self.canvas.create_oval((270, 170), (280, 180), fill='black', tags='dot')
		self.canvas.create_oval((170, 270), (180, 280), fill='black', tags='dot')
		self.canvas.create_oval((270, 270), (280, 280), fill='black', tags='dot')
		
		self.canvas.create_text(533, 150, anchor=W, fill='black', font=('Arial', 30, "bold"), tags='turn_text', text='TURN', width=500)
		self.canvas.create_text(535, 150, anchor=W, fill='orange', font=('Arial', 30, "bold"), tags='turn_text', text='TURN', width=500)
		
		return tile_tags, tile_positions
			
	def updateBoard(self, board):
		offset_x = 25
		offset_y = 25
		tile_width = 50
		i = 0
		for row in board.board:
			j = 0
			for column in row:
				self.canvas.delete(self.tile_tags[i][j])
				if(column == board.empty):
					self.canvas.create_image(offset_x, offset_y , image=self.empty, anchor=NW, tags=self.tile_tags[i][j])
					offset_x += tile_width
				elif(column == board.white):
					self.canvas.create_image(offset_x, offset_y , image=self.white, anchor=NW, tags=self.tile_tags[i][j])
					offset_x += tile_width
				elif(column == board.black):
					self.canvas.create_image(offset_x, offset_y , image=self.black, anchor=NW, tags=self.tile_tags[i][j])
					offset_x += tile_width
				elif(column == board.highlight):
					self.canvas.create_image(offset_x, offset_y , image=self.highlight, anchor=NW, tags=self.tile_tags[i][j])
					offset_x += tile_width
				j += 1
			i += 1
			offset_x = 25			
			offset_y += tile_width
		
		self.canvas.delete('dot')
		self.canvas.create_oval((170, 170), (180, 180), fill='black', tags='dot')
		self.canvas.create_oval((270, 170), (280, 180), fill='black', tags='dot')
		self.canvas.create_oval((170, 270), (180, 280), fill='black', tags='dot')
		self.canvas.create_oval((270, 270), (280, 280), fill='black', tags='dot')
		
		self.root.update()
	
	def makeAMove(self, player, name):
		if(name == 'human'):
			highlight, valid_flag = player.getHighlight(self.board)
			self.updateBoard(highlight)
			if(valid_flag == 1):
				return 0
			if(self.board.isBoardFull() or self.board.noMoreMoves() or self.rulebook.pass_turn == 2):
				self.rulebook.end_game = True
				return 0
			self.root.wait_variable(self.human_playing)
			#Human plays
			move = player.playWindow(self.move)
			self.human_playing.set(0)
			return move
		else:
			move = player.play()
			return move
		
	def playMatch(self):
		jogada = 1
		self.drawScores()
		self.updateScores()
		self.updateBoard(self.board)
		time.sleep(2)
		while not(self.rulebook.end_game):
			#Player1 joga
			self.whoseTurn(jogada)
			self.updateBoard(self.board)	
			move_p1 = self.makeAMove(self.player1, self.player1.name)
			print "Player[1] move:", move_p1
			self.updateScores()
			self.updateBoard(self.board)	
			jogada += 1
			
			#Player2 joga
			self.whoseTurn(jogada)
			self.updateBoard(self.board)
			move_p2 = self.makeAMove(self.player2, self.player2.name)
			print "Player[2] move:", move_p2
			self.updateScores()
			self.updateBoard(self.board)	
			jogada += 1
		time.sleep(2)
		who = self.rulebook.countPointsWindow()
		self.victory(who)
		
if __name__ == '__main__':
	window = Window(700, 470)
	window.initializeMenu()
	window.root.mainloop()
