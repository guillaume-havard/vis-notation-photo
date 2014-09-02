from tulip import *

class OutilsGraph:
	"""
	Classe de manipulation de graphique/ensemble de noeud
	"""
	def __init__(self, graph):
	   	
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
	
	
			
	def arrangement_location(self, param):
		"""
		Place les elements du graphique en fonction de leur localisation		
		"""
		
		if len(param) != 2 :
			raise Exception('Attention !', 'Vous ne devez avoir que 2 parametres') 
		
		varx = graph.getDoubleProperty(param[0])	
		vary = graph.getDoubleProperty(param[1])			
		
		coord = tlp.Coord()				
		for n in self.graph.getNodes():			
			x = varx.getNodeValue(n)
			y = vary.getNodeValue(n)
			coord.set(x, y, 0.)
			self.viewLayout.setNodeValue(n, coord)			
		
		# On recentre la vue.	
		updateVisualization(centerViews = True)
		
	def hauteur_cylindres(self):
		"""
		Donne au noeud une hauteur en fonction de size.
		"""
		
		for n in self.graph.getNodes():
			siz = tlp.Size(1, 1, self.size.getNodeValue(n) / 10)		
			self.viewSize.setNodeValue(n, siz)
			x = self.viewLayout.getNodeValue(n).getX()
			y = self.viewLayout.getNodeValue(n).getY()
			z = - (self.size.getNodeValue(n) / 20) /2
			coor = tlp.Coord(x, y, z)
			self.viewLayout.setNodeValue(n, coor)
			
		# On recentre la vue.	
		updateVisualization(centerViews = True)
		
	def raz_hauteur(self):
		"""
		Remet a zero les positions en Z des points.
		"""
		for n in self.graph.getNodes():			
			x = self.viewLayout.getNodeValue(n).getX()
			y = self.viewLayout.getNodeValue(n).getY()
			z = 0
			coor = tlp.Coord(x, y, z)
			self.viewLayout.setNodeValue(n, coor)
		
	def proportion_good_size(self, pas):
		"""		
		Essayer de rendre le code generique pour toute variable avec une liste de string au debut.		
		
		Repartie la population en fonction de la taille de l'album avec un pas de 'pas'.
		"""
		
		# Recuperation du max. peut etre fait en meme temps.
		max = 0
		for n in self.graph.getNodes():
			if max < self.size.getNodeValue(n):
				max = self.size.getNodeValue(n) 
				
		repartition = []
		repartition_good = []
		repartition_not_good = []
		
		interval = int(max / pas)
		
		print "max : ", max, ", intervals : ", interval 
		
		for i in range(interval):
			repartition.append([])
			repartition_good.append([])
			repartition_not_good.append([])
			
		# On va mettres les points dans les intervals en fonction de la size.
		for n in self.graph.getNodes():
			if self.size.getNodeValue(n)	:			
				index = int(self.size.getNodeValue(n)/pas)
			else :
				index = 0			
			if index >= interval :
				index = interval - 1
						
			repartition[index].append(n)
						
			if self.good.getNodeValue(n):
				repartition_good[index].append(n)
			else:
				repartition_not_good[index].append(n)			
		
		# A la fin : analyse, on sort le nombre par interval.
		valeurs = []		
		for i in range(len(repartition)):
			valeurs.append([len(repartition[i]),len(repartition_good[i]),len(repartition_not_good[i])])
		
		# Affichage des resultats.
		for i in range(len(valeurs)):
			print valeurs[i][0], ", ", valeurs[i][1], ", ", valeurs[i][2]
		
		
		
def main(graph) : 
	g = OutilsGraph(graph)
		
	g.arrangement_location(["longitude", "latitude"])
	
	#g.proportion_good_size(10)
	
	# Pour les cylindres.
    #g.hauteur_cylindres()
	#g.raz_hauteur()
