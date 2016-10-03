''' Author - G.Shanmukha Chaitanya'''

from findTypos import findTypos
import math
import time
#from Trie31 import Trie_Mod -- changed code -------------------------------------------------- #
import cPickle as pickle
#from bk_tree import bk_
import re
from soundx import soundex1

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

#dic = Trie_Mod() # creating Trie based Dictionary

total_words = 5.80071238022e+11
with open('trie_pos.pkl', 'rb') as output1:
    dic = pickle.load(output1)
output_file = open('output_file.txt','w')

words = []
insertion_file = []
deletion_file = []
substitution_file = []
transpose_file = []

insertion = open('insertion.txt','r')
substitution = open('substitution.txt','r')
deletion = open('deletion.txt','r')
transpose = open('transpose.txt','r')
#start = time.time()
'''
dict_file = open('count_1w100k.txt', 'r') # using 100,000 words file as dictionary - minimal dicionary

for line in dict_file:
	words.append(line.lower())


for line in words:
	word = line.split('\t')
	dic.insert(word[0].lower())
	#total_words += float(word[1]) # Inserting each word from the file into the dictionary
	'''
############	#############################################
#inpu = open('data.csv','r')
#score = []

#########################################
#end = time.time()

#print end-start
for line in insertion:
	insertion_file.append(line)
for line in substitution:
	substitution_file.append(line)
for line in deletion:
	deletion_file.append(line)
for line in transpose:
	transpose_file.append(line)


#print total_words
#dict_file.close()

with open('bigram_file.pkl', 'rb') as f:
	bigram_count = pickle.load(f)        # frequencies of various(676) bigrams

with open('letter_file.pkl', 'rb') as f:
	letter_count = pickle.load(f)        # frequencies of 26 alphabets
