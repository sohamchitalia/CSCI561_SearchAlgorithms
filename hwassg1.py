from operator import attrgetter
inpfile = open("input.txt","r") 
inpdata = inpfile.readlines()
inpfile.close()
algoname = str(inpdata[0])

w = int(inpdata[1].split()[0])
h = int(inpdata[1].split()[1])
lx = int(inpdata[2].split()[0])
ly = int(inpdata[2].split()[1])
maxel = int(inpdata[3])
numtarget = int(inpdata[4])

targetlist = []
for i in range(5, 5+numtarget):
	target = []
	target.append(int(inpdata[i].split()[0]))
	target.append(int(inpdata[i].split()[1]))
	targetlist.append(target)
grid = []
for i in range(5+numtarget, 5+numtarget+h):
	elevations = []
	r = inpdata[i].split()
	for j in range(w):
		elevations.append(int(r[j]))
	grid.append(elevations)

class Node:
	def __init__(self, x,y, height, dist, h, f, parent):
		self.x = x
		self.y = y
		self.height = height
		self.dist = dist
		self.parent = parent
		self.h = h
		self.f = f

def bfs(source, targetx, targety, elevation, grid):

	visited = []
	for i in range(h):
		op = []
		for j in range(w):
			op.append(False)
		visited.append(op)
	q = [source]
	visited[source.y][source.x] = True
	while q:
		p = q.pop(0)
		if p.x == targetx and p.y == targety:
			return p
		# check all 8 directions #
		#north y - 1#
		if p.y - 1 >= 0 and visited[p.y - 1][p.x] == False:
			if abs(grid[p.y - 1][p.x] - p.height) <= elevation:
				q.append(Node(p.x, p.y - 1, grid[p.y - 1][p.x], p.dist + 1, 0, p.dist + 1, p))
				visited[p.y - 1][p.x] = True

		# south y + 1
		if p.y + 1 < h and visited[p.y + 1][p.x] == False:
			if abs(grid[p.y + 1][p.x] - p.height) <= elevation:
				q.append(Node(p.x, p.y + 1, grid[p.y + 1][p.x], p.dist + 1, 0, p.dist + 1, p))
				visited[p.y + 1][p.x] = True

		# east x + 1
		if p.x + 1 < w and visited[p.y][p.x + 1] == False:
			if abs(grid[p.y][p.x + 1] - p.height) <= elevation:
				q.append(Node(p.x + 1, p.y, grid[p.y][p.x + 1], p.dist + 1, 0, p.dist + 1, p))
				visited[p.y][p.x + 1] = True

		# west x - 1
		if p.x - 1 >= 0 and visited[p.y][p.x - 1] == False:
			if abs(grid[p.y][p.x - 1] - p.height) <= elevation:
				q.append(Node(p.x - 1, p.y, grid[p.y][p.x - 1], p.dist + 1, 0, p.dist + 1, p))
				visited[p.y][p.x - 1] = True
		
		# northwest y-1, x-1
		if p.x - 1 >= 0 and p.y - 1 >= 0 and visited[p.y - 1][p.x - 1] == False:
			if abs(grid[p.y - 1][p.x - 1] - p.height) <= elevation:
				q.append(Node(p.x - 1, p.y - 1, grid[p.y - 1][p.x - 1], p.dist + 1, 0, p.dist + 1, p))
				visited[p.y - 1][p.x - 1] = True


		# northeast y - 1, x + 1

		if p.x + 1 < w and p.y - 1 >= 0 and visited[p.y - 1][p.x + 1] == False:
			if abs(grid[p.y - 1][p.x + 1] - p.height) <= elevation:
				q.append(Node(p.x + 1, p.y - 1, grid[p.y - 1][p.x + 1], p.dist + 1, 0, p.dist + 1, p))
				visited[p.y - 1][p.x + 1] = True


		# southwest y+1, x-1

		if p.x - 1 >= 0 and p.y + 1 < h and visited[p.y + 1][p.x - 1] == False:
			if abs(grid[p.y + 1][p.x - 1] - p.height) <= elevation:
				q.append(Node(p.x - 1, p.y + 1, grid[p.y + 1][p.x - 1], p.dist + 1, 0, p.dist + 1, p))
				visited[p.y + 1][p.x - 1] = True


		# southeast y + 1, x + 1

		if p.x + 1 < w and p.y + 1 < h and visited[p.y + 1][p.x + 1] == False:
			if abs(grid[p.y + 1][p.x + 1] - p.height) <= elevation:
				q.append(Node(p.x + 1, p.y + 1, grid[p.y + 1][p.x + 1], p.dist + 1, 0, p.dist + 1, p))
				visited[p.y + 1][p.x + 1] = True

	return "FAIL"

