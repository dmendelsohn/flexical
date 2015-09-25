from constants import *

## This is the object that runs the game
class GameEngine:
	def __init__(self, players):
		self.tilebag = DEFAULT_TILEBAG
		self.players = players
		for player in players:
			self.fill_player_rack(player)
			self.fill_player_rack(player)
		self.curplayer = 0
		self.num_players = len(players)
		self.consecutive_passed_turns = 0
		self.played_moves = [[] for p in players] #For each player, a list of moves
		self.is_game_over = False

	def current_player(self):
		return self.players[self.curplayer]
	def draw_from_bag(self):
		#Removes a random tile from bag and returns it, returns None if no tiles left
		if len(self.tilebag) == 0:
			return None
		else:
			return self.tilebag.pop(random.randrange(len(self.tilebag)))

	def fill_player_rack(self, player):
		while (len(tilebag) > 0 and len(player.rack) < RACKSIZE):
			tile = self.draw_from_bag()
			player.rack.append(tile)

	def play_move(self, move):
		# The 'score' field is ignored and recalculated
		# move == None passes the current player's turn
		# Returns True iff the proposed move is playable by current player
		player = self.current_player()
		if move == None:
			self.played_moves[self.curplayer].append(move) # Log move
			self.increment_curplayer()
			self.consecutive_passed_turns += 1
			if self.consecutive_passed_turns > self.num_players: # Game over
				self.end_game()
			return True
		elif self.valid_move(move, player):
			self.played_moves[self.curplayer].append(move) # Log move
			move_score = board.get_move_score(move)
			self.current_player().score += move_score # Add to player's total
			tiles_to_play = board.get_tiles_required(move)
			player.remove_tiles(tiles_to_play) # Remove tiles from player's rack
			board.play_move(move) # Update the board data structure
			self.fill_player_rack(player) # Refill the player's rack
			self.increment_curplayer() # Next player's turn
			if len(self.tilebag) == 0: # We're out of tiles
				self.end_game()
			return True
		else:
			return False # Not a valid move

	def valid_move(self, move, player):
		if move == None:
			return True
		if not board.is_valid_move(move):
			return False
		tiles_to_play = board.get_tiles_required(move) #List of tiles required for move
		return player.has_tiles(tiles_to_play)

	def increment_curplayer(self):
		self.curplayer += 1
		self.curplayer %= self.num_players

	def end_game(self):
		self.is_game_over = True
		winning_player = max(self.players, key=lambda p: p.score) #DEBUG, this is prob wrong
		winning_index = self.players.index(winning_player)
		print 'Player %d has won with a score of %d points!' \
				% (winning_index, winning_player.score)
		#TODO: write results to file and whatnot
