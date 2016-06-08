import sys


def LF(bwt, C, sigma):
	char_to_idx = dict((c, i) for i, c in enumerate(sigma))
	
	print char_to_idx
	counts = C
	 
	LF = []
	
	for i, c in enumerate(bwt):
		char_idx = char_to_idx[c]
		
		LF.append(counts[char_idx])

		counts[char_idx] += 1
	
	return LF


def decode(bwt, LF):
	s = "$"
	i = 0

	while len(s) < len(bwt):
		s = bwt[i] + s
		i = LF[i]
	
	return s


def imtf(convert):
	code = convert[0]
	l = list(convert[1])
	
	string = ""
	r = 0
	
	for i in code:
		r = int(i)
		string += str(l[r])
		
		k = l[int(i)]
		l.pop(int(i))
		l.insert(0,k)
	
	return string

