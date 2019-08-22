Noun_Sense = False
Adjective_Sense = False
Preposition_Sense = False
Adj_tokens, Prep_tokens, depender = ([] for lis in range(3))

subject_elements = ['NNP','NNPS']
object_elements = ['NN','NNS']
verb_elements = ['VB','VBD','VBG','VBN','VBP','VBZ']
wh_elements = ['WP','WDT','WP$','WRB']
adjective_elements = ['JJ','JJR','JJS']
adverb_elements = ['RB','RBR','RBS']
pronoun_elements = ['PRP','PRP$']
ex_elements = ['EX']
in_elements = ['IN']
dt_elements = ['DT']


count_dt = len(dt_elements)
count_in = len(in_elements)
count_ex = len(ex_elements)
count_wh = len(wh_elements)
count_verb = len(verb_elements)
count_adverb = len(adverb_elements)
count_subject = len(subject_elements)
count_adjectives = len(adjective_elements)
count_agreement = len(object_elements)

# 0 - adjectives, 1 - subjects, 2 - verbs, 3 - adverbs, 4 - agreements, 5 - exs, 6 - ins , 7 - dts

def process(elements, sub_text_1, sub_text_2, Mode):
	prep_token = ""
	#print elements, "\n",sub_text_1,"\n", sub_text_2
	#print "ELE->",elements[4]
	
	#selecting subject
	if elements[1] and not elements[5]:
		subject = ' '.join(elements[1])
	elif elements[5] and not elements[1]:
		subject = ' '.join(elements[5])
	elif not elements[1]:
		subject = "XXXX"

	#selecting prepositions
	if elements[6]:
		prep_token = ' '.join(elements[6])
		if elements[7]:
			prep_token = prep_token + " " + ' '.join(elements[7])

	if Mode == 1:
		if prep_token != "":
			t_1 = ' '.join(sub_text_1) + " " + prep_token + " " + ' '.join(elements[4]) + "."
		else:
			t_1 = ' '.join(sub_text_1) + " " +' '.join(elements[4])+"."
		t_2 = subject + " " + ' '.join(elements[2]) + " " +' '.join(sub_text_2)
		text = t_1 + " " + t_2
	elif Mode == 2: 
		#print elements
		t_1 = subject + " " +' '.join(elements[2]) + " " + ' '.join(sub_text_2) + "."
		if prep_token != "":
			text = ' '.join(sub_text_1) + " " + prep_token + " " + ' '.join(elements[4]) + ". " + t_1
		else:
			text = ' '.join(sub_text_1) + " " + ' '.join(elements[4]) + ". " + t_1

	return text


def picker(text, dictionary, Mode):
	#print dictionary
	look_ups = subject_elements + object_elements
	len_text = len(text)
	get_key = ""
	if Mode == 0: #backwards
		for word in range(len_text-1, 0, -1):
			#get_key = dictionary.keys()[dictionary.values().index(text[word])]
			get_key = dictionary.get(text[word])
			if get_key in look_ups:
				break
	elif Mode == 1: #forwards
		for word in range(0, len_text):
			#get_key = dictionary.keys()[dictionary.values().index(text[word])]
			get_key = dictionary.get(text[word])
			if get_key in look_ups:
				break
	
	return get_key

def Wernicke_Sensor(text, dictionary):
	pos_text_1, pos_text_2 = "", ""
	stop = ['if','and','but','then']
	stopper = []
	text = text.replace('.',' .')
	text = text.replace('?',' ?')
	get_pos = dictionary.get(".")
	if get_pos:
		elements = statement_analyzer(dictionary, get_pos, 0)
		#print elements
		#print "Argha"
	#values = dictionary.values()
	#print "-->",values
	text_tokens = text.split()
	stopper = [x for x in text_tokens if x in stop]
	if stopper:
		loc_stopper = [x for x,word in enumerate(text_tokens) if word in stop]
		if len(loc_stopper) == 1:
			location = loc_stopper[0]
			#print location
			sub_text_1 = text_tokens[0 : location]
			sub_text_2 = text_tokens[location+1 : ]
			#print sub_text_1,"\n",sub_text_2
			pos_text_1 = picker(sub_text_1, dictionary, 0)
			pos_text_2 = picker(sub_text_2, dictionary, 1)
	
	print pos_text_1," - ",pos_text_2

	if (pos_text_1 and pos_text_2 == "NNP") or (pos_text_1 and pos_text_2 == "NNPS"):
		text = ' '.join(text_tokens)
	elif pos_text_1 and pos_text_2 == "NN":
		#text = ' '.join(text_tokens)
		text = process(elements, sub_text_1, sub_text_2, 1)
	elif (pos_text_1 and pos_text_2 == "NNS" or "NNP") and (pos_text_1 is not pos_text_2):
		#mode 2
		text = process(elements, sub_text_1, sub_text_2, 2)
	elif pos_text_1 and pos_text_2 == "NNS":
		#print elements
		#mode 1
		text = process(elements, sub_text_1, sub_text_2, 1)

	return text



