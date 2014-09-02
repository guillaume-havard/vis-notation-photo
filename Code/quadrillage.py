from tulip import *

class Quadrillage :
	"""
	Classe effectuant un quadrillage et un coloriage des zones
	"""
	def __init__(self, graph) :
		self.graph = graph		
		self.good = graph.getDoubleProperty("good")
		self.height = graph.getDoubleProperty("height")
		self.id_ = graph.getDoubleProperty("id")
		self.latitude = graph.getDoubleProperty("latitude")
		self.longitude = graph.getDoubleProperty("longitude")
		self.size =  graph.getDoubleProperty("size")	
		self.viewLayout =  graph.getLayoutProperty("viewLayout")
		self.viewColor =  graph.getColorProperty("viewColor")
		self.viewSize =  graph.getSizeProperty("viewSize")
		self.viewShape =  graph.getIntegerProperty("viewShape")
		self.viewNbAlbum =  graph.getIntegerProperty("viewNbAlbum")
		self.viewLongitude =  graph.getDoubleProperty("longitude")
		self.viewLatitude =  graph.getDoubleProperty("latitude")
		
		self.xmin = 10000
		self.xmax = -10000
		self.ymin = 10000
		self.ymax = -10000
		self.distX = 0
		self.distY = 0
		self.zoneX = 10
		self.zoneY = 10
		self.nbZoneX = 0
		self.nbZoneY = 0
		self.listZone = []
		self.decalX = 0
		self.decalY = 0
		self.listMoy = []
		self.seuil = 3
	
	# function set the graph's borders and calculate the distance between them
	def setLimites(self) :
		for n in self.graph.getNodes() :
			if(self.viewLayout.getNodeValue(n).getX() < self.xmin) : self.xmin = self.viewLayout.getNodeValue(n).getX()
			if(self.viewLayout.getNodeValue(n).getX() > self.xmax) : self.xmax = self.viewLayout.getNodeValue(n).getX()
			if(self.viewLayout.getNodeValue(n).getY() < self.ymin) : self.ymin = self.viewLayout.getNodeValue(n).getY()
			if(self.viewLayout.getNodeValue(n).getY() > self.ymax) : self.ymax = self.viewLayout.getNodeValue(n).getY()
		
		self.distX = (self.xmin - self.xmax) * (-1)
		self.distY = (self.ymin - self.ymax) * (-1)
	
	# function computing the number of zones required to make the new graph
	def setNbZones(self) :
		if(self.distX % self.zoneX == 0) : self.nbZoneX = (int)(self.distX / self.zoneX)
		else : self.nbZoneX = (int)(self.distX / self.zoneX) + 1
		if(self.distY % self.zoneY == 0) : self.nbZoneY = (int)(self.distY / self.zoneY)
		else : self.nbZoneY = (int)(self.distY / self.zoneY) + 1
		
		# create list of zones : [[x, y] nodes[]]
		for x in range(self.nbZoneX) :
			tmp = []
			for y in range(self.nbZoneY) :
				tmp.append([])
			self.listZone.append(tmp)
	
	# function used for moving the graph, lower-left coordinates at (0, 0)
	def setDecalage(self) :
		self.decalX = 0 - self.xmin
		self.decalY = 0 - self.ymin
		
		for n in self.graph.getNodes() :
			coord = self.viewLayout.getNodeValue(n)
			
			coord.setX(self.viewLayout.getNodeValue(n).getX() + self.decalX)
			coord.setY(self.viewLayout.getNodeValue(n).getY() + self.decalY)
			
			self.viewLayout.setNodeValue(n,coord)
			
		updateVisualization(centerViews = True)
	
	# function used to get in which zone the nodes are and add them to the zone's node list
	def getPointsInZones(self) :
		x = 0
		y = 0
		
		for n in self.graph.getNodes() :
			if(self.viewLayout.getNodeValue(n).getX() % self.zoneX == 0) : x = (int)(self.viewLayout.getNodeValue(n).getX() / self.zoneX)
			else : x = (int)(self.viewLayout.getNodeValue(n).getX() / self.zoneX)
			if(self.viewLayout.getNodeValue(n).getY() % self.zoneY == 0) : y = (int)(self.viewLayout.getNodeValue(n).getY() / self.zoneY)
			else : y = (int)(self.viewLayout.getNodeValue(n).getY() / self.zoneY)
			
			self.listZone[x-1][y-1].append(n)
	
	# function used to create a list of average : [[x, y] average]
	def getMoy(self) :
		x = 0
		y = 0
		sum = 0
		
		for x in range(self.nbZoneX) :
			tmp = []
			for y in range(self.nbZoneY) :
				tmp.append([])
			self.listMoy.append(tmp)
		
		x = 0
		
		for lz in self.listZone :
			y = 0
			
			for ln in lz :
				if(len(ln) == 0) : self.listMoy[x][y] = -1
				elif(len(ln) <= self.seuil) : self.listMoy[x][y] = -1
				else :
					for n in ln :
						sum = sum + self.good.getNodeValue(n)
					sum = sum / len(ln)
					self.listMoy[x][y] = sum
					sum = 0
					
				y = y + 1
			x = x + 1
	
	# function used to draw the graph
	def graphQuadri(self) :
		quadrillage = tlp.newSubGraph(graph, "quadrillage")
		
		viewLocalLayout =  quadrillage.getLocalLayoutProperty("viewLayout")
		
		moyGood = quadrillage.getDoubleProperty("Moyenne good")
		
		for x in range(self.nbZoneX) :
			for y in range(self.nbZoneY) :
				if(self.listMoy[x][y] != -1) :
					n = quadrillage.addNode()
					coord = self.viewLayout.getNodeValue(n)
					coord.setX((x+1) * (self.zoneX / 2))
					coord.setY((y+1) * (self.zoneY / 2))
					viewLocalLayout.setNodeValue(n, coord)
					coord.setX(-100)
					coord.setY(-100)
					self.viewLayout.setNodeValue(n, coord)
					moyGood.setNodeValue(n, self.listMoy[x][y])
					siz = tlp.Size(self.zoneX/2, self.zoneX/2, 1)
					self.viewSize.setNodeValue(n, siz)
					self.viewNbAlbum.setNodeValue(n, len(self.listZone[x][y]))
					self.viewLongitude.setNodeValue(n, self.longitude.getNodeValue(self.listZone[x][y][0]))
					self.viewLatitude.setNodeValue(n, self.latitude.getNodeValue(self.listZone[x][y][0]))


def main(graph) : 
	g = Quadrillage(graph)
	
	g.setLimites()
	
	g.setNbZones()
	
	g.setDecalage()
	
	g.getPointsInZones()
	
	g.getMoy()
	
	g.graphQuadri()

