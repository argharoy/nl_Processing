import re
import itertools
def Broca_Calculator(operations, extracted_digits):
	print operations," |<>| ",extracted_digits
	calculate = []
	operands = []
	ext_len = len(extracted_digits)
	#print "ex--",ext_len
	opt_len = len(operations)
	if opt_len > 1 and extracted_digits:
		for digits in range(0,ext_len):
			operands = extracted_digits[digits]
			cal = 0
			#print operands,"\n"
			operands_length = len(operands)
			for operator in range(0,operands_length):
				if operations[operator] == 0:
					return
				elif operations[operator] == 1:
					cal = cal + int(operands[operator])
				elif operations[operator] == 2:
					cal = int(operands[operator]) - cal
				else:
					pass
			if cal != "":
				calculate.append(abs(cal))
			else:
				pass
	elif opt_len <= 1 and extracted_digits:
		operands = extracted_digits	
		cal = 0
		if operations[0] == 0:
			return
		elif operations[0] == 1:
			for operand in range(0,len(operands)):
				cal = cal + int(operands[operand])
		elif operations[0] == 2:
			cal = abs(int(operands[0]) - int(operands[1]))
		else:
			pass
		if cal != "":
			calculate.append(cal)
		else:
			pass

	return calculate
def Broca_Tense_learner(dictionary):
	tense = ""
	present_tense_qoutes = ['VB']
	past_tense_quotes = ['VBD']
	verb_magic_quotes = ['do','does','did','are']

	keys = dictionary.keys()
	print "KEys -> ",keys


	#extract verb do,does,did,are and process accordingly

	common_verbs = [x for x in verb_magic_quotes if x in keys]
	print common_verbs
	if common_verbs[0] == "did":
		tense = "past"
	else:
		tense = "present"

	return tense

def Broca_Person_learner(dictionary):
	first_person_singular, third_person_plural, third_person_singular = ([] for lis in range(3))
	#third_person_plural for data sets
	fps_magic_quotes = ["i","you","we","they","there"] #do words
	sps_magic_quotes = ['you']#2nd person singular
	tps_magic_quotes = ['NNP'] #he/she/it
	tpp_magic_quotes = ['NNS','NNPS']
	t_list = []

	qdic_keys = dictionary.keys()
	qdic_values = dictionary.values()
	print qdic_values,"````~~~~"

	if [x for x in fps_magic_quotes if x in qdic_keys]:
		first_person_singular = [x for x in fps_magic_quotes if x in qdic_keys]
	else:
		pass

	if [x for x in tps_magic_quotes if x in qdic_keys]:
		common_tps = [x for x in tps_magic_quotes if x in qdic_keys]
		len_tps = len(common_tps)
		for j in range(0,len_tps):
			val = dictionary.get(common_tps[j])
			t_list.append(val)
	else:
		pass

	third_person_singular.extend(t_list)

	if [x for x in tpp_magic_quotes if x in qdic_keys]:
		common_tpp = [x for x in tpp_magic_quotes if x in qdic_keys]
		len_tpp = len(common_tpp)
		for j in range(0,len_tpp):
			val = dictionary.get(common_tpp[j])
			t_list.append(val)
	else:
		pass

	third_person_plural.extend(t_list)

	print first_person_singular, third_person_plural, third_person_singular
	return first_person_singular, third_person_plural, third_person_singular

def Broca_Logic_generator(Question_dictionary, Ques_for, location_keys, location_cds, extracted_digits, extracted_sentence_number):
	operations = []
	operation = 0
	calculate = ""
	#print extracted_digits
	Q_for_length = len(Ques_for)
	esn_length = len(extracted_sentence_number)
	ed_length = len(extracted_digits)
	#print Question_dictionary
	#for subject in range(0,Q_for_length):
	logic_info = []
	dictionary = Question_dictionary[0]
	first_person_singular, third_person_plural, third_person_singular = Broca_Person_learner(dictionary)
	#make tense learner
	tense = Broca_Tense_learner(dictionary)
	#print first_person_singular, third_person_plural, third_person_singular
	logic_info.extend([first_person_singular, third_person_singular])

	#print logic_info[0]

	if logic_info[0] and not logic_info[1] and tense == "present":
		operation = 1
	elif logic_info[1] and not logic_info[0] and tense == "past":
		operation = 2
	elif not logic_info[0] and not logic_info[1] and tense == "past":
		operation = 2
	else:
		operation = 3

	operations.append(operation)
	
	return operations

