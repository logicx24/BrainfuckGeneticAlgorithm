from sys import *
import os.path
import time
from datetime import datetime, timedelta

class BrainFuckException(object):

	def throw(self, message):
		print(message)
		exit()

class Brainfuck(object):

	def __init__(self, arraySize=300):
		self.valid_symbols = ['+', '-', '>', '<', '.', ',', '[', ']', '*']
		self.arraySize = arraySize
		self.programArray = [0]*self.arraySize
		self.counter = 0
		self.code_dict = self.functions()
		self.exceptionObj = BrainFuckException()

		self.input = []
		self.inp_i = 0
		self.output = []

	def setCode(self, string):
		self.code = self.filterCode(string)

	def setInp(self, lst):
		self.input = lst

	def setFileCode(self, filename):
		self.code = self.filterCode(open(filename, 'r').read())

	def expandProgramArray(self):
		self.programArray.extend([0]*1000)

	def filterCode(self, code):
		return "".join(char for char in code.replace(" ", "") if char in self.valid_symbols)

	def incrementCounter(self):
		self.counter += 1

		if self.counter >= len(self.programArray):
			self.expandProgramArray()

	def decrementCounter(self):
		if self.counter > 0:
			self.counter -= 1
		if self.counter >= len(self.programArray):
			self.expandProgramArray()

	def incrementDeref(self):
		if self.counter >= len(self.programArray):
			self.expandProgramArray()
		self.programArray[self.counter] += 1

	def decrementDeref(self):
		if self.counter >= len(self.programArray):
			self.expandProgramArray()
		self.programArray[self.counter] -= 1

	def addOutput(self):
		if self.counter >= len(self.programArray):
			self.expandProgramArray()
		try:
			self.output.append(str(chr(self.programArray[self.counter])))
		except ValueError:
			self.output.append(str(self.programArray[self.counter]))

	def syntaxErrors(self):
		stack = []
		stackList = ['[']
		stackHash = {']':'['}
		for i in range(len(self.code)):
			letter = self.code[i]
			if letter in stackList:
				stack.insert(0, letter)
			elif letter in stackHash:
				if len(stack) == 0:
					return True
				elif stack.pop(0) != stackHash[letter]:
					return True
		if len(stack) != 0:
			return True
		return False

	def commaFunc(self):
		# print('Please enter a single character below.')
		# userInput = input()
		# if len(userInput) > 1:
		# 	self.exceptionObj.throw('Only enter one character to the input.')
		if self.inp_i >= len(self.input):
			return
		self.programArray[self.counter] = self.input[self.inp_i]
		if self.inp_i < len(self.input):
			self.inp_i += 1

	def functions(self):
		code_dict = {
			'.' : lambda : self.addOutput(),
			'>' : lambda : self.incrementCounter(),
			'<' : lambda : self.decrementCounter(),
			'+' : lambda : self.incrementDeref(),
			'-' : lambda : self.decrementDeref(),
			',' : lambda : self.commaFunc(),
			'*' : lambda : print(self.programArray[self.counter])
		}
		return code_dict

	def reset(self):
		self.programArray = [0]*self.arraySize
		self.counter = 0
		self.output = []
		self.input = []
		self.inp_i = 0		

	def loopIndex(self):
		counterToIndex = {}
		loopNumber = 0
		openToClosing = {}
		closingToOpening = {}
		for index, char in enumerate(self.code):
			if char == "[":
				loopNumber += 1
				counterToIndex[loopNumber] = index
			elif char == "]":
				if loopNumber in counterToIndex:
					openToClosing[counterToIndex[loopNumber]] = index
					closingToOpening[index] = counterToIndex[loopNumber]
				loopNumber -= 1
		return openToClosing, closingToOpening

	def executeCode(self, time_limit=1):
		# if self.syntaxErrors():
		# 	#self.output += ["ZZZZZZZZZZZZZZZZZZ"]
		# 	return
		loopHashForward, loopHashBackward = self.loopIndex()
		i = 0

		start = time.time()#datetime.fromtimestamp(time.time())
		while i < len(self.code):
			char = self.code[i]
			if char in self.code_dict:
				self.code_dict[char]()
				i += 1
			elif char == '[':
				if self.programArray[self.counter] == 0:
					if i not in loopHashForward:
						return
					i = loopHashForward[i] + 1
				else:
					i += 1
			elif char == ']':
				if self.programArray[self.counter] == 0:
					i += 1
				else:
					if i not in loopHashBackward:
						return
					i = loopHashBackward[i] + 1
			else:
				i += 1
			# print(self.output)

			end = time.time()#datetime.fromtimestamp(time.time())
			if (end - start) > time_limit:
				#self.output = ["ZZZZZZZZZZZZZZZZZZ11"]
				return
			
	def runProgram(self, code, inp=[]):
		self.reset()
		self.setCode(code)
		self.setInp(inp)
		self.executeCode()

		if len(self.output) > 0:
			outstr = "".join(self.output).strip()
			if len(outstr) > 0:
				return outstr

	def repl(self):
		while True:
			self.reset()
			self.setCode(input("> "))
			self.executeCode()
			print("".join(self.output[:100]))

if __name__ == "__main__":
	brainfuck = Brainfuck()
	if len(argv) == 1:
		brainfuck.repl()
	elif len(argv) >= 2:
		if os.path.isfile(argv[1]):
			brainfuck.setFileCode(argv[1])
			brainfuck.executeCode()
		else:
			print("This file does not exist. Check your path.")

