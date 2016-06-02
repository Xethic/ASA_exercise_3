import sys

def encode(T):
	
	s = ""
	
	transform = []
	
	ordered = sorted(T)
	
	for i in range(len(T)):		
		
		s = T[i:]			
		s += T[:i]
		
		transform.append(s)
		
	print transform	
	
	sort = sorted(transform)
	
	print sort 
	
	bwtstring = ""
	index = 0
	
	for i in range(len(sort)):
		if sort[i] == T:
			index = i
		bwtstring += sort[i][-1:] 
	
	
	return bwtstring
	
	

def decode(bwt, LF):
	s = "$"
	i = 0
	
	while len(s) < len(bwt):
		s = bwt[i] + s
		i = LF[i]
	
	return s
		

def computeC(s):
	C = dict()
	res = []
	
	s = sorted(s)
	
	for i in range(len(s)):
		if s[i] not in C:
			C[s[i]] = i
			
	sort = sorted(C.items(), key = lambda tup: tup[0])
	
	for s in sort:
		res.append(s[1])		
			
	return res
	
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
	
	

def mtf(string):
	l= list()
	
	for c in string:
		if c not in l:
			l.append(str(c))
			
	l.sort()
	
	code = list()
	r = 0
	
	for c in string:
		r = l.index(str(c))
		code += [str(r)]
		
		l.pop(r)
		l.insert(0,c)
		
	l.sort()
	
	return [code, l]
	


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
	
	
def huffman(string):
	freq = dict()
	
	sort = sorted(string)
	l = len(sort)
	
	for s in sort:
		if s not in freq:
			freq[s] = float(sort.count(s)) / float(l)
		
	liste = freq.items()
	
	#liste = sorted(liste)
	
	sfreq = sorted(liste, key = lambda tup: tup[1])
	
	#first and second in list, 0 left 1 right, new node with "first+second" as name, first+second freq as value
	#tree contains node as key, tupel of freq, 0 or 1, parent as value
	
	print sfreq
	
	tree = dict()
	newnode = []
	
	if sfreq[0] <= sfreq[1]:
		
		l = sfreq[0]
		r = sfreq[1]
	else:
		r = sfreq[0]
		l = sfreq[1]
	
	njoin = (l[0]+r[0], l[1]+r[1])		
	newnode.append(njoin)
	
	tree[l[0]] = (l[1], "0", njoin)
	tree[r[0]] = (r[1], "1", njoin)
				
	for i in range (2, len(sfreq)):

		if sfreq[i][1] < newnode[0][1]:
			l = sfreq[i]
			r = newnode[0]
		else:
			r = sfreq[i]
			l = newnode[0]
				
		njoin = (l[0]+r[0], l[1]+r[1])
		newnode = []
		newnode.append(njoin)
		
		tree[l[0]] = (l[1], "0", njoin)
		tree[r[0]] = (r[1], "1", njoin)
		
		print l
		print r
	
	tree[njoin[0]] = (njoin[1])
	print tree
	
	code = ""	
	for s in string:
		s1 = s
		co = ""
		while(tree[s1] != 1.0):
			co += tree[s1][1]
			s1 = tree[s1][2][0]
		
		code += co[::-1]
	
	print code
	
	''''code = []
	bit = "1"
	start = True
	
	for f in sfreq[::-1]:
		if start:	
			code.append(f[0], bit
			start = False
		
		else:
			bit = "0"+bit
	print sfreq'''
	
	
with open(str(sys.argv[1])) as f:
	line = f.readline()
	
	line = line.replace("\n", "")
	
	line += "$"
	
	#returns bwt string and index with original string
	bwt = encode(line)
	
	sigma = []
	
	for s in sorted(line):
		if s not in sigma:
			sigma.append(s)
	
	C = computeC(line)

	LF = LF(bwt, C, sigma)
	
	code = mtf(bwt)	
	dec = imtf(code)	
	
	print decode(bwt, LF)
	#print decode(dec, bwt[1])
	

	huffman("300012003")

