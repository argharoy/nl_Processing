def parse(sentence):
	
	from corenlp import StanfordCoreNLP

	parser = StanfordCoreNLP()

	data = parser.parse(sentence)
	#print data
	
	open_file = open("data.json","wb")

	open_file.write(data)

	open_file.close()