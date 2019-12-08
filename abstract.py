from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx, sys


def summary(text, n = 5):
	stop = stopwords.words('english')
	text_summary = list()
	splitted_text = splitting(text)

	get_sentence_similarity_matrix = text_similarity_matrix(splitted_text, stop)

	similarity_graph = nx.from_numpy_array(get_sentence_similarity_matrix)
	scoring = nx.pagerank(similarity_graph)

	sentences_indexed = sorted(((scoring[i], score) for i, score in enumerate(splitted_text)), reverse=True)
	print(len(sentences_indexed))
	#print("Sentences after being ranked : ", sentences_indexed)
	if len(sentences_indexed) < n:
		n = len(sentences_indexed)
	
	for i in range(n):
		text_summary.append(" ".join(sentences_indexed[i][1]))

	print("Text Summary: \n", ". ".join(text_summary))

	open('summary.txt', 'w').write(str(text_summary))


def splitting(splitted_text):
	
	lines = list()

	for line in splitted_text:
		#print(line)
		lines.append(line.replace("[^a-zA-Z]", " ").split(" "))

	return lines

def text_similarity_matrix(splitted_text, stop):
	matrix = np.zeros((len(splitted_text), len(splitted_text)))

	for i in range(len(splitted_text)):
		for j in range(len(splitted_text)):
			if not i == j:
				matrix[i][j] = finding_similarity(splitted_text[i], splitted_text[j], stop)
			else:
				continue

	return matrix


def finding_similarity(line1, line2, stop=None):
	if stop is None:
		stop = list()

	line1 = [word.lower() for word in line1]
	line2 = [word.lower() for word in line2]

	all_words = list(set(line1 + line2))

	check1 = [0] * len(all_words)
	check2 = [0] * len(all_words)

	for word in line1:
		if word in stop:
			continue
		check1[all_words.index(word)] += 1

	for word in line2:
		if word in stop:
			continue
		check2[all_words.index(word)] += 1

	return 1 - cosine_distance(check1, check2)

file = sys.argv[1]
print(file)
text = open(file, 'r')
textdata = text.readlines()
summary(textdata, n=6)
