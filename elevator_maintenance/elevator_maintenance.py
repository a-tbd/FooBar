import itertools

class Node:
	def __init__(self, major, minor=-1, revision=-1):
		self.major = major
		self.minor = minor
		self.revision = revision

	def __repr__(self):
		string = "%s%s" % ('"', str(self.major))
		if self.minor != -1:
			string = "%s.%s" % (string, self.minor)

		if self.revision != -1:
			string = "%s.%s" % (string, self.revision)
		string = "%s%s" % (string, '"')
		return string

# list of str --> list of obj for elevator manuals
def addNode(node):
	if len(node) == 1:
		return Node(node[0])
	elif len(node) == 2:
		return Node(node[0], node[1])
	else:
		return Node(node[0], node[1], node[2])

# node obj --> int aspect
def major(node):
	return int(node.major)

def minor(node):
	if node.minor != -1:
		return int(node.minor)
	else:
		return node.minor

def revision(node):
	if node.revision != -1:
		return int(node.revision)
	else:
		return node.revision

# insertion sort for instances of Node() according to the specified aspect: major, minor revision
def sort(l, aspect):
	for i in range(1, len(l)):  
		temp = l[i]
		j = i - 1	
		while j >= 0 and aspect(l[j]) > aspect(temp): 
			l[j+1] = l[j]
			j -= 1
		l[j+1] = temp
	
	return l

def answer(l):
	# convert list of str --> list of obj instances
	revisionList = [item.split(".") for item in l]
	nodeList = [addNode(item) for item in revisionList]

	# sort and group by major number in ascending order
	sort(nodeList, major)
	nodesByMajor = [list(g) for k, g in itertools.groupby(nodeList, lambda x: x.major)]

	# sort and group by minor number in ascending order
	nodesByMinor = []
	for node in nodesByMajor:
		sort(node, minor)
		nodesByMinor.append([list(g) for k, g in itertools.groupby(node, lambda x: x.minor)])

	# sort and group by revision number in ascending order
	for node in nodesByMinor:
		for innerNode in node:
			if len(innerNode) > 1:
				sort(innerNode, revision)

	# combine sorted lists
	return [str(node) for item in nodesByMinor for i in item for node in i]
	


l = ["0", "5.6.3", "5.7.3", "1.0", "5.6.1", "1", "3.1", "1.0.0", "2.0", "5.6.2", "2.0.1"] #11 items

print answer(["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"])
print answer(["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"])

#print sort([3, 2, 0, 1])
#print sort([3, 5, 10, 0, 2, 6, -4, 0, 1])
print type(answer(l)[0])