sentences = open('input.txt','r')
for s in sentences:

	#s = raw_input("Enter the sentence: ")
	s = s.replace('\n','')
	s = re.sub(r'[^\w\s]','',s).split()
	s = [w.lower() for w in s]
	length = len(s)
	found1 = False
	count = 0
	while 1:
		if count == length:
			break
		w = s[count] # Inputting the typo word
		if dic.search(w):
			count += 1
			continue
		found1 = True
		#start = time.time()
		############### testing code ######################
		'''
		if count%25 == 0:
			print count
		if count % 100 == 0:
			print mean(score)
		string = inpu.readline()
		if string == '':
			break
		string = string.split(',')
		w = string[0].lower()
		string[1] = string[1].lower()
		'''
		##################################################
		if len(w) <= 5:
			edit_dis = 1
		else:
			edit_dis = 2
		if w == '..':
			break
		#print 'FOUND: ' + ('YEP' if dic.search(w) else 'NOPE') # fouund or not in the dictionary#########################################

		found = dic.find(w)
		set_len = len(found)
		suggestions = [] # suggestions including words upto 3-edit distances

		for x in xrange(0,set_len):
			suggestions.append(found.pop())

		typos_arr = [] # typos including words upto 3-edit distances

		for x in xrange(0,set_len):
			typos_arr.append(findTypos(suggestions[x], w))

		suggestions_2 = [] # suggestions for just 2-edit distance case
		typos_final = []

		suggestions_3 = [] # suggestions for just 3-edit distance case

		for x in xrange(0,set_len):
			if len(typos_arr[x].split('.')) < edit_dis+2: # filtering words upto 2-edit distances
				suggestions_2.append(suggestions[x])
				typos_final.append(typos_arr[x])
			else:
				if len(typos_arr[x].split('.')) == edit_dis+2:
					suggestions_3.append(suggestions[x])	
		posterior_arr = []

		for i in xrange(0,len(typos_final)):
			typo = typos_final[i]
			typo_sing = typo.split('.')
			likelihood = 1.0
			for x in xrange(1,len(typo_sing)):
				#words = open('count_1w.txt', 'r')
				decode = typo_sing[x].split('|')
				if decode[0] == 'i':
					if decode[1] == '#':
						den = total_words
					else:
						den = float(letter_count[ord(decode[1])-97])
					num = 0.0
					for line in insertion_file:
						line_arr = line.split(' ')
						if decode[1] == line_arr[0] and decode[2] == line_arr[1]:
						 	 num += float(line_arr[2])
					likelihood = likelihood * num/den

				if decode[0] == 'd':
					if len(decode[1]) != 1:
						den = bigram_count[decode[1]]				
					num = 0.0
					for line in deletion_file:
						line_arr = line.split(' ')
						if decode[1] == line_arr[0] and decode[2] == line_arr[1]:
						 	 num += float(line_arr[2])
					likelihood = likelihood * num/den

				if decode[0] == 's':
					den = float(letter_count[ord(decode[1])-97])
					num = 0.0
					for line in substitution_file:
						line_arr = line.split(' ')
						if decode[1] == line_arr[0] and decode[2] == line_arr[1]:
						 	 num += float(line_arr[2])
					likelihood = likelihood * num/den
				if decode[0] == 't':
					den = bigram_count[decode[1]]
					num = 0.0
					for line in transpose_file:
						line_arr = line.split(' ')
						if decode[1] == line_arr[0] and decode[2] == line_arr[1]:
						 	 num += float(line_arr[2])
					likelihood = likelihood * num/den

			freq = 0.0

			for line in words:
				line_arr = line.split('\t')
				if suggestions_2[i] == line_arr[0]:
					freq = float(line_arr[1])
					break
			prior = (freq + 0.5)/total_words
			posterior = likelihood * prior
			posterior_arr.append(posterior)

		posterior_arr_3 = [0.0]*len(suggestions_3)
		soundx_code = soundex1(w)
		#posterior_arr = [math.log(x) for x in posterior_arr]
		if len(posterior_arr) != 0:
			max_pos = max(posterior_arr)
			if max_pos != 0:
				posterior_arr = [x/max_pos for x in posterior_arr]
		soundx_val = mean(posterior_arr)
		if soundx_val == 0.0:
			soundx_val = 1.0
		for x in xrange(0,len(suggestions_2)):
			if soundex1(suggestions_2[x]) == soundx_code:
				posterior_arr[x] += soundx_val
		for x in xrange(0,len(suggestions_3)):
			if soundex1(suggestions_3[x]) == soundx_code:
				posterior_arr_3[x] += soundx_val

		posterior_final = posterior_arr + posterior_arr_3
		suggestions_final = suggestions_2 + suggestions_3

		########################################
		#score_this = 0.0
		######################################
		final = [(y,x) for (y,x) in sorted(zip(posterior_final,suggestions_final), reverse = True)]
		if len(final) != 0:
			if final[0][1] == w:
				if len(final) != 1:
					final = final[1:]
		string = ''
		for x in xrange(0,min(3,len(final))):
			string += final[x][1] + ' ' + str(final[x][0]) + ' '
		
		string = string[0:len(string)-1] + '\n'
		output_file.write(string)
			#print final[x][1],###########################################
			#print final[x][0],###########################################

		#print ''#######################################################
		break
		#end = time.time()
		#print end-start
		#score.append(score_this)
	####### word spell checker ends and context spell checker starts ###################
	if not found1:
		confusion_set_file = open('confusion2.csv','r')
		confusion_set = []
		confusion_count = []
		for line in confusion_set_file:
			confusion_set.append(line)

		#s = raw_input("Enter the sentence: ")
		#s = re.sub(r'[^\w\s]','',s).split()
		#s = [w.lower() for w in s]
		confusion_count_file = open('confusion_count.txt','r')
		for line in confusion_count_file:
			confusion_count.append(line)
		#print s
		#confusion_set = confusion_set.split(',')
		count = 0

