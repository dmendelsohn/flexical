#This is my own custom wordfinder for scrabble-esque games
#TODO: Add link to paper

import Tkinter as tk
import pickle
import tkSimpleDialog
from trie import WordTrie
from board import Board
from constants import *

## GUI CODE ##
class App(tk.Frame):
	def __init__(self, master, board):
		tk.Frame.__init__(self, master)
		self.board = board
		self.preview_letters = {} #Format is (row,col):'X'
		self.possible_moves = []
		self.grid()
		self.create_widgets()
		self.render_board_grid()

	def on_key_press(self, i, j, event):
		if event.keysym == 'Left':
			j -= 1
		elif event.keysym == 'Right':
			j += 1
		elif event.keysym == 'Up':
			i -= 1
		elif event.keysym == 'Down':
			i += 1
		if i >= 0 and j >= 0 and i < self.board.size and j < self.board.size:
			self.squares[i][j].focus_set()
		elif i == self.board.size:
			self.rack_entry.focus_set()

	def set_default_text_color(self, i, j):
		self.squares[i][j].configure(foreground=DEFAULT_TEXT_COLOR)

	def on_rack_key_press(self, event):
		if event.keysym == 'Up':
			self.squares[-1][5].focus_set()

	def on_list_select(self, event):
		w = event.widget
		index = int(w.curselection()[0])
		if index < len(self.possible_moves):
			move = self.possible_moves[index]
			self.display_move(move)
		else:
			print "Selected index is out of bounds, somehow"

	#Updates the board data structure to reflect board shown on GUI
	def update_board(self):
		for i in range(self.board.size):
			for j in range(self.board.size):
				if (i,j) not in self.preview_letters: #Only count non-preview letters
					letter = self.squares[i][j].get()
					self.board.set_tile(i,j,letter)

	def find_moves(self, event=None):
		print "Getting moves"
		rack = list(self.rack_entry.get())
		self.update_board()
		moves = self.board.get_all_moves(rack)
		self.clear_preview()
		self.possible_moves = moves
		self.update_move_list()
	
	def update_move_list(self): #Moves are (word, i, j, score, isVertical) tuple
		self.listbox.delete(0,tk.END) #Clear the list
		for move in self.possible_moves:
			self.listbox.insert(tk.END, self.get_move_string(move))
		self.listbox.selection_clear(0,tk.END)
		self.listbox.selection_set(0)
		if len(self.possible_moves) > 0:
			self.display_move(self.possible_moves[0])

	def get_move_string(self, move):
		return ' %d pts: %s' % (move[3], move[0])

	def display_move(self, move):
		self.clear_preview()
		(word, i, j, score, isVertical) = move
		for letter in word:
			if self.board.is_empty_square(i,j): # Only if this letter is new
				self.render_letter_preview(letter, i, j) # Render onto board
				self.preview_letters[(i,j)] = letter # Add to dict of preview letters
			if isVertical:
				i+=1 #Increment row
			else:
				j+=1 #Increment column

	def render_letter_preview(self, letter, i, j):
		e = self.squares[i][j]
		e.configure(foreground=PREVIEW_TEXT_COLOR)
		e.insert(0, letter)

	def clear_preview(self):
		for (i,j) in self.preview_letters:
			self.clear_letter_preview(i,j)
		self.preview_letters = {}

	def clear_letter_preview(self, i, j):
		e = self.squares[i][j]
		e.delete(0,tk.END)
		e.configure(foreground=DEFAULT_TEXT_COLOR)

	def perform_selected_move(self):
		selection_list = map(int, self.listbox.curselection())
		if len(selection_list) > 0:
			index = selection_list[0]
			move = self.possible_moves[index]
			self.perform_move(move)
		else:
			print "You need to select a move."

	def clear_possible_moves(self):
		self.possible_moves = [] #Clear the list of possible moves
		self.listbox.delete(0, tk.END)

	def render_clean(self):
		self.clear_preview()
		self.clear_possible_moves()
		for i in range(self.board.size):
			for j in range(self.board.size):
				self.squares[i][j].delete(0, tk.END) #Clear any letter that might be there
				self.squares[i][j].insert(0, self.board.grid[i][j]) #Insert appropriate letter

	def import_board(self):
		print "Importing board"
		filename = FileEntryDialog(self).result
		try:
			self.board = pickle.load(open(filename, "rb"))
			self.render_clean()
			print "Imported board"
		except:
			print "Invalid file name for importing board"

	def save_board(self):
		print "Saving board"
		self.update_board()
		filename = FileEntryDialog(self).result
		try:
			pickle.dump(self.board, open(filename, "wb"))
			print "Save successful"
		except:
			print "Save failed"

	def perform_move(self, move):
		for (i,j) in self.preview_letters:
			self.squares[i][j].configure(foreground=DEFAULT_TEXT_COLOR)
		self.preview_letters = {} #Clear the preview letters
		self.clear_possible_moves()
		#TODO: Once a game engine and scoring are implemented, scoring logic here

	def create_widgets(self):
		n = self.board.size
		def is_ok_entry(self, text):
			return len(text) == 0 or (len(text) == 1 and text.isalpha())
		okay_command = self.register(is_ok_entry)
		self.squares = [[None for i in range(15)] for j in range(15)]
		for i in range(n):
			for j in range(n):
				# Set up this widget's custom handler for key presses, callback to main handler
				def handle_key_press(event, i=i, j=j):
					self.on_key_press(i, j, event)
				def default_text(event, i=i, j=j):
					self.set_default_text_color(i, j)
				self.squares[i][j] = tk.Entry(self, width=2, justify=tk.CENTER,\
						validate='all', validatecommand=(okay_command, self, '%P'))
				e = self.squares[i][j]
				e.grid(row=i, column=j)
				e.bind('<Left>', handle_key_press)
				e.bind('<Right>', handle_key_press)
				e.bind('<Up>', handle_key_press)
				e.bind('<Down>', handle_key_press)
				e.bind('<Return>',self.find_moves)
				# Make sure that any user keypress forces the color back to default
				for letter in LOWER_CASE_LETTERS:
					e.bind(letter, default_text)
				if (i,j) in BONUS_DICT:
					bonus = BONUS_DICT[(i,j)]
					color = BONUS_COLORS[bonus]
					e.configure(background=color)
		tk.Label(self, text='Enter your rack: ')\
				.grid(columnspan=4, row=n, column=0, sticky=tk.W)
		def is_ok_rack(self, text):
			for l in text:
				if not l.islower() and l != UNUSED_BLANK_CHAR:
					return False
			return True
		ok_rack_command = self.register(is_ok_rack)
		self.rack_entry = tk.Entry(self, width=10, justify=tk.CENTER, \
				validate='all', validatecommand=(ok_rack_command, self, '%P'))
		self.rack_entry.grid(columnspan=4, row=n, column=4, sticky=tk.W)
		self.rack_entry.bind('<Up>', self.on_rack_key_press)
		self.rack_entry.bind('<Return>', self.find_moves)
		
		#Find moves button
		self.find_moves_button = tk.Button(self, text='Find moves',width=10,\
				justify=tk.CENTER, command=self.find_moves)
		self.find_moves_button.grid(columnspan=4, row=n, column=8,sticky=tk.W)
	
		#Perform moves button
		self.perform_button = tk.Button(self, text='Use selected move', width = 18,\
				justify=tk.CENTER, command = self.perform_selected_move)
		self.perform_button.grid(columnspan=1, row=n, column=n)

		self.listbox = tk.Listbox(self, selectmode=tk.BROWSE, height=24)
		self.listbox.grid(rowspan=n, row=0, column=n)
		self.listbox.bind('<<ListboxSelect>>', self.on_list_select)

		#Import board button
		self.import_board_button = tk.Button(self, text='Import board', width=12,\
				justify=tk.CENTER, command=self.import_board)
		self.import_board_button.grid(columnspan=4, row=n+1, column=0, sticky=tk.W)

		#Download board button
		self.save_board_button = tk.Button(self, text='Save board', width=12,\
				justify=tk.CENTER, command=self.save_board)
		self.save_board_button.grid(columnspan=4, row=n+1, column=4, sticky=tk.W)

	def render_board_grid(self):
		n = self.board.size
		for i in range(n):
			for j in range(n):
				e = self.squares[i][j]
				e.select_range(0, tk.END)
				e.select_clear()
				e.insert(0, self.board.grid[i][j])

class FileEntryDialog(tkSimpleDialog.Dialog):
	def body(self, master):
		tk.Label(master, text="Enter file name:").grid(row=0)
		self.e = tk.Entry(master)
		self.e.grid(row=0, column=1)
		return self.e

	def apply(self):
		filename = self.e.get()
		self.result = filename

def main():
	try:
		print "Retrieving word trie"
		trie = pickle.load(open(TRIE_FILENAME,"rb"))
	except:
		trie = WordTrie.build_trie_from_filename(WORDLIST_FILENAME)
		print "Retrieval failed, building trie from word list"
		pickle.dump(trie, open(TRIE_FILENAME, "wb")) #Save pickle file
	board = Board(trie)
	root = tk.Tk()
	app = App(root, board)
	app.master.title('Words With Friends Assistant')
	app.mainloop()

if __name__ == "__main__": main()
