import re
import json
import nlp_parser
import Wernicke
import Broca

element, subs, reference, Q_tokens, St_tokens = ([] for lis in range(5))
eleminate = ["He","he","HE","She","she","SHE","them","Them","it","its","It","It's","His","his","Her","her"]
cp_text = ""



#Functions Definations
#-----------------------------------------------------------------------------------------------------------------------
def assembler(tokens, statement_number, dictionary):
	global Q_tokens
	global St_tokens

	extracted_Ques_tokens = [value for x in tokens for value in x]
	
	if statement_number == 0:
		token_length = len(extracted_Ques_tokens)
		for i  in range(0,token_length):
			Q_tokens.append(extracted_Ques_tokens[i])

	else:
		St_tokens.extend([extracted_Ques_tokens])

def Wernicke_main(text, dictionary, statement_number):
	get_pos = dictionary.keys()[dictionary.values().index(".")]
	#print get_pos
	tokens, Q_Signal = Wernicke.statement_analyzer(dictionary, get_pos, 1)
	if Q_Signal == True:
		assembler(tokens, 0, dictionary)
	elif Q_Signal == False:
		assembler(tokens, statement_number, dictionary)
	else:
		pass
def information_extractor(data_words):
	words,poss = (list() for l in range(2))
	count_dw = len(data_words)
	for counter in range(0,count_dw):
		word = data_words[counter][0]
		p_o_s = data_words[counter][1].get("PartOfSpeech")
		words.append(word)
		poss.append(p_o_s)
	return words,poss

def sentence_sensor():
	zipper_info = dict()
	with open('data.json') as data_file:
		data = json.load(data_file)

	extracted_info = []
	extracted_text = []

	for key in data:
		if key == "sentences":
			count_lists = len(data["sentences"])
			#print count_lists,"\n"
			for i in range(0,count_lists):
				dictionary = data["sentences"][i]
				#print dictionary,"\n"
				data_text = dictionary.get("text")
				#print data_text
				data_words = dictionary.get("words")
				words,poss = information_extractor(data_words)
				#print words," == ",poss
				#print len(words),"!!",len(poss)
				zipper_info = dict(zip(words,poss))
				#print zipper_info
				extracted_info.append(zipper_info)
				extracted_text.append(data_text)
		else:
			pass
	return extracted_text,extracted_info

def sentence_parser():
	with open('data.json') as data_file:
		data = json.load(data_file)

	for key in data:
		if key == "coref":
			list_count = len(data["coref"])
			for i in range(0, list_count):
				#print len(data["coref"][i]
				#print data["coref"][i]
				#print
				data_list_1 = data["coref"][i]
				lc1 = len(data_list_1)
				for j in range(0, lc1):
					data_list_2 = data["coref"][i][j]
					#print data_list_2
					#print
					lc2 = len(data_list_2)
					for k in range(0, lc2-1):
						flag = 0
						data_list_3 = data["coref"][i][j][k]
						if k == 0:
							if eleminate.count(data_list_3[0]) > 0:
								flag = 1
								element.append(data_list_3[0])
								reference.append(data_list_3[1])
							else:
								flag = 0
						if flag == 1:
							subs.append(data["coref"][i][j][k+1][0])
		else:
			pass

#-----------------------------------------------------------------------------------------------------------------------

