import ast
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


def decodeBWT(bwt, LF):
	s = "$"
	i = 0
	print LF
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
	

def decodeHuffmann(tree, root, seq):
	encodedstring = ''
	print 'HUFFMANN'
	print str(tree)
	pointer = root
	for i in range(len(seq)):
					
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
	
	return encodedstring


with open(str(sys.argv[1])) as f:
	line = f.readline()
	line = line.replace("\n", "")
	
	treelength = int(line)
	tree = {}
	
	line = f.readline()
	line = line.replace("\n", "")
	line = line.split()
	root = line[0]
	
	for i in range(treelength-1):
		line = f.readline()
		line = line.replace("\n", "")
		line = line.split()
		if(not tree.has_key(line[2])):
			tree[line[2]] = (line[0], line[1])
		else:
			tree[line[2]] = (tree[line[2]], (line[0], line[1]))
	
	line = f.readline()
	line = line.replace("\n", "")
	C = ast.literal_eval(line)
	#print C
	
	line = f.readline()
	line = line.replace("\n", "")
	sigma = ast.literal_eval(line)
	#print sigma
	
	line = f.readline()
	line = line.replace("\n", "")
	line = int(line)
	
	get_bin = lambda x: format(x, "b")
	s = get_bin(line)
	
	print s
	decH = decodeHuffmann(tree, root, s)
	
	print decH
	
	decimtf = [decH, sigma]
	
	bwt = imtf(decimtf)
	
	print bwt
	
	LF = LF(bwt, C, sigma)
	
	decodedstring = decodeBWT(bwt, LF)
	
	with open("decoding.txt",  "w") as out:
		out.write(decodedstring[:-1])
