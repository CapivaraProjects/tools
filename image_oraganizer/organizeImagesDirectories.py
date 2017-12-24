import os, argparse
import re
import sqlite3

import logging
logging.basicConfig(filename='image_path_organizer.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def moveImagesToHealthyDir(healthy):
	
	for sourceDestination in healthy:
		
		# First I need take the source path without plant name
		# for this I need all '/' positions in source URL as delimiters
		listDelimiters = [m.start() for m in re.finditer('/', sourceDestination)]

		# get the last position of a slash with [-1]  
		# /usr/local/images/plantvillage/medium/[plantName](HERE!)
		domain = sourceDestination[0:listDelimiters[-1]]
		
		# save the image name for later
		imgName = sourceDestination[listDelimiters[-1]+1:len(sourceDestination)]
		
		# concatenate /healthy to domain
		healthyDomain = "{}/healthly".format(domain)
		
		# create the directory healthly if not exist
		if not os.path.exists(healthyDomain):
			os.makedirs(healthyDomain)
			
		# concatenate the image name back
		targetDestination = "{}/{}".format(healthyDomain,imgName)
		
		# rename the path of image to the new directory
		os.rename(sourceDestination, targetDestination)

	
def moveImagesToDiseasesDir(diseases):
	
	for disease in diseases:
		
		# complete URL now
		sourceDestination = disease[0]
		
		# First I need take the source path without plant name
		# for this I need all '/' positions in source URL as delimiters
		listDelimiters = [m.start() for m in re.finditer('/', sourceDestination)]

		# get the last position of a slash with [-1]  
		# /usr/local/images/plantvillage/medium/[plantName](HERE!)
		domain = sourceDestination[0:listDelimiters[-1]]
		
		# save the image name for later
		imgName = sourceDestination[listDelimiters[-1]+1:len(sourceDestination)]
		
		# concatenate /[disease] to domain
		diseaseDomain = "{}/{}".format(domain,disease[1])
		
		# create the disease directory if not exist
		if not os.path.exists(diseaseDomain):
			os.makedirs(diseaseDomain)
			
		# concatenate the image name back
		targetDestination = "{}/{}".format(diseaseDomain,imgName)
		
		# rename the path of image to the new directory
		os.rename(sourceDestination, targetDestination)
	
	
def start_execute(database, table):

	logging.info("OPEN CONNECTION IN: {}".format(database))
	conn = sqlite3.connect(database)
	cursor = conn.cursor()
	logging.info("CONNECTION ESTABLISHED!")
	
	healthy = []
	diseases = []
		
	# select just images without disease
	# /usr/local/images/plantvillage/medium/Apple/*.[jpg|png]
	healthyQuery = "SELECT URL FROM {} WHERE DISEASE_COMMON_NAME=''".format(table)
	logging.info(healthyQuery)
	
	for row in cursor.execute(healthyQuery):
		healthy.append(row[0]) # the return into row is a set of tuples but it's look like [(),] than I get just tuple in 0	
	
	logging.info("{} LINES RETURNED".format(len(healthy)))
	
	# move healthy images for a named 'healthy' directory
	logging.info("MOVING HEALTHY IMAGES")
	moveImagesToHealthyDir(healthy)
		
	# select just images with disease
	# each line have URL of image and the disease name, the object 'diseases' got this format
	# 	[('url/of/image1', 'd1'),('url/of/image2', 'd2'), ...]
	diseaseQuery = "SELECT URL, DISEASE_COMMON_NAME FROM {} WHERE DISEASE_COMMON_NAME<>'' ORDER BY DISEASE_COMMON_NAME ASC".format(table)
	logging.info(diseaseQuery)
	
	for row in cursor.execute(diseaseQuery):
		diseases.append(row)
	
	logging.info("{} LINES RETURNED".format(len(diseases)))
		
	# move image with disease for thir respective disease directory
	logging.info("MOVING DISEASES IMAGES")
	moveImagesToDiseasesDir(diseases)

	
if __name__=="__main__":
	# Help para o script
	parser = argparse.ArgumentParser(description="""This component should be used to organize directories from a sqlite database with plantvillage images information""", epilog="""""")
	parser.add_argument("--database", help="database.db file to connect")
	parser.add_argument("--table", help="table with images content")

	args = parser.parse_args()

	if None in args:
		parser.print_help()
		sys.exit(1)
	else:
		start_execute(args.database, args.table)
