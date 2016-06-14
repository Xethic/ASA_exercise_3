import sys

#computes sigma of given string with all characters
def computeSigma(text):
	sigma = []
	
	for s in sorted(text):
		if s not in sigma:
			sigma.append(s)
	
	return sigma


#BWT encoding, returns BWT
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
		

#computes C table, for each character the number of lexicographically smaller characters
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
	

#move to front encoding, returns encoded string and used alphabet
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
	
	
#huffman encoding
#tree is structured as following:
#dictionary with k as the lable of the node, respective characters
#value is its parent, 0 or 1 as the description of the path and the probability of the node 
#returns encoded string and the used tree
def huffman(string):
	freq = dict()
	
	sort = sorted(string)
	l = len(sort)
	
	for s in sort:
		if s not in freq:
			freq[s] = float(sort.count(s)) / float(l)
		
	liste = freq.items()
	
	sfreq = sorted(liste, key = lambda tup: tup[1])
	
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
'''
	
#main
#command line should have one argument with the given string that should be compressed	
with open(str(sys.argv[1])) as f:
	line = f.readline()
	
	line = line.replace("\n", "")
	
	line += "$"
	
	#computation of alphabet
	sigma = computeSigma(line)
	
	#BWT
	bwt = encodeBWT(line)
	
	#C table
	C = computeC(line)
	
	#move to front
	code = mtf(bwt)	
	
	#huffman encoding
	hcode = huffman(code[0])
	
	#length of huffman string
	length = len(hcode[0])
	
	#converts bit string into an integer
	s = int(hcode[0],2 )
	
	#write needed information to the file
	with open("encoding.txt",  "w") as out:
		#stores the huffman tree
		out.write(str(len(hcode[1].items()))+"\n")
		treeoutput = ''
		for item in hcode[1].items():
			if item[1] != 1.0:
				treeoutput += item[0]+" "+item[1][1]+" "+item[1][2]+"\n"
			else:
				treeoutput = item[0]+" "+str(item[1])+"\n" + treeoutput
		
		out.write(treeoutput)
		
		#stores C table, sigma, bitstring length and converted integer as final encoding
		out.write(str(C))
		out.write("\n")
		out.write(str(sigma))
		out.write("\n")
		out.write(str(length))
		out.write("\n")
		out.write(str(s))
	
	

