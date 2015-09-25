from constants import *

## CODE FOR THE TRIE DATA STRUCTURE ##
class WordTrie:
	def __init__(self, is_terminal):
		self.is_terminal = is_terminal
		self.edges = {}
		self.size = 1
		self.numwords = 0
		if is_terminal:
			self.numwords += 1
	def get_size(self):
		return self.size
	def get_numwords(self):
		return self.numwords
	def add_edge(self, char, subtrie):
		self.edges[char] = subtrie
		self.size += subtrie.get_size()
		self.numwords += subtrie.get_numwords()
	def get_edge(self, char):
		if char in self.edges:
			return self.edges[char]
		else:
			return None
	def check_word(self, word):
		if len(word) == 0:
			return self.is_terminal
		else:
			l = word[0].lower() #Convert everything to lower case
			return (l in self.edges and self.edges[l].check_word(word[1:]))
	def get_subtrie(self, word): #Returns the node for word, or None if none exists
		if len(word) == 0:
			return self
		l = word[0].lower()
		if l in self.edges:
			return self.edges[l].get_subtrie(word[1:])
		else:
			return None

	@staticmethod
	def build_trie_from_filename(filename):
		wordlist = WordTrie.generate_word_list(filename)
		trie = WordTrie.build_trie(wordlist)
		return trie

	@staticmethod
	def build_trie(wordlist):
		return WordTrie.build_subtrie(wordlist, 0, "")[0]

	@staticmethod
	def build_subtrie(wordlist, start_index, prefix):
		# Returns a tuple of the form (subtrie, size)
		# "subtrie" is WordNode object reached by input prefix in the DFA
		# "numwords" = # of terminal nodes in the subtrie, including root
		# If there are no words with this prefix, returns (None, 0)
		# Start_index should be index of the first word in with that prefix
		## if one exists
		index = start_index
		if index >= len(wordlist) or not wordlist[index].startswith(prefix):
			return (None, 0) #There is no word with this prefix
	
		if wordlist[index] == prefix:
			trie = WordTrie(True) # This is a terminal node
			numwords = 1
		else:
			trie = WordTrie(False) # This isn't a terminal node
			numwords = 0
			
		for char in LOWER_CASE_LETTERS:
			(subtrie, subnumwords) = \
				WordTrie.build_subtrie(wordlist,index+numwords,prefix+char)
			if subtrie != None:
				trie.add_edge(char, subtrie)
				numwords += subnumwords

		return (trie, numwords)

	@staticmethod
	def generate_word_list(filename,verbose=False):
		f = open(filename)
		wordlist = []
		word = f.readline()
		while (word != ''):
			wordlist.append(word.strip())
			word = f.readline()
	
		if verbose:
			wordlengths = {}
			for word in wordlist:
				length = len(word)
				if length in wordlengths:
					wordlengths[length] += 1
				else:
					wordlengths[length] = 1
			print "Total # of words: " + str(len(wordlist))
			print "Distribution by length: " + str(wordlengths)
			print "Longest word is: " + max(wordlist, key=len)

		return wordlist


