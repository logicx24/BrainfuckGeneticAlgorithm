from brainfuck import Brainfuck
import random
import pdb

class GeneticAlg(object):

	def __init__(self, mutationRate, crossoverRate, generationCnt, basePop, baseLen):
		self.mutationRate = mutationRate
		self.crossoverRate = crossoverRate
		self.generations = generationCnt
		self.bf = Brainfuck()
		self.symbols = ['+', '-', '>', '<', '.', '[', ']']
		self.desiredOutput = "Hello Me!"
		self.sampleInput = []
		self.basePop = basePop
		self.baseLen = baseLen

	# def setVars(self, out, in):
	# 	self.desiredOutput = out
	# 	self.sampleInput = []

	def initGen(self):
		out = []
		for _ in range(self.basePop*4):
			curr = []
			for i in range(self.baseLen):
				curr.append(random.choice(self.symbols))
			out.append("".join(curr))
		return out

	def crossover(self, code1, code2):
		return self.two_point_crossover(code1, code2)

	def one_point_crossover(self, code1, code2):
		split_point = random.randint(0, min(len(code1), len(code2)))
		# if isinstance(code1, tuple):
		# 	print(code1)
		# if isinstance(code2, tuple):
		# 	print(code2)
		return code1[:split_point] + code2[split_point:], code2[:split_point] + code1[split_point:]

	def two_point_crossover(self, code1, code2):
		split_point1 = random.randint(0, min(len(code1), len(code2)))
		split_point2 = random.randint(0, min(len(code1), len(code2)))		
		while split_point1 == split_point2:
			split_point2 = random.randint(0, min(len(code1), len(code2)))

		c1 = code1[:split_point1] + code2[split_point1:split_point2] + code1[split_point2:]
		c2 = code2[:split_point1] + code1[split_point1:split_point2] + code2[split_point1:]

		return c1, c2

	def in_mutate(self, code):
		rand = random.randint(0, len(code))
		return code[:rand] + random.choice(self.symbols) + code[rand:]

	def sub_mutate(self, code):
		w = list(code)
		w[random.randint(0, len(code) - 1)] = random.choice(self.symbols)
		return "".join(w)

	def del_mutate(self, code):
		rand = random.randint(0, len(code))
		return code[:rand] + code[rand+1:]		

	def fitness(self, output):
		if not output:
			return float("-inf")
		fitness = 0
		# if len(output) < len(self.desiredOutput):
		# 	output += "\x01"*(len(self.desiredOutput) - len(output))
		for i in range(min(len(output), len(self.desiredOutput))):
			fitness += 256 - (abs(ord(output[i]) - ord(self.desiredOutput[i])))
		fitness -= .05*abs(len(output) - len(self.desiredOutput))
		# if len(output) < len(self.desiredOutput):
		# 	fitness -= sum(ord(w) for w in "\x01"*(len(self.desiredOutput) - len(output)))
		# if len(output) > len(self.desiredOutput):
		# 	fitness -= sum([ord(x) for x in output[len(self.desiredOutput):]][50:])
		return fitness

	# def weighted_choice(self, choices):
	# 	total = sum(w for c, w in choices)
	# 	r = random.uniform(0, total)
	# 	upto = 0
	# 	for c, w in choices:
	# 		if upto + w >= r:
	# 			return c
	# 		upto += w
		# choice = random.choice(choices)
		# while random.random() > (choice[1]/total):
		# 	choice = random.choice(choices)
		# return choice

	# def rank_selection(self, size):
	# 	 w = random.randint(0, size-1)
	# 	 i = 1
	# 	 while i <= w

	def pickOne(self, len, totalF):
		randNum = random.random() * totalF;
		i = 1
		while i <= len:
			randNum -= i
			if randNum <= 0:
				return i - 1
			i += 1
		return len - 1


	def runOne(self, pop):
		pop = [(c, w) for c, w in pop if w > float("-inf")]

		nextPop = [pop[-1][0]]
		totalF = (self.basePop * (self.basePop + 1)) / 2

		output_hash = {}
		output_set = set()
		
		while len(nextPop) < self.basePop:#len(pop):
			gene1 = pop[self.pickOne(len(pop), totalF)][0]
			gene2 = pop[self.pickOne(len(pop), totalF)][0]
			while gene1 == gene2:
				gene2 = pop[self.pickOne(len(pop), totalF)][0]

			if random.random() < self.crossoverRate:	
				gene1, gene2 = self.crossover(gene1, gene2)

			for fn in [self.in_mutate, self.sub_mutate, self.del_mutate]:
				if random.random() < self.mutationRate:
					gene1 = fn(gene1)
				if random.random() < self.mutationRate:
					gene2 = fn(gene2)

			to_add = []
			for gene in [gene1, gene2]:
				g_out = self.bf.runProgram(gene, self.sampleInput)
				if g_out and g_out[:len(self.desiredOutput)] not in output_set:
					g_out = g_out[:len(self.desiredOutput)]
					output_set.add(g_out)
					output_hash[gene] = g_out
					to_add.append(gene)

			nextPop.extend(to_add)
#			nextPop.extend([gene1, gene2])

		return sorted([(c, self.fitness(output_hash[c])) for c in nextPop], key=lambda x: x[1])

	def run(self):
		pop = [(c, self.fitness(c)) for c in self.initGen() + ["++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."]]
		best_code = max(pop, key=lambda x: x[1])[0]
		print(pop)
		i = 0
		while self.bf.runProgram(best_code) != self.desiredOutput and i < self.generations:
			#pdb.set_trace()
			pop = self.runOne(pop)
			best_code, w = pop[-1]#max(pop, key=lambda x: x[1])
			print("-------------------------")
			print(pop) 
			print(best_code)
			print(w)
#			print(self.bf.runProgram(best_code))
			print("-------------------------")
			i += 1

		return best_code

def fitness(output, desiredOutput):
	fitness = 0
	for i in range(min(len(output), len(desiredOutput))):
		fitness += (256 - abs(ord(output[i]) - ord(desiredOutput[i])))
	return fitness


if __name__ == "__main__":
	galg = GeneticAlg(0.05, 0.95, 1000, 20, 40)
	print(galg.run())

 


