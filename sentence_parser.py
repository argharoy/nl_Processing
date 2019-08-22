def parse():
	import json
	import re

	eleminate = ["He","he","HE","She","she","SHE","them","Them","it","its","It","It's","His","his"]s

	with open('data.json') as data_file:

		data = json.load(data_file)

	for key in data:
		if key == "coref":
			list_count = len(data["coref"]
			for i in range(0,list_count):
				'''
				print len(data["coref"][i])
				print data["coref"][i]
				print
				'''
				data_list_1 = data["coref"][i]
				lc1 = len(data_list_1)
				for j in range(0,lc1):
					data_list_2 = data["coref"][i][j]
					print data_list_2
					print
					lc2 = len(data_list_2)
					for k in range(0,lc2-1):
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