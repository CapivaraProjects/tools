import os
import sqlite3


"""
def createNewDirectories(rootImgDir, diseases):
	
	# All directory name in rootImgDir is a plant name then:
	plantName = os.listdir(rootImgDir)
	for
	path = "%s/%s/%s".format(rootImgDir,)
	os.mkdir()
"""

def moveImagesToHealthyDir(healthy)
	
	for sourceDestination in healthy:
		# tem que pegar o caminho sem o nome da imagem
		# domain = sourceDestination...
		# imgName = sourceDestination...
		# concatenar /healthy ao domain
		# healthyDomain = "%s/healthly".format(domain)
		# concatenar o nome da imagem devolta
		# targetDestination = "%s/%s'.format(healthyDomain,imgName) 	
		os.rename(sourceDestination, targetDestination)
		
	
def start_execute(database, table, rootImgDir):

	# obtem conexão
	conn = sqlite3.connect(database)
	cursor = conn.cursor()
	
	healthy = []
	unhealthy = []
	diseases = []
		
	# obtem apenas imagens sem doenca
	for row in cursor.execute("SELECT URL FROM ANNOTATIONS WHERE DISEASE_COMMON_NAME=''"):
		healthy.append(row)
	
	# move as imagens saudaveis para o diretorio healthy
	moveImagesToHealthyDir(healthy)
		
	# obtem imagens com doenca
	for row in cursor.execute("SELECT URL FROM ANNOTATIONS WHERE DISEASE_COMMON_NAME<>'' ORDER BY DISEASE_COMMON_NAME ASC"):
		unhealthy.append(row)
	
	# mapear doencas para cada planta com um dicionario no formato
	# dict['pant1'] = ['d1','d2','d3']
	# dict['pant2'] = ['d1','d2']
	# dict['pant3'] = ['d1','d4']
	
	# criar os diretorios para cada doenca dentro do diretorio de cada planta
	"""
	diseaseDict = dict()
	
	for i in len(unhealthy):
		
		# get just scientific_disease column
		disease = unhealthy[i][4]
		
		# get just crop_common_name column
		platName = unhealthy[i][1]
		
		if not disease in 
		
		path = "%s/%s/%s".format(rootImgDir, plantName, disease)
		if not disease in diseases:
			os.mkdir()
			diseases.append(disease)

	"""

if __name__=="__main__":
	# Help
	parser = argparse.ArgumentParser(description="""This component should be used to organize directories from a sqlite database with plantvillage images information""", epilog="""""")
	parser.add_argument("--database", help="database to connect")
	parser.add_argument("--table", help="table with images content")
	parser.add_argument("--rootImgDir", help="root path to images plant directories")

	args = parser.parse_args()
	
	if None in args:
		parser.print_help()
		sys.exit(1)
	else:
		if  args.rootImgDir[-1] == "/":
			rootImgDir = args.rootImgDir[:-1]
		else
			rootImgDir = args.rootImgDir
		
		start_execute(args.database, args.table, rootImgDir)