def Wernicke_Sentence_parser(C_text, C_info):
	tokens = []
	len_C_text = len(C_text)
	for i in range(0, len_C_text):
		text = C_text[i]
		dictionary = C_info[i]
		text = Wernicke_Sensor(text, dictionary)
		tokens.append(text)
	sentence = ' '.join(tokens)
	#print sentence
	return sentence

def finder(count, keys, elements, dictionary):
	#print "**", keys,"**", elements
	vals = dictionary.keys()
	#print "Val - > ",vals
	#print keys
	ret_lis = []
	for i in range(0,len(keys)):
		if keys[i] in elements:
			#ret_lis.append(dictionary.get(elements[i]))
			ins = dictionary.keys()[dictionary.values().index(keys[i])]
			if ins in ret_lis:
				for j in range(i,len(keys)):
					if keys[j] in elements:
						ret_lis.append(vals[j])
			else:
				ret_lis.append(ins)
		else:
			pass
	#print "RL-->",ret_lis
	return ret_lis

def filters(dictionary, subjects):
	ret_subjs, ret_args, resultant = ([] for lis in range(3))
	values = dictionary.values()
	proceed_if = [x for x in values if x in subjects]
	if proceed_if:
		len_prc_if = len(proceed_if)
		for proceed in range(0,len_prc_if):
			#get_key = dictionary.keys()[dictionary.values().index(proceed_if[proceed])]
			get_key = dictionary.get(proceed_if[proceed])
			if get_key == "NNS":
				ret_subjs.append(proceed_if[proceed])
			elif get_key == "NN":
				ret_args.append(proceed_if[proceed])
			else:
				pass
	else:
		pass

	resultant.append(ret_subjs)
	resultant.append(ret_args)
	#print ret_subjs,ret_args

	if ret_subjs and ret_args:
		return resultant
	else:
		return False;
			

def statement_analyzer(dictionary, pos, mode):
	ws, verbs, adverbs, subjects, agreements, adjectives, ret_list = ([] for lis in range(7))
	values = dictionary.values()
	#print "x-->",values

	exs = finder(count_ex, values, ex_elements, dictionary) 
	ins = finder(count_in, values, in_elements, dictionary)
	dts = finder(count_dt, values, dt_elements, dictionary)
	verbs = finder(count_verb, values, verb_elements, dictionary)
	adverbs = finder(count_adverb, values, adverb_elements, dictionary)
	adjectives = finder(count_adjectives, values, adjective_elements, dictionary)


	if pos == '?':

		whs = finder(count_wh, values, wh_elements, dictionary)
		subjects = finder(count_agreement,values,object_elements, dictionary)
		agreements = finder(count_subject, values, subject_elements, dictionary)

		if mode == 0:
			return ret_list

		filter_store = filters(dictionary, subjects)

		if filter_store == False:
			pass
		else:
			adjectives = filter_store[0]
			subjects = filter_store[1]
			agreements = filter_store[2]

		#print ws," | ",adjectives," | ",subjects," | ",verbs," | ",adverbs," | ",agreements
		ret_list.extend([whs,adjectives,subjects,verbs,agreements,exs,ins,dts])
		
		return ret_list, True

	elif pos == '.':

		subjects = finder(count_subject, values, subject_elements, dictionary)
		agreements = finder(count_agreement, values, object_elements, dictionary)
		#print adjectives," | ",subjects," | ",verbs," | ",adverbs," | ",agreements
		ret_list.extend([adjectives, subjects, verbs, adverbs, agreements,exs,ins,dts])

		if mode == 0:
			return ret_list
		else:
			return ret_list, False

	else:
		pass

def Preposition_learner(dictionary, Ques_for):
	tokens = []
	keys = dictionary.keys()
	values = dictionary.values()
	for i in range(0,len(keys)):
		if values[i] == "IN":
			tokens.append(keys[i])
	if tokens:
		return tokens, True
	else:
		return False, False

def Adjective_learner(dictionary, Ques_for):
	remember_adj = ["much","many"]
	tokens = []
	keys = dictionary.keys()
	values = dictionary.values()
	for i in range(0,len(keys)):
		if values[i] == "JJ" and keys[i] not in remember_adj:
			tokens.append(keys[i])
	if tokens:
		return tokens, True
	else:
		return False, False

def Question_Analyzer(dictionary, Ques_for, text):
	global Adjective_Sense, Preposition_Sense, Noun_Sense, Adj_tokens, Prep_tokens, depender, Noun_tokens
	#print dictionary," = ",Ques_for
	keys = dictionary.keys()
	values = dictionary.values()
	Adj_tokens, Adjective_Sense = Adjective_learner(dictionary, Ques_for)
	#print Adjective_Sense
	Prep_tokens, Preposition_Sense = Preposition_learner(dictionary, Ques_for)
	#print Preposition_Sense
	#Noun_tokens, Noun_Sense  = Noun_learner(dictionary, Ques_for, text)
	if Preposition_Sense == True:
		#print text
		texts = text.split()
		loc = [x for x,word in enumerate(texts) if word == Prep_tokens[0]]
		for j in range(loc[0]+1, len(texts)):
			val = dictionary.get(texts[j])
			if val == "NNS" or val == "NN":
				depender.append(texts[j])

#print Adjective_Sense," --- ",Preposition_Sense," --- ",Noun_Sense