def findTypos(correction, typo):
	i = 0
	j  =0
	corr_size = len(correction)
	typo_size = len(typo)

	typosFound = ''
	while 1:
		if i < corr_size and j < typo_size:
			if correction[i] == typo[j]:
				i += 1
				j += 1
			else:
				if i+1 < corr_size and j+1 < typo_size:
					if correction[i] == typo[j+1] and correction[i+1] == typo[j] :
						typosFound = typosFound + '.' + 't' + '|' + correction[i:i+2] + '|' + typo[j:j+2]
						i += 2
						j += 2
					elif correction[i] == typo[j+1]:
						if i-1 != -1:
							typosFound = typosFound + '.' + 'i' + '|' + typo[j-1] + '|' + typo[j-1:j+1]
						else:
							typosFound = typosFound + '.' + 'i' + '|' + '#' + '|' + typo[j]
						i += 1
						j += 2
					elif correction[i+1] == typo[j]:
						if i-1 != -1:
							typosFound = typosFound + '.' + 'd' + '|' + typo[j-1] + correction[i] + '|' + typo[j-1]
						else:
							typosFound = typosFound + '.' + 'd' + '|' + correction[i] + '|' + '#'
						i += 2
						j += 1
					else:
						typosFound = typosFound + '.' + 's' + '|' + correction[i] + '|' + typo[j]
						i += 1
						j += 1
				else:
					if i+1 == corr_size and j+1 == typo_size:
						typosFound = typosFound + '.' + 's' + '|' + correction[i] + '|' + typo[j]
						i += 1
						j += 1
					elif i+1 == corr_size:
						if correction[i] == typo[j+1]:
							typosFound = typosFound + '.' + 'i' + '|' + typo[j-1] + '|' + typo[j-1:j+1]
							i += 1
							j += 2
						else:
							typosFound = typosFound + '.' + 's' + '|' + correction[i] + '|' + typo[j]
							i += 1
							j += 1
					elif j+1 == typo_size:
						if correction[i+1] == typo[j]:
							typosFound = typosFound + '.' + 'd' + '|' + typo[j-1] + correction[i] + '|' + typo[j-1]
							i += 2
							j += 1
						else:
							typosFound = typosFound + '.' + 's' + '|' + correction[i] + '|' + typo[j]
							i += 1
							j += 1
					else:
						typosFound = typosFound + '.' + 's' + '|' + correction[i] + '|' + typo[j]
						i += 1
						j += 1						
								
		else:
			break

		if i != corr_size or j != typo_size :
			if i == corr_size:
				for x in xrange(j,typo_size):
					typosFound = typosFound + '.' + 'i' + '|' + typo[x-1] + '|' + typo[x-1:x+1]
			elif j == typo_size:
				for x in xrange(i,corr_size):
					typosFound = typosFound + '.' + 'd' + '|' + typo[j-1] + correction[x] + '|' + typo[j-1]

	return typosFound 
							