def ucs(source, targetx, targety, elevation, dist): ### Check loop detection ###
	
	openq = [source]
	visited = [[0 for i in range(w)] for j in range(h)]
	openmat = [[0 for i in range(w)] for j in range(h)]
	openq = [source]

	visited[source.y][source.x] = source
	openmat[source.y][source.x] = source
	while openq:
		p = openq.pop(0)
		openmat[p.y][p.x] = False
		if p.x == targetx and p.y == targety:
			return p
		# check all 8 directions #
		
		xarr = [0, 0, 1, -1, -1, 1, -1, 1]
		yarr = [-1, 1, 0, 0, -1, -1, 1, 1]

		# check all 8 directions #
		for i in range(8):
			if xarr[i] == 0 or yarr[i] == 0:
				adddist = 10
			else:
				adddist = 14
			
			if 0 <= p.x + xarr[i] < w and 0<= p.y + yarr[i] < h and visited[p.y + yarr[i]][p.x + xarr[i]] == False:
				htdiff = abs(grid[p.y + yarr[i]][p.x + xarr[i]] - p.height)
				if htdiff <= elevation: 
					g = p.dist + adddist
					child = Node(p.x + xarr[i], p.y + yarr[i], grid[p.y + yarr[i]][p.x + xarr[i]], g , 0, g, p)
					# visited[p.y + yarr[i]][p.x + xarr[i]] = True
					if openmat[child.y][child.x] == False and visited[child.y][child.x] == False:
						openq.append(child)
						openmat[child.y][child.x] = child
					elif openmat[child.y][child.x] != False:
						i = openmat[child.y][child.x]
						if i.f > child.f:
							openq.remove(i)
							# heapq.heappush(openq, child)
							openq.append(child)
							openmat[child.y][child.x] = child
					

		# Added all 8 directions to children queue

		visited[p.y][p.x] = p #appending current node to closed Queue
		openq.sort(key = attrgetter('f')) # sort in-place
		
	return "FAIL"


# A star #
def heuristic(nx, ny, targetx, targety):
	
	dx = abs(nx - targetx)
	dy = abs(ny - targety)
	return 10 * (dx + dy) + (14 - 2 * 10) * min(dx, dy)
	

def astar(source, targetx, targety, elevation, grid):
	# h is the heuristic function max(Xdis, Ydis)
	visited = [[0 for i in range(w)] for j in range(h)]
	openmat = [[0 for i in range(w)] for j in range(h)]
	openq = [source]
	
	visited[source.y][source.x] = source
	openmat[source.y][source.x] = source
	while openq:
		
		p = openq.pop(0)
		openmat[source.y][source.x] = 0
		if p.x == targetx and p.y == targety:
			return p
		visited[p.y][p.x] = p
		xarr = [0, 0, 1, -1, -1, 1, -1, 1]
		yarr = [-1, 1, 0, 0, -1, -1, 1, 1]
		# check all 8 directions #
		
		for i in range(8):
			if xarr[i] == 0 or yarr[i] == 0:
				adddist = 10
			else:
				adddist = 14
			cx = p.x + xarr[i]
			cy = p.y + yarr[i]
			if 0 <= cx < w and 0<= cy < h and visited[cy][cx] == 0:
				htdiff = abs(grid[cy][cx] - p.height)
				if htdiff <= elevation: 
					heu = heuristic(cx, cy, targetx, targety)
					g = p.dist + adddist + htdiff
					f = heu + g
					child = Node(cx, cy, grid[cy][cx], g , heu, f, p)
					if openmat[child.y][child.x] == 0 and visited[child.y][child.x] == 0:
						openq.append(child)
						openmat[child.y][child.x] = child
					elif openmat[child.y][child.x] != 0:
						i = openmat[child.y][child.x]
						if i.f > child.f:
							openq.remove(i)
							openq.append(child)
							openmat[child.y][child.x] = child
		
		visited[p.y][p.x] = p #appending current node to closed Queue
		openq.sort(key = attrgetter('f')) # sort in-place

	return "FAIL"

# end A star #
def printPath(node, st):
	while node != None:
		st = '{},{} '.format(node.x, node.y) + st
		node = node.parent
	return st

def main():
	f = open("output.txt", "w")
	if algoname[0] == "B":
		counter = numtarget
		for j in targetlist:
			st = ""
			source = Node(lx,ly,grid[ly][lx],0, 0, 0, None)
			n = bfs(source, j[0], j[1], maxel, grid)
			if n != "FAIL":
				l = printPath(n, st)
				f.write(l)
			else:
				f.write("FAIL")
			if counter > 1:
				f.write("\n")
			counter = counter - 1	

	elif algoname[0] == "U":
		counter = numtarget
		for j in targetlist:
			st = ""
			source = Node(lx,ly,grid[ly][lx],0, 0, 0, None)
			n = ucs(source, j[0], j[1], maxel, grid)
			if n != "FAIL":
				l = printPath(n, st)
				f.write(l)
			else:
				f.write("FAIL")
			if counter > 1:
				f.write("\n")
			counter = counter - 1
			
	elif algoname[0] == "A":
		
		counter = numtarget
		for j in targetlist:
			st = ""
			sdist = heuristic(lx, ly, j[0], j[1])
			source = Node(lx,ly,grid[ly][lx],0, sdist, sdist, None)
			n = astar(source, j[0], j[1], maxel, grid)
			if n != "FAIL":
				
				l = printPath(n, st)
				f.write(l)
				
			else:
				f.write("FAIL")
			if counter > 1:
				f.write("\n")
			counter = counter - 1
	f.close()


	
if __name__ == "__main__":
	main()









		







		





















		







		


















