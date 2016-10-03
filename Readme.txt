

Word Spell Check:

** The file to be run is main_w.py.
 Code Dependencies:
               findTypos.py
	       Trie31.py
	       soundx.py


 Data Dependencies:
		insertion.txt
		substitution.txt
		transpose.txt
		deletion.txt
		count_1w100k.txt
		bigram_file.pkl
		letter_file.pkl
 Input File:
	    input_w.txt - contains all wrongly spelt words, with one word per line
 Output File:
            output_file_w.txt - Code produces the top 10 suggestions for the given word with their scores

Sentence Spell Check:

** The file to be run is main_s.py.
 Code Dependencies:
               findTypos.py
	       Trie31.py
	       soundx.py


 Data Dependencies:
		insertion.txt
		substitution.txt
		transpose.txt
		deletion.txt
		count_1w100k.txt
		bigram_file.pkl
		letter_file.pkl
		confusion2.csv
		confusion_count.txt
		'collocations' folder placed in the same folder of above dependencies
		'confusion_words' folder placed in the same folder of above dependencies
 Input File:
	    input.txt - contains all sentences with atmost on incorrect word(although code can be easily modified to check for any number of    words), with one sentence per line
 Output File:
            output_file.txt - Code produces the top 3 suggestions for the identified incorrect(mispelt or word placed in wrong context) word with their scores





