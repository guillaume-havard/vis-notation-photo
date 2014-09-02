from tulip import *

class Notation :
	
	def __init__ (self, graph):
		self.graph = graph		
		
		self.height =  graph.getDoubleProperty("height")
		self.id_ =  graph.getDoubleProperty("id")
		self.latitude =  graph.getDoubleProperty("latitude")
		self.longitude =  graph.getDoubleProperty("longitude")
		self.size =  graph.getDoubleProperty("size")	
		self.width =  graph.getDoubleProperty("width")
		
		self.note =  graph.getDoubleProperty("note")
		
		self.name =  graph.getStringProperty("name")
		self.caption =  graph.getStringProperty("caption")
		self.description =  graph.getStringProperty("description")
		self.mots = [] # liste des mots de chaque albums.
		
		self.not_loc = {}
		self.not_taille = {}
		self.not_mots = {}
		self.not_size  = {}
		
		self.fichier_loc = "notation-localisation.csv"	
		self.fichier_tailles = ""
		self.fichier_mots = "notation-mots.csv"
		self.fichier_size = ""
		self.sortie = "sortie.csv"
		
	def notation(self):
		"""
		Note les albums du graph Tulip et renvoie la sortie dans le fichier 'sortie'.
		"""		
		self.__recuperation_notation__(); 
		print "Recuperation des donnees des fichiers."
		
		self.__initialisation_notes__(); 
		print "Initialisation des notes."
		
		self.__notation_size__(); 
		print "Initialisation des notes en fonction de size."	
		
		self.__notation_localisation__(20, 0.3); 
		print "Notation en fonction de la localisation."
		self.__notation_mots__(100, 0.1); 
		print "Notation en fonction des mots de l'album."
		self.__notation_tailles__(); 
		print "Notation en fonction de de la taillede sphotos de l'albums."
		
		print "Fin de l'algorithme"
			
	def __recuperation_notation__(self):
		"""
		Recuperes les information des fichier de notation pour le ajouter Ã  notre objet dans le but de noter les photos
		"""
		
		self.__recuperation_notation_location__()
		self.__recuperation_notation_mots__()
		
	def __recuperation_notation_location__(self):
		
		f_in = open(self.fichier_loc, 'r')
		if not f_in : 
		    raise Exception("Notation.__recuperation_notation_location__ : echec de l'ouverture du fichier")
		
		f_in.readline() # on enleve la ligne d'entete.		
		ligne = f_in.readline()
		
		while len(ligne):
			ligne = ligne.replace("\n", "")	
			texte = ligne.split("\t") #0:latitude;	1:longitude;	2:nb_album;	3:moyenne good
			
			self.not_loc[int(texte[0]), int(texte[1])] = (int(texte[2]), float(texte[3]))
			
			#print texte[3], " ", float(texte[3])
			
			ligne = f_in.readline()
		
		f_in.close()	
		
		
	
	def __recuperation_notation_taille__(self):
		pass
		
	def __recuperation_notation_mots__(self):
		
		f_in = open(self.fichier_mots, 'r')
		if not f_in : 
		    raise Exception("Notation.__recuperation_notation_mots__ : echec de l'ouverture du fichier")
		
		f_in.readline() # on enleve la ligne d'entete.		
		ligne = f_in.readline()
		
		while len(ligne):				
			ligne = ligne.replace("\n", "")	
			texte = ligne.split("\t") #0:identifiant;	1:degree;	2:moyenne good			
						
			self.not_mots[texte[0]] = (int(texte[1]), float(texte[2]))			
			
			ligne = f_in.readline()
		
		f_in.close()

		
	def __traitement_mots_noeud__(self, noeud):
		"""
		Retourne une liste de tous les identifiants d'un album.
		"""
		tmp = self.name[noeud].split(" ")
		
		tmp2 = [m for m in self.description[noeud].split(" ") if not tmp.count(m)]
		for m in tmp2:
			tmp.append(m)
			
		tmp2 = [m for m in self.caption[noeud].split(" ") if not tmp.count(m)]
		for m in tmp2:
			tmp.append(m)
			
		return tmp
		
	
			
	def __initialisation_notes__(self):
		"""
		Initialise les notes pour la notation.
		"""
				
		for n in self.graph.getNodes():
			self.note[n] = 0.5;
			
		
	def __notation_tailles__(self):
		"""
		Note en fonction de la taille des photos.
		"""
		
		for n in self.graph.getNodes():
			if not self.height[n] or not self.width[n] :
				self.note[n] = 0
		
	def __notation_localisation__(self, qqt=0, good=1.0):
		"""
		Note en fonction de la localisation des photos.
		"""
		
		for n in self.graph.getNodes():
			pos = (int(self.latitude[n]), int(self.longitude[n]))
			if self.not_loc.has_key(pos) and self.not_loc[pos][0] >= qqt and ((self.not_loc[pos][1] >= (1 - good)) or self.not_loc[pos][1] <= good):
				self.note[n] += self.not_loc[pos][1] - 0.5
		
	def __notation_mots__(self, qqt=0, good=1.0):
		"""
		Note en fonction des mots des photos.
		"""
		for n in self.graph.getNodes():
			for m in self.__traitement_mots_noeud__(n):
				if self.not_mots.has_key(m) and self.not_mots[m][0] >= qqt and (self.not_mots[m][1] >= (1 - good) or self.not_mots[m][1] <= good):
					print self.not_mots[m][1]
					self.note[n] += self.not_mots[m][1] - 0.5					
					
	def __notation_size__(self):
		"""
		Note en fonction de la taille des albums.
		"""
		cpt = 0
		cptP = 0

		for n in self.graph.getNodes():			
			if self.size[n] < 200 :
				self.note[n] = 0.140 * (self.size[n]**0.180)
				cpt += self.note[n]
				cptP += 1
			else :
				self.note[n] = 0.5
				
		decalage = cpt/cptP
		
		for n in self.graph.getNodes():
			if self.note[n] < 0.5:
				self.note[n] += decalage
		
		
	def analyse(self):
		"""
		Analyse les resultats pour tester les algorithmes.
		"""
		cptN = 0					
		
		for n in self.graph.getNodes():
			self.note[n] += 0.1
			
			if self.note[n] < 0:
				self.note[n] = 0
			elif self.note[n] > 1:
				self.note[n] = 1
				
			if self.note[n] < 0.5:				
				cptN += 1			
							
		print "Il y a ", 12000 - cptN, " marquee bonnes."
		
	def ecriture_sortie(self):
		"""
		Ecrit les notes dans le fichier de sortie.
		"""
		
		f_out = open(self.sortie, 'w')
		if not f_out : 
		    raise Exception("Notation.ecriture_sortie : echec de l'ouvertur du fichier " + self.sortie)
	
		for n in self.graph.getNodes():			
			f_out.write(str(int(self.id_[n])) + "," + str(self.note[n]) + "\n")			
			
		f_out.close()


def main(graph) :
	
	g = Notation(graph)
	
	g.notation()
	
	g.analyse()
	
	g.ecriture_sortie()
