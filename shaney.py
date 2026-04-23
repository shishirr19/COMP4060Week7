#!/usr/bin/python 
import os, sys, string, random

# Markov chain word generator.

def build(contexts, words, n):
	context = words[:n]
	for word in words[n:]:
		key = tuple(context)
		wordfreq = contexts.get(key, {})
		wordfreq[word] = wordfreq.get(word, 0) + 1
		contexts[key] = wordfreq
		context = context[1:] + [word]
		
def generate(f, starters, contexts):
	context = random.choice(starters)

	word_count = 0
	paragraph_size = 50

	f.write(" ".join(context).upper())
	word_count += len(context)

	while True:
		key = tuple(context)
		wordfreq = contexts.get(key, {})
		if not wordfreq:
			break

		word = choose(wordfreq).upper()
		f.write(" " + word)
		word_count += 1

		if word_count >= paragraph_size:
			f.write("\n\n")
			word_count = 0

		context = context[1:] + [word.lower()]

	f.write("\n")

def choose(wordfreq):
	total = 0
	for w, count in wordfreq.items():
		total += count

	chosen = random.randint(1, total)

	sofar = 0
	for word, count in wordfreq.items():
		sofar += count
		if chosen <= sofar:
			return word

	assert(0)

def main():
	data_dir = "data/"
	n = 2
	for arg in sys.argv[1:]:
		if arg.isnumeric(): 
			n = int(arg)
		else: 
			data_dir = arg

	contexts = {}
	starters = []

	for filename in sorted(os.listdir(data_dir)):
		print("Reading " + data_dir + filename)
		f = open(data_dir + filename, encoding="utf-8")
		words = f.read().split()
		starters.append(words[:2])
		build(contexts, words, 2)

	out_file = "output.txt"
	print("Writing " + out_file)
	f = open(out_file, "w", encoding="utf-8")

	for _ in starters:
		generate(f, starters, contexts)
		f.write("\n")

	f.close()

if __name__ == '__main__':
	main()