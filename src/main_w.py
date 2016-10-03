from findTypos import findTypos
import math
import time
from Trie31 import Trie_Mod
import cPickle as pickle
#from bk_tree import bk_tree
from soundx import soundex1

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

dic = Trie_Mod() # creating Trie based Dictionary

total_words = 5.80071238022e+11

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
dict_file = open('count_1w100k.txt', 'r') # using 100,000 words file as dictionary - minimal dicionary

for line in dict_file:
	words.append(line.lower())


for line in words:
	word = line.split('\t')
	dic.insert(word[0].lower())
	#total_words += float(word[1]) # Inserting each word from the file into the dictionary
############	#############################################
#inpu = open('data.csv','r')
#score = []
count = 1
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
dict_file.close()

with open('bigram_file.pkl', 'rb') as f:
	bigram_count = pickle.load(f)        # frequencies of various(676) bigrams

with open('letter_file.pkl', 'rb') as f:
	letter_count = pickle.load(f)        # frequencies of 26 alphabets
words_file = open('input_w.txt','r')
output_file = open('output_file_w.txt','w')
for w in words_file:
	while 1:
		w = w.replace('\n','')
		#w = raw_input('Enter the word: ').lower() # Inputting the typo word
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
		for x in xrange(0,min(10,len(final))):
			string += final[x][1] + ' ' + str(final[x][0]) + ' '
			#print final[x][1],###########################################
			#print final[x][0],###########################################
		string = string[0:len(string)-1] + '\n'
		output_file.write(string)
		break
		#print ''#######################################################
		#end = time.time()
		#print end-start
		#score.append(score_this)
		count += 1
	
