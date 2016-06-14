import ast
import sys

#compute LF table
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


#decoding of BWT string with LF mapping
def decodeBWT(bwt, LF):
	s = "$"
	i = 0
	print LF
	while len(s) < len(bwt):
		s = bwt[i] + s
		i = LF[i]
		
	return s


#inverted move to front algorithm
def imtf(s):
	code = s[0]
	l = list(s[1])
	
	string = ""
	r = 0
	
	for i in code:
		r = int(i)
		string += str(l[r])
		
		k = l[int(i)]
		l.pop(int(i))
		l.insert(0,k)
	
	return string
	

#Huffman decoding with the given Huffman tree, its root and the given sequence to decode
def decodeHuffmann(tree, root, seq):
	encodedstring = ''
	print 'HUFFMANN'
	print str(tree)
	pointer = root
	nextnode = root
	for i in range(len(seq)):
		
		if pointer in tree:			
			nextnodes = tree[pointer]
			
			if(len(nextnodes[0][0]) == 1 and nextnodes[0][1] == seq[i]):
				encodedstring += nextnodes[0][0]
				pointer = root
				
			elif(len(nextnodes[1][0]) == 1 and nextnodes[1][1] == seq[i]):
				encodedstring += nextnodes[1][0]
				pointer = root
				
			elif(nextnodes[0][1] == seq[i]):
				pointer = nextnodes[0][0]
				#print nextnodes[0][0]
				#print nextnodes[0][1]
				#print seq[i]
				
			else:
				pointer = nextnodes[1][0]
				#print nextnodes[1][0]
				#print nextnodes[1][1]
		else:
			encodedstring += nextnodes[0][0]
			pointer = root
			
			
	
	return encodedstring


#main
#command line should have one argument with the compressed file
with open(str(sys.argv[1])) as f:
	line = f.readline()
	line = line.replace("\n", "")
	
	treelength = int(line)
	tree = {}
	
	line = f.readline()
	line = line.replace("\n", "")
	line = line.split()
	root = line[0]
	
	#read tree, stored in a dictionary	
	for i in range(treelength-1):
		line = f.readline()
		line = line.replace("\n", "")
		line = line.split()
		if(not tree.has_key(line[2])):
			tree[line[2]] = (line[0], line[1])
		else:
			tree[line[2]] = (tree[line[2]], (line[0], line[1]))
	
	
	#read C table
	line = f.readline()
	line = line.replace("\n", "")
	C = ast.literal_eval(line)
	
	
	#read sigma of given sequence
	line = f.readline()
	line = line.replace("\n", "")
	sigma = ast.literal_eval(line)
	
	#length of original bit sequence 
	length = f.readline()
	
	#last readline reads the final code
	line = f.readline()
	line = line.replace("\n", "")
	line = int(line)
	
	#convert code number into binary string
	get_bin = lambda x: format(x, "b")
	s = get_bin(line)

	#add 0 to the front if binary string is not as long as original bit string
	while len(s) < int(length):
		s = "0"+s
		print s			
	
	#Huffman decoding
	decH = decodeHuffmann(tree, root, s)	
	
	#move to front decoding
	decimtf = [decH, sigma]
	bwt = imtf(decimtf)
	
	#LF mapping
	LF = LF(bwt, C, sigma)
	
	#BWT decoding
	decodedstring = decodeBWT(bwt, LF)
	
	#write decoded string to file
	with open("decoding.txt",  "w") as out:
		out.write(decodedstring[:-1])