# --------- --------------------- ------------------- #


		def rel_metric(c1, c2, confusion_list):
			if len(c1.split()) > 1:
			 	freq_f = []
			 	for word in confusion_list:
			 		string = 'collocations/' + word + '.txt'
			 		f = open(string,'r')
			 		found = False
			 		for line in f:
			 			line = line.replace("\n", "")
			 			if line.split(' ')[0:5] == c1.split():
			 				found = True
			 				freq_f.append(float(line.split(' ')[5]))
			 				break
			 		if found == False:
			 			freq_f.append(0.0)
			 	if sum(freq_f) != 0.0:
			 		r1 = max(freq_f)/sum(freq_f)
			 	else:
			 		r1 = 0.0
			 		
			else:
			 	freq_f = []
			 	for word in confusion_list:
			 		string = 'confusion_words/' + word + '.txt'
			 		f = open(string,'r')
			 		found = False
			 		for line in f:
			 			line = line.replace("\n", "")
			 			if line.split(' ')[0] == c1:
			 				found = True
			 				freq_f.append(float(line.split(' ')[1]))
			 				break
			 		if found == False:
			 			freq_f.append(0.0)
			 	if sum(freq_f) != 0.0:
			 		r1 = max(freq_f)/sum(freq_f)
			 	else:
			 		r1 = 0.0

			if len(c2.split()) > 1:
			 	freq_f = []
			 	for word in confusion_list:
			 		string = 'collocations/' + word + '.txt'
			 		f = open(string,'r')
			 		found = False
			 		for line in f:
			 			line = line.replace("\n", "")
			 			if line.split(' ')[0:5] == c2.split():
			 				found = True
			 				freq_f.append(float(line.split(' ')[5]))
			 				break
			 		if found == False:
			 			freq_f.append(0.0)
			 	if sum(freq_f) != 0.0:
			 		r2 = max(freq_f)/sum(freq_f)
			 	else:
			 		r2 = 0.0

			else:
			 	freq_f = []
			 	for word in confusion_list:
			 		string = 'confusion_words/' + word + '.txt'
			 		f = open(string,'r')
			 		found = False
			 		for line in f:
			 			line = line.replace("\n", "")
			 			if line.split(' ')[0] == c2:
			 				found = True
			 				freq_f.append(float(line.split(' ')[1]))
			 				break
			 		if found == False:
			 			freq_f.append(0.0)
			 	if sum(freq_f) != 0.0:
			 		r2 = max(freq_f)/sum(freq_f)
			 	else:
			 		r2 = 0.0

			return False if r1 > r2 else True

		def context_words_f(s, index):
			list_c = []
			for x in xrange(max(0,index-3),min(len(s),index+4)):
				if x != index:
					list_c.append(s[x])
			return list_c

		def collocations_f(s, index):
			tag_set_words_l = []
			tag_set_words_r = []
			for x in xrange(max(0,index-2),min(len(s),index+3)):
				if x < index:
					tag_set_words_l.append(dic.search(s[x]))
				if x > index:
					tag_set_words_r.append(dic.search(s[x]))
			list_c = []

			if len(tag_set_words_l) != 0:
				for tag in tag_set_words_l[-1]:
					col = tag + ' _ * *'
				 	list_c.append('* ' + col)
				 	if len(tag_set_words_l) > 1:
				 		for tag1 in tag_set_words_l[-2]:
				 			list_c.append(tag1 + ' ' + col)
						list_c.append(s[index-2] + ' ' + col)	 		
				col = s[index-1] + ' _ * *'
				list_c.append('* ' + col)
				if len(tag_set_words_l) > 1:
				 	for tag in tag_set_words_l[-2]:
				 		list_c.append(tag + ' ' + col)

			if len(tag_set_words_r) != 0:
				for tag in tag_set_words_r[0]:
					col = '* * _ ' + tag 
				 	list_c.append(col + ' *')
				 	if len(tag_set_words_r) > 1:
				 		for tag1 in tag_set_words_r[1]:
				 			list_c.append(col + ' ' + tag1)
						list_c.append(col + ' ' + s[index+2])
				col = '* * _ ' + s[index+1]
				list_c.append(col + ' *')
				if len(tag_set_words_r) > 1:
				 	for tag in tag_set_words_r[1]:
				 		list_c.append(col + ' ' + tag)

			if len(tag_set_words_l) != 0 and len(tag_set_words_r) != 0:
				tag_words = list(tag_set_words_l[-1])
				tag_words.append(s[index-1])
				tag_words1 = list(tag_set_words_r[0])
				tag_words1.append(s[index+1])
				for tag in tag_words:
					for tag1 in tag_words1:
						col =  '* ' + tag + ' _ ' + tag1 + ' *'
						list_c.append(col)
			return list_c

		final_words = []

		for word in s:
			found = False
			if found:
				break
			for line in confusion_set:
				line = line.replace("\n", "")
				confuse_words = line.split(',')
				confuse_words = [w for w in confuse_words if w != '']
				for confuse_word in confuse_words:
					if confuse_word == word:
						confusion_list = confuse_words
						found = True
						break
				if found == True:
					break
			#print found
			if found == True:
				#print confusion_list
				context_words = context_words_f(s,count)
				collocations = collocations_f(s, count)
				index = 0
				while 1:
					if index == len(collocations):
						break
					collocation = collocations[index]
					left_c = collocation.split('_')[0].split(' ')
					right_c = collocation.split('_')[1].split(' ')
					index_c = index+1
					while 1:
						if index_c == len(collocations):
							break
						next_c = collocations[index_c]
						next_cleft =  next_c.split('_')[0].split(' ')
						next_cright = next_c.split('_')[1].split(' ')
						if left_c[1] == next_cleft[1] and left_c[1] != '*':
							if rel_metric(collocation,next_c, confusion_list):
								del collocations[index]
								break
							else:
								del collocations[index_c]
								continue
						if right_c[1] == next_cright[1] and right_c[1] != '*':
							if rel_metric(collocation,next_c, confusion_list):
								del collocations[index]
								break
							else:
								del collocations[index_c]
								continue

						
						index_c += 1
					index += 1

				for context_word in context_words:
					for collocation in collocations:
						col_list = collocation.split()
						if context_word in col_list:
							if rel_metric(context_word,collocation, confusion_list):
								context_words.remove(context_word)
								break
							else:
								collocations.remove(collocation)
								continue

				#features = context_words + collocations
				
				prob = []

				for confusion_word in confusion_list:
					prob_word = 1
					for line in confusion_count:
						line = line.replace("\n", "")
						if line.split()[0] == confusion_word:
							word_count = float(line.split()[1])
							break
					for context_word in context_words:
						path = 'confusion_words/' + confusion_word + '.txt'
						f = open(path,'r')
						context_count = 0.0
						for line in f:
							line = line.replace("\n", "")
							if context_word == line.split()[0]:
								context_count = float(line.split()[1])
								break
						prob_word *= (0.005 + context_count)/word_count

					for collocation in collocations:
						path = 'collocations/' + confusion_word + '.txt'
						f = open(path,'r')
						collocation_count = 0.0
						for line in f:
							line = line.replace("\n", "")
							if collocation.split() == line.split()[0:5]:
								collocation_count = float(line.split()[5])
								break
						prob_word *= (0.005 + collocation_count)/word_count

					prob.append(prob_word)

				final_words = [y for (x,y) in sorted(zip(prob,confusion_list), reverse = True)]
				prob.sort(reverse = True)
				



			count += 1

		string = ''
		for x in xrange(0, min(3, len(final_words))):
			#print final_words[x],###########################################
			#print prob[x],###########################################

			string += final_words[x] + ' ' + str(prob[x]) + ' '
		string = string[0:len(string)-1] + '\n'
		output_file.write(string)

	
