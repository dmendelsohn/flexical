WORDLIST_FILENAME = "wwf.txt"
TRIE_FILENAME = "trie.p"

BOARDSIZE = 15
RACKSIZE = 7

BINGO_BONUS = 35
BONUS_DICT = {(0,3):'tw', (0,6):'tl', (0,8):'tl', (0,11):'tw',\
		(1,2):'dl', (1,5):'dw', (1,9):'dw', (1,12):'dl',\
		(2,1):'dl', (2,4):'dl', (2,10):'dl', (2,13):'dl',\
		(3,0):'tw', (3,3):'tl', (3,7):'dw', (3,11):'tl', (3,14):'tw',\
		(4,2):'dl', (4,6):'dl', (4,8):'dl', (4,12):'dl',\
		(5,1):'dw', (5,5):'tl', (5,9):'tl', (5,13):'dw',\
		(6,0):'tl', (6,4):'dl', (6,10):'dl', (6,14):'tl',\
		(7,3):'dw', (7,11):'dw',\
		(8,0):'tl', (8,4):'dl', (8,10):'dl', (8,14):'tl',\
		(9,1):'dw', (9,5):'tl', (9,9):'tl', (9,13):'dw',\
		(10,2):'dl', (10,6):'dl', (10,8):'dl', (10,12):'dl',\
		(11,0):'tw', (11,3):'tl', (11,7):'dw', (11,11):'tl', (11,14):'tw',\
		(12,1):'dl', (12,4):'dl', (12,10):'dl', (12,13):'dl',\
		(13,2):'dl', (13,5):'dw', (13,9):'dw', (13,12):'dl',\
		(14,3):'tw', (14,6):'tl', (14,8):'tl', (14,11):'tw'}

DOUBLE_LETTER = 'dl'
TRIPLE_LETTER = 'tl'
DOUBLE_WORD = 'dw'
TRIPLE_WORD = 'tw'

EMPTY_SQUARE_CHAR = ''
DOUBLE_LETTER_CHAR = '\''
TRIPLE_LETTER_CHAR = '\"'
DOUBLE_WORD_CHAR = '-'
TRIPLE_WORD_CHAR = '='
UNUSED_BLANK_CHAR = '?'

LOWER_CASE_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
UPPER_CASE_LETTERS = LOWER_CASE_LETTERS.upper()
VALUES_DICT = {UNUSED_BLANK_CHAR:0, 'a':1, 'b':4, 'c':4, 'd':2, 'e':1, 'f':4, 'g':3, 'h':3,\
		'i':1, 'j':10, 'k':5, 'l':2, 'm':4, 'n':2, 'o':1, 'p':4, 'q':10, 'r':1, 's':1,\
		't':1, 'u':2, 'v':5, 'w':4, 'x':8, 'y':3, 'z':10}
for l in UPPER_CASE_LETTERS:
	VALUES_DICT[l] = 0

DEFAULT_TEXT_COLOR = '#000000'
PREVIEW_TEXT_COLOR = '#707070'
BONUS_COLORS = {DOUBLE_LETTER: '#8090FF',\
		TRIPLE_LETTER: '#40FF40',\
		DOUBLE_WORD: '#FF0000',\
		TRIPLE_WORD: '#FFA500'}


