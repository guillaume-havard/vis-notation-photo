from tulip import *


class GraphMots:
	"""
	Classe pour creer un graph album/mots.
	"""
	
	def __init__(self, graph):
		
		self.graph = graph 
		
		# Fichier csv contenant les donnees.
		self.donnees_mots = "/home/guillaume/Tulip-3.7.0/Workspace/Projet/mots.csv"
		
		# Listes des identifiants.
		self.name = []
		self.description = []
		self.caption = []
		self.tout = []
		
		self.donnees_good = []
		
		# Dictionaire des noeuds.
		self.albums = []
		self.mots = []		
		self.ref = {}
		
		# Properties des noeuds.
		self.viewColor =  graph.getColorProperty("viewColor")
		self.good =  graph.getDoubleProperty("good")
		self.est_album =  graph.getDoubleProperty("est_album")
		self.identifiant =  graph.getDoubleProperty("identifiant")
		self.type_mot = graph.getDoubleProperty("type_mot")
		self.degree = graph.getDoubleProperty("degree")
		
		self.subGraph_simple = tlp.newSubGraph(self.graph, "grosDeGreeMot")
		self.subGraph_albums = None

		self.ratio = 0.5
		self.seuil_degree = 10
		
	def extraction_donnees_fichier(self):
		"""
		Extrait les donnees de "donnees_mots" et les range dans les tableaux d'identifiants correspondant.
		"""	
		
		f_in = open(self.donnees_mots, 'r')
		if not f_in : raise Exception("Mots.exraction_donnees : echec de l'ouverture du fichier")
		
		f_in.readline()
		line = f_in.readline()
		
		while len(line):
			info = line.split(",")	
			
			tout = []
			# name
			name = []
			if info[1] != " ":
				texte = info[1].split(" ")
				for id in texte:
					name.append(id)
					if not tout.count(id):
						tout.append(id)
      		
				self.name.append(name)
      		
			# description
			description = []
			if info[2] != " ":
				texte = info[2].split(" ")
				for id in texte:
					description.append(id)
					if not tout.count(id):
						tout.append(id)
      				
				self.description.append(description)
      		
			# caption
			caption = []
			if info[3] != " ":
				texte = info[3].split(" ")
				for id in texte:
					caption.append(id)
					if not tout.count(id):
						tout.append(id) 
      				
				self.caption.append(caption)
	
			# tout
			if len(tout):
				self.tout.append(tout)
      	
			# good	
			self.donnees_good.append(info[4])
      	
			line = f_in.readline()      
		f_in.close()	
	
	def extraction_donnees_graph(self):
		"""
		Extrait les donnees du graph et les range dans les tableaux d'identifiants correspondant.
		"""	
		
		for n in self.graph.getNodes():
			if self.est_album[n]:
				self.albums.append(n)
			
			else:
				if self.type_mot[n] == 1:
					self.name.append(n)	
				if self.type_mot[n] == 2:
					self.name.description(n)
				if self.type_mot[n] == 3:
					self.name.caption(n)
				
				self.mots.append(n)
				self.tout.append(n)
		
	def donnees_en_graphe(self, liste):
		""" Transforme les donnees en un graphe. """
	
		for i in range(len(liste)):
			n = self.graph.addNode()
			self.albums.append(n)
			self.est_album[n] = 1
			self.identifiant[n] = i
			for e in range(len(liste[i])):
				if not self.ref.has_key(liste[i][e]):
				#if not self.mots.count(self.ref[liste[i][e]]): 
					m = self.graph.addNode()				
					self.mots.append(m)
					self.est_album[m] = 0
					self.identifiant[m] = int(liste[i][e])
					self.ref[liste[i][e]] = m
					
				self.graph.addEdge(n, self.ref[liste[i][e]])
   
			self.good[n] = int(self.donnees_good[i])
			
		#self.__ajout_categories__()
		
	def __ajout_categories__(self):
		"""
		Met la bonne categorie de mot.
		"""
		
		for n in self.name:
			self.type_mot[n] = 1
			
		for n in self.description:
			self.type_mot[n] = 2
			
		for n in self.caption:
			self.type_mot[n] = 3
			
	def calcul_moyenne_good(self):
		"""
		Calcul les moyennes de good pour chaque mots.
		"""
			
		for mot in self.mots:
			somme = 0.0
			tot = 0.0
			for pred in graph.getInNodes(mot):
				somme += self.good[pred]
				tot += 1.0
		
			self.good[mot]	= somme/tot
			

	def mise_en_forme_noeuds(self):
		"""
		Colorise les albums 
		"""
		
		rouge = tlp.Color(255, 0, 0)
		vert = tlp.Color(0, 255, 0)
		
		for n in self.albums:
			self.viewColor[n] = rouge
			
		for n in self.mots:
			self.viewColor[n] = vert
			
	def layout(self, graff):
		
		viewLocalLayout = graff.getLocalLayoutProperty("viewLayout")
		dataSet = tlp.getDefaultPluginParameters("Bubble Tree", graph)	
		dataSet["result"] = viewLocalLayout	
		tlp.applyAlgorithm(graff, dataSet, "Bubble Tree")
		
			
	def calcul_degree(self):
		"""
		Calcul du degree.
		"""
		
		dataSet = tlp.getDefaultPluginParameters("Degree", graph)
		dataSet["result"] = self.degree		
		tlp.applyAlgorithm(self.graph, dataSet, "Degree")
			
	
	def reduction_degre_mot(self):
		"""
		Colore les noeud en fonction de leur degre.
		et floue les albums.
		"""
		
		inter = []			
					
		for n in self.graph.getNodes():
			if self.degree[n] > self.seuil_degree:				
				if not self.est_album[n]:
					inter.append(n)
					
		intere = []
		for n in inter:
			if self.good[n] < self.ratio or self.good[n] > (1 - self.ratio):
				intere.append(n)				
			
		for n in intere:	
			self.subGraph_simple.addNode(n)
			
	def reduction_degre_mot_album(self):
		"""
		Colore les noeud en fonction de leur degre.
		On ajoute les albums en relations avec ces mots.
		"""				
				
		inter = []					
		for n in self.graph.getNodes():
			if self.degree[n] > self.seuil_degree:
				if not self.est_album[n]:
					inter.append(n)
					
		intere = []
		for n in inter:
			if self.good[n] < self.ratio or self.good[n] > (1 - self.ratio):
				intere.append(n)
				
				
		inter = []
		for n in intere:
			inter.append(n)
			for alb in self.graph.getInNodes(n):
				inter.append(alb)	
		
		
		self.subGraph_albums = graph.inducedSubGraph(inter)
		
		
	def bet_cen(self):
		"""
		appel de l'algo "Betweenness Centrality" de tulip
		"""
		
		dataSet = tlp.getDefaultPluginParameters("Betweenness Centrality", graph)		
		tlp.applyAlgorithm(self.graph, dataSet, "Betweenness Centrality")
		
		
	def estomper_albums(self):
		"""
		rend les album moins visible.
		"""
		
		blanc = tlp.Color(255, 255, 255)
		blanc.setA(0)
		for n in self.albums:
			#a = self.viewColor[n]
			#a.setA(0)
			self.viewColor[n] = blanc
			
	def noircir_albums(self):
		"""
		rend les album moins visible.
		"""
		
		noir = tlp.Color(0, 0, 0)
		blanc.setA(255)
		for n in self.albums:
			self.viewColor[n] = noir
		

def main(graph) : 
	g = GraphMots(graph)

	g.donnees_mots = "/home/guillaume/Tulip-3.7.0/Workspace/Projet/mots.csv"
	
	g.extraction_donnees_fichier()
	print "Extraction finie"
	g.donnees_en_graphe(g.tout)
	print "Creation du graphe"
	g.calcul_moyenne_good()			
		
	g.calcul_degree()	
	g.ratio = 0.2
	g.seuil_degree = 100
	g.reduction_degre_mot()
	g.reduction_degre_mot_album()
	print "Sous-graphe cree"
	
	g.layout(g.subGraph_simple)	
	g.layout(g.subGraph_albums)
	g.mise_en_forme_noeuds()
	print "Agencement fini"
	
	