#text = "Mike has 35 books in his library. He bought several books at a yard sale over the weekend. He now has 56 books in his library. How many books did he buy at the yard sale?"
#text = "Joan found 70 stones on beach. She gave Sam some of her stones. She has 27 stones. Mike has 35 books in his library. He bought several books at a yard sale over the weekend. He now has 56 books in his library. How many books did he buy at the yard sale? How many stones did she give to Sam?"
#text = "There were 28 bales of hay in the barn. Tim stacked bales in the barn today. There are now 54 bales of hay in the barn. How many bales did he store in the barn?"
#text = "There are 22 walnut trees currently in the park. Park workers will plant walnut trees today. When the workers are finished there will be 55 walnut trees in the park. How many walnut trees did the workers plant today? XXXX Future Tense"
#text = "Mike had 34 stones at his roadside fruit dish. He went to the orchard and picked stones to stock up. There are now 86 stones. How many stones did he pick?"
#text = "There were 6 roses in the vase. Mary cut some roses from her flower garden. There are now 16 roses in the vase. How many roses did she cut?"
#text = "There were 32 bales of hay in the barn and 26 bales in the shed. Jason stacked bales in the barn today. There are now 98 bales of hay in the barn. How many bales did he store in the barn? MODE - 3"
#text = "Alyssa 's dog had puppies . She gave 7 to her friends. She now has 5 puppies. How many puppies did she have to start with? - SUPPORTING SUBJECT IN ANSWER SENTENCE AND CONFUSION SENTENCE"
#text = "Dan found 56 seashells on the beach, he gave Jessica some of his seashells. He has 22 seashells. How many seashells did he give to Jessica?"
#text = "Sally had 13 apples at her roadside fruit dish. She went to the orchard and picked apples to stock up . There are now 55 apples. how many apples did she pick ?"
#text = "Benny received 67 dollars for his birthday. He went to a sporting goods store and bought a baseball glove, baseball, and bat . He had 33 dollars over. How much dollars did he spend on the baseball gear? CONFUSION INFORMATION"
#text = "There were 3 roses in the vase. Alyssa cut some roses from her flower garden. There are now 14 roses in the vase. How many roses did she cut?"
#text = "There were 73 bales of hay in the barn. Jason stacked bales in the barn today. There are now 96 bales of hay in the barn. How many bales did he store in the barn?"
#text = "Jason had pokemon cards. He gave 9 cards to his friends. He now has 4 cards. How many Pokemon cards did he have to start with?"
#text = "Last week Fred had 23 dollars and Jason had 46 dollars . Fred washed cars over the weekend and now has 86 dollars. How much dollar did Fred make washing cars ?"
#text = "There are 31 short trees and 32 tall trees currently in the park. Park workers will plant short trees today. When the workers are finished there will be 95 short trees in the park . How many short trees did the workers plant today ?" 
#text = "There were 9 red orchids and 3 white orchids in the vase. Sally cut some red orchids from her flower garden. There are now 15 red orchids in the vase . How many red orchids did she cut ?"
#text = "Joan found 72 seashells and 12 starfishes on the beach. She gave Alyssa some of her seashells. She has 28 seashells. How many seashells did she give to Alyssa ?"
#text = "Sara had 24 peaches and 37 pears at her fruit dish. She went to the orchard and picked peaches . There are now 61 peaches. How many peaches did she pick ?"
#text = "Dan had 14 peaches and 10 pears at his roadside fruit dish. He went to the orchard and picked peaches to stock up . There are now 85 peaches. how many did he pick ? QUESTION INFO MISSING"
#text = "Benny received 79 dollars and 9 movie tickets for his birthday. He went to a sporting goods store and bought a baseball glove , baseball , and bat . He had 32 dollars over, how much did he spent on the baseball gear ? "
#text = "There are 43 maple trees and 22 orange trees currently in the park. Park workers will plant maple trees today . When the workers are finished there will be 54 maple trees in the park. How many maple trees did the workers plant today?"
#text = "Melanie has 41 books and 31 magazines in her library. She bought several books at a yard sale over the weekend. She now has 87 books in her library. How many books did she buy at the yard sale? "
#text = "There were 2 red orchids and 4 white orchids in the vase. Jessica cut some red orchids from her flower garden. There are now 18 red orchids in the vase. How many red orchids did she cut?" 
#@text = "Last week Tom had 74 dollars. He washed cars over the weekend and now has 86 dollars. How much dollars did he make washing cars? QUES_FOR -> DOLLARS CORRECT QUES_FOR MONEY -> WRONG XXXXXXXXXXXXXX"
#text = "Joan found 75 seashells and 14 starfishes on the beach. She gave Tim some of her seashells . She has 62 seashells. How many seashells did she give to Tim?"
#text = "There were 46 bales of hay in the barn and 32 bales in the shed . Tom stacked bales in the barn today . There are now 60 bales of hay in the barn . How many bales did he store in the barn ?"

text = "There are 8 apples in a pile on the desk. Each apple comes in a package of 11. 5 apples are added to the pile. How many apples are there in the pile?"
#text = "There are 5 apples in the basket. 10 apples are added to the basket. How many apples are there in the basket?"


#text = "Jason has 18 books and he has read 9 of them . Mary has 42 books . How many books do they have together ?"
#text = "Joan 's high school played 864 baseball games this year , 128 of the games were played at night . She attended 395 games . How many baseball games did Joan miss ?"
#@text = "There were a total of 8 football games this year , 4 are played at night . Keith missed 4 of the games . How many football games did Keith go to in total ?"
#text = "Sally paid 12.32 dollar total for peaches , after a 3 dollar coupon , and 11.54 dollar for cherries . In total , how much money did Sally spend ?"
#'''
nlp_parser.parse(text)

sentence_parser()

print "Given Text : -"
print
print text
print

if not element or not subs or not reference:
	pass
else:
	edit = zip(reference, subs, element)
	edit.sort()
	reference, subs, element = zip(*edit)
	list(reference)
	list(subs)
	list(element)
	text = text.replace("."," .")
	text = text.replace("?"," ?")
	word_net = text.split()
	#print word_net
	len_wrd_net = len(word_net)
	temp_holder = []
	j = 0
	for i in range(0, len_wrd_net):
		if word_net[i] in element:
			temp_holder.append(subs[j])
			j += 1
		else:
			temp_holder.append(word_net[i])
		
	text = ' '.join(temp_holder)
print

#'''

texts, info = sentence_sensor()
#print info
text = Wernicke.Wernicke_Sentence_parser(texts, info)
print "Parsed Text : -"
print text

nlp_parser.parse(text)
texts, info = sentence_sensor()
cp_text = text

Q_text,Q_dict,St_dict,St_text = ([] for lis in range(4))
le = len(info)
for i in range(0,le):
	dictionary = info[i]
	get_pos = dictionary.keys()[dictionary.values().index(".")]
	if get_pos == '?':
		Q_text.append(texts[i])
		Q_dict.append(info[i])
	elif get_pos == '.':
		St_text.append(texts[i])
		St_dict.append(info[i])
#print Q_text,"\n",Q_dict,"\n",St_dict,"\n",St_text

len_qtxt = len(Q_text)
for i in range(0,len_qtxt):
	Wernicke_main(Q_text[i], Q_dict[i], 0)
len_sttxt = len(St_text)
for i in range(0,len_sttxt):
	Wernicke_main(St_text[i], St_dict[i], i+1)
#print Q_tokens,"\n",St_tokens,"\n"

for i in range(0,le):
	dictionary = info[i]
	get_pos = dictionary.keys()[list(dictionary.values()).index(".")]
	if get_pos == "?":
		Wernicke.Question_Analyzer(dictionary, Q_tokens, texts[i])

#--!!----!!----!!----!!----!!----!!----!!----!!----!!----!!----!!----!!----!!----!!----!!----!!----!!----!!-

question, answer = Broca.Broca(cp_text, texts, Q_dict, info, Q_tokens, St_tokens)
for i in range(0,len(answer)):
	print "Total ",question[i]," : ",answer[i],"\n"
