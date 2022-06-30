import Astar
if __name__ == '__main__':
	a = Astar.A(Astar.Node([[1,2,3],[8,0,4],[7,6,5]]), Astar.Node([[1,2,3],[8,0,4],[7,6,5]]))
	if a.isSame():
		a.showSteps()
	else:
		print ("A* start:")
		a.start()
		#a.showPath()
		a.showSteps()
