'''
Find the shortest path from point A (source) to point B (destination)
on a chessboard (8x8 board) using only moves for a knight.

Solved as part of Google's coding challenges (hence the weird file name...).
'''

# eight possible 'knight' moves
def move1(r, c, board):
	if 0 <= r + 1 < 8 and 0 <= c + 2 < 8:
		return board[r+1][c+2]
	return -1

def move2(r, c, board):
	if 0 <= r + 2 < 8 and 0 <= c + 1 < 8:
		return board[r+2][c+1]
	return -1

def move3(r, c, board):
	if 0 <= r - 2 < 8 and 0 <= c + 1 < 8:
		return board[r-2][c+1]
	return -1

def move4(r, c, board):
	if 0 <= r - 2 < 8 and 0 <= c - 1 < 8:
		return board[r-2][c-1]
	return -1

def move5(r, c, board):
	if 0 <= r + 1 < 8 and 0 <= c - 2 < 8:
		return board[r+1][c-2]
	return -1

def move6(r, c, board):
	if 0 <= r + 2 < 8 and 0 <= c - 1 < 8:
		return board[r+2][c-1]
	return -1

def move7(r, c, board):
	if 0 <= r - 1 < 8 and 0 <= c - 2 < 8:
		return board[r-1][c-2]
	return -1

def move8(r, c, board):
	if 0 <= r - 1 < 8 and 0 <= c + 2 < 8:
		return board[r-1][c+2]
	return -1

# list of all valid moves for a node
def moves(node, board):
		try:
			r, c = next((i, pos.index(node)) for i, pos in enumerate(board) if node in pos) # current position on board
			return [i(r, c, board) for i in [move1, move2, move3, move4, move5, move6, move7, move8] if i(r, c, board) != -1] # all valid nodes from this node
		except:
			return []

def answer(src, dest):
	board = [[row*8+col for col in range(8)] for row in range(8)] # initialize the board
	
	distances = {i: float('inf') for i in range(64)} # all available nodes with initial dist = infinity
	distances[src] = 0 # distance at the source = 0

	#paths = {i: [] for i in range(64)} # all available nodes with initial dist = infinity
	#paths[src] = [src]
	#print paths
	
	visited = set() # nodes that have been visited, initialized as empty


	while len(visited) < 64: # while there are still nodes to visit
		for u in distances:  
			if not u in visited and distances[u] != float('inf'): # pick a vertex that has a distance value and hasn't been visited visited
				visited.add(u) 
				#paths[u].insert(0, u)
				nextNodes = moves(u, board)
				for node in nextNodes:	# update distances for all the moves reachable from that node
					if distances[u] + 1 < distances[node]:
						#paths[node] = paths[u]
						#paths[node].append(u)
						distances[node] = distances[u] + 1


	#print "paths 0: ", paths[0]
	#print "paths 10: ", paths[10]
	return distances[dest]

def test():
	print answer(0, 1)
	print answer(1, 0)
	print answer(0, 12)
	print answer(12, 0)
	print answer(0, 25)
	print answer(25, 0)



test()





		

		






