def Broca_Compiler(sentence_locations, sentence_web, measeure, dictionary):
	keys, cds, digits, sen_no = ([] for lis in range(4))
	#print sentence_locations

	sen_loc_length = len(sentence_locations)
	for j in range(0,sen_loc_length):
		text = sentence_web[sentence_locations[j]]
		text = text.replace(".","")
		text = text.replace("?","")

		word_net = text.split()
		infos = dictionary[sentence_locations[j]]
		vals = infos.values()
		if "CD" not in vals:
			pass
		else:
			get_CD = infos.keys()[list(infos.values()).index("CD")]
			measure_word_location = [w for w,word in enumerate(word_net) if word == measeure]			
			CD_location = [d for d,digit in enumerate(word_net) if digit == get_CD]
			#print CD_location
			cds.append(CD_location)
			keys.append(measure_word_location)
			digits.append(get_CD)
			sen_no.append(j+1)

	return keys, cds, digits, sen_no

def sensor_common_extractor(length, sent_dict, c_var):
	if c_var:
		#values = sent_dict.values()
		values = sent_dict.keys()
		l = len(values)
		for j in range(0,l):
			#print Ques_for
			#print "Vj-> ",sent_dict.get(values[j])
			#key = list(sent_dict.keys())[list(sent_dict.values()).index(values[j])]
			key = sent_dict.get(values[j])
			if key == "NNS" and values[j] == Ques_for:
				get_CD = sent_dict.keys()[list(sent_dict.values()).index("CD")]
				#print "NN->",get_CD
				extracts.append(get_CD)
				measeure = Ques_for
		extracted_values.extend(extracts)
	else:
		pass


def Broca_sensor_extractor(texts, Ques_for, search_for, dictionary):
	from Wernicke import Adjective_Sense, Adj_tokens, Preposition_Sense, Prep_tokens, depender
	#print Adjective_Sense," --- ",Preposition_Sense
	extracted_values = []
	key_loc = []
	cd_loc = []
	sen_no = []
	measeure = ""
	length = len(dictionary)
	#print "XX--",Ques_for
	if Adjective_Sense == True:
		for i in range(0, length):
			extracts = []
			sent_dict = dictionary[i]
			vals = sent_dict.values()
			c_var = [x for x in vals if x == "CD"]
			if c_var:
				token = texts[i].split()
				print token
				common = [x for x in token if x in Adj_tokens]
				if common and Ques_for in token:
					get_CD = sent_dict.keys()[list(sent_dict.values()).index("CD")]
					extracts.append(get_CD)
					loc = [x for x, k in enumerate(token) if k == get_CD]
					cd_loc.append(loc[0])
					loc = [x for x, k in enumerate(token) if k == Ques_for]
					key_loc.append(loc[0])
					measeure = Ques_for
					sen_no.append(i+1)
				else:
					pass
			else:
				pass

			extracted_values.extend(extracts)

	elif Preposition_Sense == True:
		for i in range(0, length):
			extracts = []
			sent_dict = dictionary[i]
			print sent_dict,"\n Depender : - ",depender,"-->PT-->",Prep_tokens
			vals = sent_dict.values()
			c_var = [x for x in vals if x == "CD"]
			if c_var:
				token = texts[i].split()
				common = [x for x in token if x in Prep_tokens]
				#print "Common : - ",common
				if common or depender in token:
					get_CD = sent_dict.keys()[list(sent_dict.values()).index("CD")]
					extracts.append(get_CD)
					loc = [x for x, k in enumerate(token) if k == get_CD]
					cd_loc.append(loc[0])
					loc = [x for x, k in enumerate(token) if k == Ques_for]
					key_loc.append(loc[0])
					measeure = Ques_for
					sen_no.append(i+1)
				elif [x for x in token if x in Ques_for]:
					values = sent_dict.keys()
					l = len(values)
					for j in range(0,l):
						#print Ques_for
						#print "Vj-> ",sent_dict.get(values[j])
						#key = list(sent_dict.keys())[list(sent_dict.values()).index(values[j])]
						key = sent_dict.get(values[j])
						if key == "NNS" and values[j] == Ques_for:
							get_CD = sent_dict.keys()[list(sent_dict.values()).index("CD")]
							#print "NN->",get_CD
							extracts.append(get_CD)
							measeure = Ques_for
				else:
					pass
			extracted_values.extend(extracts)
	else:
		for i in range(0,length):

			extracts = []
			sent_dict = dictionary[i]
			vals = sent_dict.values()
			c_var = [x for x in vals if x == "CD"]
			#control_var = c_var[0]
			if c_var:
				#values = sent_dict.values()
				values = sent_dict.keys()
				l = len(values)
				for j in range(0,l):
					#print Ques_for
					#print "Vj-> ",sent_dict.get(values[j])
					#key = list(sent_dict.keys())[list(sent_dict.values()).index(values[j])]
					key = sent_dict.get(values[j])
					if key == "NNS" and values[j] == Ques_for:
						get_CD = sent_dict.keys()[list(sent_dict.values()).index("CD")]
						#print "NN->",get_CD
						extracts.append(get_CD)
						measeure = Ques_for
				extracted_values.extend(extracts)
			else:
				pass

	#print extracted_values, key_loc, cd_loc, sen_no, measeure
	return extracted_values, key_loc, cd_loc, sen_no, measeure

