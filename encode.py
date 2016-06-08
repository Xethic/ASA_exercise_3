import sys


def computeSigma(text):
	sigma = []
	
	for s in sorted(text):
		if s not in sigma:
			sigma.append(s)
	
	return sigma


def encodeBWT(T):
	
	s = ""
	
	transform = []
	
	ordered = sorted(T)
	
	for i in range(len(T)):		
		
		s = T[i:]			
		s += T[:i]
		
		transform.append(s)	
	
	sort = sorted(transform)
	
	bwtstring = ""
	index = 0
	
	for i in range(len(sort)):
		if sort[i] == T:
			index = i
		bwtstring += sort[i][-1:] 
	
	
	return bwtstring
		
		
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
	
	#print sfreq
	
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
	
	tree[l[0]] = (l[1], "0", njoin[0])
	tree[r[0]] = (r[1], "1", njoin[0])
				
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
		
		tree[l[0]] = (l[1], "0", njoin[0])
		tree[r[0]] = (r[1], "1", njoin[0])
	
	tree[njoin[0]] = (njoin[1])
	print tree
	
	code = ""	
	for s in string:
		s1 = s
		co = ""
		while(tree[s1] != 1.0):
			co += tree[s1][1]
			s1 = tree[s1][2]
		
		code += co[::-1]
	
	return (code, tree)
	
	
'''
def runlength(string):
	
	res = ""
	curr = string[0]
	i = 1
	for k in range(1, len(string)):
		if curr != string[k]:
			if i == 1:
				if string[k-1] == "0":
					res += "A"
				else:
					res += "B"
			else:
				if string[k-1] == "0":
					res += str(i)+"A"
				else:
					res += str(i)+"B"
			i = 1
			curr = string[k]
		else:			
			i += 1
			continue
	if i == 1:
		if string[k] == "0":
			res += "A"
		else:
			res += "B"
	else:
		if string[k] == "0":
			res += str(i)+"A"
		else:
			res += str(i)+"B"
		
	return res
'''

def binary(string):
	res = ""
	store = ""
	i = 1
	
	for s in string:
		store += s
		
		if i == 65:
			res += str(int(store, 2))

			store = ""
			i = 1
		
		i += 1
	
	res += str(int(store,2))
	
	return res
	
	
with open(str(sys.argv[1])) as f:
	line = f.readline()
	
	line = line.replace("\n", "")
	
	line += "$"
	
	sigma = computeSigma(line)
	
	#returns bwt string and index with original string
	bwt = encodeBWT(line)
	
	C = computeC(line)
	
	#print LF
	code = mtf(bwt)	
	
	hcode = huffman(code[0])
	print hcode[0]
	
	s = int(hcode[0],2 )
	
	#print s
	
	#print int(hcode, 2)
	#print runlength(hcode)
	
	with open("encoding.txt",  "w") as out:
		out.write(str(len(hcode[1].items()))+"\n")
		treeoutput = ''
		for item in hcode[1].items():
			if item[1] != 1.0:
				treeoutput += item[0]+" "+item[1][1]+" "+item[1][2]+"\n"
			else:
				treeoutput = item[0]+" "+str(item[1])+"\n" + treeoutput
		
		out.write(treeoutput)
		out.write(str(C))
		out.write("\n")
		out.write(str(sigma))
		out.write("\n")
		out.write(str(int(hcode[0], 2)))
	
	#binary(hcode)

