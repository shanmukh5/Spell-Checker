class TrieNode:
	def __init__(self):
		self.key = None
		self.valuePointers={}
   
class Trie_Mod:
	
	def __init__(self):
		self.root = TrieNode()
		self.MAX_OPS = 3
		
	def insert(self, word):
		self.rec_insert(word, self.root)
		return
			
	def rec_insert(self, word, node):
		if word[:1] not in node.valuePointers:
			newNode=TrieNode()
			newNode.key=word[:1]
			node.valuePointers[word[:1]]=newNode
			self.rec_insert(word, node)
		else:
			nextNode = node.valuePointers[word[:1]]
			if len(word[1:])==0:
				nextNode.valuePointers[' ']='WORD_END'
				return
			return self.rec_insert(word[1:], nextNode)
			
	def search(self, word):
		if len(word)==0:
			return False
		return self.rec_search(word,self.root)
	
	def rec_search(self, word, node):
		if word[:1] not in node.valuePointers:
			return False
		else:
			nextNode = node.valuePointers[word[:1]]
			if len(word[1:])==0:
				if ' ' in nextNode.valuePointers:
					return True
				else:
					return False
			return self.rec_search(word[1:],nextNode)

	def find(self, word):
		self.found = set()
		buff = ''
		self.findSub(word, self.root, 0, buff)
		self.findIns(word, self.root, 0, buff)
		self.findDel(word, self.root, 0, buff)
		return self.found

	def findSub(self, word, node, ops, buff):
		if ops != self.MAX_OPS:
			if len(word[1:])==0:
				for x in node.valuePointers:
					if x != ' ':
						if x != word[:1]: 
							nextNode = node.valuePointers[x]
							if ' ' in nextNode.valuePointers:
								self.found.add(buff + x)
			else:	
				for x in node.valuePointers:
					if x != ' ':
						if word[:1] == x:
							self.findSub(word[1:], node.valuePointers[x], ops, buff + x)
						else:
							if self.rec_search(word[1:], node.valuePointers[x]):
								self.found.add(buff + x + word[1:])
							self.findSub(word[1:], node.valuePointers[x], ops + 1, buff + x)
							if ops+1 != self.MAX_OPS:
								self.findIns(word[1:], node.valuePointers[x], ops + 1, buff + x)
								self.findDel(word[1:], node.valuePointers[x], ops + 1, buff + x)			

	def findIns(self, word, node, ops, buff):
		if ops != self.MAX_OPS:
			if len(word[1:])==0:
				if word[:1] in node.valuePointers:
					nextNode = node.valuePointers[word[:1]]
					for x in nextNode.valuePointers:
						if x != ' ':
							if self.rec_search(x, nextNode):
								self.found.add(buff + word[:1] + x)
							self.findIns(x, nextNode, ops + 1, buff + word[:1])
							if ops+1 != self.MAX_OPS:
								self.findSub(x, nextNode, ops + 1, buff + word[:1])
								self.findDel(x, nextNode, ops + 1, buff + word[:1])
				for x in node.valuePointers:
					if x != ' ':
						if self.rec_search(word, node.valuePointers[x]):
							self.found.add(buff + x + word)
						self.findIns(word, node.valuePointers[x], ops + 1, buff + x)
						if ops+1 != self.MAX_OPS:
							self.findDel(word, node.valuePointers[x], ops + 1, buff + x)			
							self.findSub(word, node.valuePointers[x], ops + 1, buff + x)	
			else:
				if word[:1] in node.valuePointers:
					self.findIns(word[1:], node.valuePointers[word[:1]], ops, buff + word[:1])		
				for x in node.valuePointers:
					if x != ' ':
						if self.rec_search(word, node.valuePointers[x]):
							self.found.add(buff + x + word)	
						self.findIns(word, node.valuePointers[x], ops + 1, buff + x)
						if ops+1 != self.MAX_OPS:
							self.findDel(word, node.valuePointers[x], ops + 1, buff + x)	
							self.findSub(word, node.valuePointers[x], ops + 1, buff + x)				

	def findDel(self, word, node, ops, buff):
		if ops != self.MAX_OPS:
			if len(word[1:])==0:
				if ' ' in node.valuePointers:
					self.found.add(buff)	
			else:
				if word[:1] in node.valuePointers:
					self.findDel(word[1:], node.valuePointers[word[:1]], ops, buff + word[:1])
				if self.rec_search(word[1:], node):
					self.found.add(buff + word[1:])	
				self.findDel(word[1:], node, ops + 1, buff)
				if ops+1 != self.MAX_OPS:
					self.findIns(word[1:], node, ops + 1, buff)
					self.findSub(word[1:], node, ops + 1, buff)		
					
					
											