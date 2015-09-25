from constants import *

## CODE FOR BOARD DATA STRUCTURE ##
class Board:
	def __init__(self, trie):
		self.size = BOARDSIZE
		#By convention, first index is row number, second is column number
		self.grid = [[EMPTY_SQUARE_CHAR for i in range(self.size)] for j in range(self.size)]
		self.bonuses = BONUS_DICT
		self.trie = trie
	def set_tile(self, row, col, tile):
		self.grid[row][col] = tile
	def clear_tile(self, row, col): #also returns the removed tile
		tile = self.grid[row][col]
		self.grid[row][col] = EMPTY_SQUARE_CHAR
		return tile
	def get_tile(self, row, col):
		return self.grid[row, col]
	def transpose(self): # Transposes the board
		self.grid = [[j[i] for j in self.grid] for i in range(len(self.grid))]
	def is_valid_square(self, i, j):
		return i >= 0 and j >= 0 and i < self.size and j < self.size
	def is_empty_square(self, i, j):
		return self.is_valid_square(i,j) and self.grid[i][j] == EMPTY_SQUARE_CHAR
	def is_occupied_square(self, i, j):
		return self.is_valid_square(i,j) and self.grid[i][j] != EMPTY_SQUARE_CHAR
	def is_anchor(self, i, j): # True if this square is empty and an adjacent one is occupied
		is_neighbor_occupied = self.is_occupied_square(i+1,j) or \
				self.is_occupied_square(i-1,j) or \
				self.is_occupied_square(i,j+1) or \
				self.is_occupied_square(i,j-1)
		return is_neighbor_occupied and self.is_empty_square(i,j)
	def get_anchor_grid(self): # Returns a size by size 2D array of booleans
		grid = [[self.is_anchor(i,j) for j in range(self.size)] for i in range(self.size)]
		if not any(map(any, grid)): # This must be the first move, make middle an anchor
			mid = self.size/2
			grid[mid][mid] = True
		return grid
	def get_crosscheck(self, i, j): #Returns list of 1-char strings indicating valid crosses
		crosses = []
		if not self.is_empty_square(i,j):
			return crosses # Out of bounds or occupied squares have no valid crosses
		top_part = ''
		iprime = i-1
		while self.is_occupied_square(iprime,j):
			top_part = self.grid[iprime][j] + top_part
			iprime -= 1
		bottom_part = ''
		iprime = i+1
		while self.is_occupied_square(iprime,j):
			bottom_part += self.grid[iprime][j]
			iprime += 1
		for l in LOWER_CASE_LETTERS:
			crossword = top_part + l + bottom_part
			if self.trie.check_word(crossword) or len(crossword) == 1:
				crosses.append(l)
		return crosses
	def get_crosscheck_grid(self, trie):
		return [[self.get_crosscheck(i,j) for j in range(self.size)] for i in range(self.size)]
	def get_cross_score(self, i, j, letter): 
		# Return the sum of tiles contiguous to this square, vertically
		# Return 0 if the space isn't a valid empty square
		if not self.is_empty_square(i,j):
			return 0
		is_cross = self.is_occupied_square(i+1,j) or self.is_occupied_square(i-1,j)
		if not is_cross:
			return 0 #If no adjacent letters, cross score should be 0
		total = VALUES_DICT[letter] # Start calculation with tile being placed
		iprime = i-1
		while self.is_occupied_square(iprime,j):
			total += VALUES_DICT[self.grid[iprime][j]]
			iprime -= 1
		iprime = i+1
		while self.is_occupied_square(iprime,j):
			total += VALUES_DICT[self.grid[iprime][j]]
			iprime += 1
		#Account for bonuses
		if (i,j) in BONUS_DICT:
			if BONUS_DICT[(i,j)] == DOUBLE_LETTER:
				total += VALUES_DICT[letter] # Need to count score one more time
			elif BONUS_DICT[(i,j)] == TRIPLE_LETTER:
				total += 2*VALUES_DICT[letter] # Need to count score two more times
			elif BONUS_DICT[(i,j)] == DOUBLE_WORD:
				total *= 2
			elif BONUS_DICT[(i,j)] == TRIPLE_WORD:
				total *=3
		return total
	def get_left_part_limit(self, i, j): # Returns the number of empty non-anchors left given square
		k = 0
		jprime = j-1
		while self.is_empty_square(i,jprime) and not self.is_anchor(i,jprime):
			k += 1
			jprime -= 1
		return k
	def get_existing_left_part(self, i, j):
		jprime = j-1
		word = ''
		while self.is_occupied_square(i,jprime):
			word = self.grid[i][jprime] + word
			jprime -= 1
		return word
	def left_part(self, rack, partial_word, trie, limit, i, j): #LeftPart as described in the paper
		moves = self.right_part(rack, partial_word, trie, i, j, True)
		if limit > 0:
			for l in trie.edges:
				if l in rack:
					rack.remove(l)
					subtrie = trie.edges[l]
					moves += self.left_part(rack, partial_word+l, subtrie, limit-1, i, j)
					rack.append(l)
				if UNUSED_BLANK_CHAR in rack: # Use the blank
					rack.remove(UNUSED_BLANK_CHAR)
					subtrie = trie.edges[l]
					moves += self.left_part(rack, partial_word+l.upper(), subtrie, limit-1, i, j)
					rack.append(UNUSED_BLANK_CHAR)
		return moves
	def right_part(self, rack, partial_word, trie, i, j, initial_call): #as described in the paper
		# Returns list of moves in form (row, col, word_string), assumed to be horizontal
		moves = []
		if self.is_empty_square(i,j):
			if trie.is_terminal and not initial_call:
				moves.append((partial_word, i, j-len(partial_word)))
			for l in trie.edges: #For each letter we can add to the partial word
				if l in self.get_crosscheck(i,j):
					if l in rack:
						rack.remove(l) #Recall rack is a list of single char strings
						subtrie = trie.edges[l]
						moves += self.right_part(rack, partial_word+l, subtrie, i, j+1, False)
						rack.append(l)
					if UNUSED_BLANK_CHAR in rack: # Use blank
						rack.remove(UNUSED_BLANK_CHAR)
						subtrie = trie.edges[l]
						moves += self.right_part(rack, partial_word+l.upper(), subtrie, i, j+1, False)
						rack.append(UNUSED_BLANK_CHAR)
		elif self.is_occupied_square(i,j):
			l = self.grid[i][j]
			if l.lower() in trie.edges:
				subtrie = trie.edges[l.lower()]
				moves += self.right_part(rack, partial_word+l, subtrie, i, j+1, False)
		else: #(i,j) isn't a valid square
			if trie.is_terminal:
				moves.append((partial_word, i, j-len(partial_word)))
		return moves
	def get_moves_from_anchor(self, rack, trie, i, j): 
		#Returns a list of valid moves from a given anchor
		#Pre-condition: space must be anchor (or central space if the board is empty)
		if self.is_occupied_square(i, j-1):
			partial_word = self.get_existing_left_part(i, j)
			subtrie = trie.get_subtrie(partial_word)
			print "partial word = %s" % partial_word
			if subtrie is None: # If partial_word is invalid, we shouldn't add to it
				return []
			return self.right_part(rack, partial_word, subtrie, i, j, True)
		else:
			k = self.get_left_part_limit(i,j)
			return self.left_part(rack, '', trie, k, i, j)
	def get_moves(self, rack):
		moves = [] # Horizontal moves only, still
		anchor_grid = self.get_anchor_grid()
		for i in range(self.size):
			for j in range(self.size):
				if anchor_grid[i][j]:
					moves.extend(self.get_moves_from_anchor(rack, self.trie, i,j))
		moves = self.score_moves(moves) # Calculate the score of each
		return moves
	def get_all_moves(self, rack):
		h_moves = self.get_moves(rack) # Horizontal moves
		self.transpose()
		v_moves = self.get_moves(rack) # Vertial moves
		self.transpose()
		# Add isVertical field to all moves (and swap row/col for vertical ones)
		h_moves = [(word, row, col, score, False) for (word, row, col, score) in h_moves]
		v_moves = [(word, col, row, score, True) for (word, row, col, score) in v_moves]
		moves = h_moves + v_moves
		moves.sort(key=lambda x: x[3], reverse=True)
		return moves
	def score_move(self, move):
		# Augments the (word, row, col) tuple, adding a score field
		multiplier = 1
		cross_score = 0
		word_score = 0
		letters_placed = 0
		word = move[0]
		row = move[1]
		col = move[2]
		j = col
		for l in word:
			letter_score = VALUES_DICT[l]
			# If this is a newly placed tile, do cross_score and bonus calculations
			if self.is_empty_square(row, j):
				cross_score += self.get_cross_score(row,j,l)
				letters_placed += 1
				if (row, j) in BONUS_DICT:
					if BONUS_DICT[(row,j)] == DOUBLE_LETTER:
						letter_score *= 2
					elif BONUS_DICT[(row,j)] == TRIPLE_LETTER:
						letter_score *= 3
					elif BONUS_DICT[(row,j)] == DOUBLE_WORD:
						multiplier *= 2
					elif BONUS_DICT[(row,j)] == TRIPLE_WORD:
						multiplier *= 3
			word_score += letter_score
			j += 1
		score = word_score * multiplier + cross_score
		if letters_placed == RACKSIZE: #If we have a bingo
			score += BINGO_BONUS
		return (word, row, col, score)
	def score_moves(self, moves):
		return [self.score_move(x) for x in moves]
	def __str__(self):
		rep = []
		for i in range(self.size):
			for j in range(self.size):
				if self.grid[i][j] == EMPTY_SQUARE_CHAR:
					if (i,j) not in self.bonuses:
						rep.append(EMPTY_SQUARE_CHAR)
					elif self.bonuses[(i,j)] == DOUBLE_LETTER:
						rep.append(DOUBLE_LETTER_CHAR)
					elif self.bonuses[(i,j)] == TRIPLE_LETTER:
						rep.append(TRIPLE_LETTER_CHAR)
					elif self.bonuses[(i,j)] == DOUBLE_WORD:
						rep.append(DOUBLE_WORD_CHAR)
					elif self.bonuses[(i,j)] == TRIPLE_WORD:
						rep.append(TRIPLE_WORD_CHAR)
				else:	
					rep.append(self.grid[i][j])
				rep.append(' ')
			rep.append('\n')
		rep = rep[:-1] # Because the extra newline at the bottom bothers me
		return ''.join(rep)


