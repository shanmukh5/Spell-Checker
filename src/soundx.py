def soundex1(word):
	#word = word.lower()
   #code = '01230120022455012623010202'
	code = '01360240043788015936020505'
	soundX_code = word[0].upper()
	if len(word) != 1:
		if code[ord(word[1])-97] != '0':
			soundX_code += code[ord(word[1])-97]
		for i in word[2:]:
			letter_code = code[ord(i)-97]
			if letter_code != '0' and letter_code != soundX_code[-1]:
				soundX_code += letter_code
	if len(soundX_code) < 5 :
		for x in xrange(0, 5-len(soundX_code)):
			soundX_code += '0'
	return soundX_code[:5]