def most_common(ques):
	import operator
	ques_for = reduce(operator.add, ques)
	return max(set(ques_for), key=ques_for.count)

def ques_for_checker(text, token):
	#print token
	verb_magic_quotes = ['do','does','did','are']
	verb_loc = [x for x, word in enumerate(text) if word in verb_magic_quotes]
	token_loc = [x for x, word in enumerate(text) if word == token]
	if token_loc[0] < verb_loc[0]:
		return True
	else:
		return False


def Broca(text, texts, Question_dictionary, dictionary, Q_tokens, St_tokens):
	Ques_for,sentence_number,Search_for,calculate,measeures = ([] for lis in range(5))
	location_keys, location_cds, extracted_digits, extracted_sentence_number = ([] for lis in range(4))
	Q_length = len(Question_dictionary)
	St_length = len(St_tokens)
	temp_dictionary = list(reversed(dictionary))
	temp_texts = list(reversed(texts))
	#print Question_dictionary
	for i in range(0, Q_length):
		Ques = []
		#print Question_dictionary[i],"\n",temp_texts[i]
		q_dict = temp_dictionary[i]
		print q_dict
		tx_lis = temp_texts[i].split()
		commons = [x for x in tx_lis if x in Q_tokens]
		print commons
		len_commons = len(commons)
		for j in range(0, len_commons):
			get_pos = q_dict.get(commons[j])
			if get_pos == "NNS":
				get_response = ques_for_checker(tx_lis,commons[j])
				if get_response == True:
					Ques_for.append(commons[j])
		Ques.append(Ques)
	#print Ques_for
	Ques_for = list(reversed(Ques_for))
	temp_ques = []
	for i in range(0,St_length):
		if [x for x in St_tokens[i] if x in Ques_for]:
			temp_ques.append([x for x in St_tokens[i] if x in Ques_for])
			sentence_number.append(i)
			Search_for.append(x)

	le_qf = len(Ques_for)
	sentence_web = re.split('(?<=[.?]) +',text)

	for i in range(0,le_qf):
		ext_values, key_loc, cd_loc, sen_no, measeure = Broca_sensor_extractor(texts, Ques_for[i], Search_for, dictionary)
		#for which sentence
		#print "SLOC ->",sentence_locations
		#for calculation
		print "VALS ->",ext_values
		#subject to be found
		print "MEA ->",measeure
		
		#keys, cds, digits, extracted_sentence_number = Broca_Compiler(sentence_number, sentence_web, measeure, dictionary)
		#location_keys.extend(keys)
		#location_cds.extend(cds)
		#extracted_digits.extend([digits])
		#print extracted_sentence_number,"\n",location_keys," <==>",extracted_digits,"\n",extracted_digits
		if measeure and ext_values:
			operations = Broca_Logic_generator(Question_dictionary, Ques_for, key_loc, cd_loc, ext_values, sen_no)
			calculate = Broca_Calculator(operations, ext_values)
			measeures.append(str(measeure))
				
		else:
			pass
	return measeures, calculate