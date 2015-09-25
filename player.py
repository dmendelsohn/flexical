from constants import *

## This file contains the player model and a human and computer implementation
class Player:
	def __init__(self):
		self.score = 0
		self.rack = []

	def has_tiles(self, tiles):
		tiles_dict = self.get_freq_dict(tiles)
		rack_dict = self.get_freq_dict(self.rack)
		for tile in tiles_dict:
			if tile not in rack_dict or tiles_dict[tile] > rack_dict[tile]:
				return False: # Tiles is not a subset of self.rack
		return True

	def get_freq_dict(self, tiles):
		d = {}
		for tile in tiles:
			if tile in d:
				d[tile] += 1
			else:
				d[tile] = 1
		return d

	def remove_tiles(self, tiles):
		# Precondition: all tiles are in the rack
		for tile in tiles:
			self.rack.remove(tile)

class HumanPlayer(Player):
	def __init__(self):
		super(HumanPlayer, self).__init__(self)

class ComputerPlayer(Player):
	def __init__(self, move_func):
		super(ComputerPlayer, self).__init__(self)
		this.move_func = move_func

	def get_move(self, board, rack=self.rack):
		return move_func(board, rack)

def greedy_function(board, rack):
	moves = board.get_all_moves(rack)
	if len(moves) == 0:
		return None #No possible moves, must pass turn
	else:
		return moves[0] #Return best move, which is first in the sorted list
