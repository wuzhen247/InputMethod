# coding: utf-8
from util import __pinyin 
class Node(object):
	"""docstring for Node"""

	def __init__(self, char):
		self.char = char
		self.set_freq(0)
		self.set_root(False)
		self.set_end(False)
		self.children = dict()

	def set_freq(self, freq):
		self.freq = freq

	def set_root(self, is_root):
		self.is_root = is_root
	
	def set_end(self, is_end):
		self.is_end = is_end

	def get_freq(self):
		return self.freq

	def get_root(self):
		return self.is_root

	def get_end(self):
		return self.is_end

	def add_child(self, child_node):
		self.children[child_node.get_char()] = child_node

	def get_child(self, char):
		return self.children.get(char)

	def get_char(self):
		return self.char

class DictTree(object):
	"""docstring for DictTree"""
	#_pinyin_dir = './data/pinyin'
	_pinyin_dir = './IME/data/pinyin'
	
	def __init__(self):
		super(DictTree, self).__init__()
		self.root = Node('<ROOT>')
		with open(DictTree._pinyin_dir) as py_f:
			py = py_f.read().strip()
			self.pinyin = eval(py)
		for py in self.pinyin:
			self.insert_word(py)

	def insert_word(self, word):
		cur_node = self.root
		for ii, char in enumerate(word):
			if cur_node.get_child(char):
				if ii == len(word) - 1:
					end_node = cur_node.get_child(char)
					end_node.set_end(True)
					end_node.set_freq(end_node.get_freq() + 1)
			else:
				new_node = Node(char)
				if ii == len(word) - 1:
					new_node.set_root(False)
					new_node.set_end(True)
					new_node.set_freq(1)

				cur_node.add_child(new_node)

			cur_node = cur_node.get_child(char)

	def search_freq(self, word):
		freq = -1

		cur_node = self.root
		for ii, char in enumerate(word):
			if cur_node.get_child(char):
				cur_node = cur_node.get_child(char)
				freq = cur_node.get_freq()
			else:
				freq = -1
				break

		return freq

	def split_pinyin(self, seq):
		cur_node = self.root
		seq += '\n'
		ret_seq = []
		cur_pinyin = ''
		ii = 0
		while ii < len(seq):
			char = seq[ii]
			if cur_node.get_child(char):
				cur_pinyin += char
				cur_node = cur_node.get_child(char)
				ii += 1
			else:
				if char == '\'' : 
					ii += 1
				elif not self.root.get_child(char):
					#return False
					return ret_seq

				if cur_node.get_end():
					ret_seq.append(cur_pinyin)
				else:
					#return False
					return ret_seq

				cur_node = self.root
				cur_pinyin = ''

		return ret_seq

if __name__ == '__main__':
	tree = DictTree()
	print "ha'ha", tree.split_pinyin("ha'ha")
	print "xi'an", tree.split_pinyin("xi'an")
	print "xi4an", tree.split_pinyin("xi4an")
	print "jomang", tree.split_pinyin("jomang")
	print ":D", tree.split_pinyin("rinidayecaonimalegebi")