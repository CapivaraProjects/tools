import os, argparse
import re
import sqlite3
import shutil
import logging
from capivaraprojects.greeneyes.models.OldAnnotation import OldAnnotation
from capivaraprojects.greeneyes.models.Plant import Plant
from capivaraprojects.greeneyes.models.Disease import Disease
from capivaraprojects.greeneyes.models.Image import Image

logging.basicConfig(filename='image_path_organizer.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def searchPlantByScientificName(plants, name):
    """ (list, str) -> int
        Method used to realize search in plants list for a name
    """
    for plant in plants:
        if (plant.scientificName == name):
            return plants.index(plant)

    return -1

def searchDiseaseByScientificName(plant, name):
    """ (Plant, str) -> int
        Method used to realize search plant by diseases with the scientific name
    """
    for disease in plant.diseases:
        if (disease.scientificName == name):
            return plant.diseases.index(disease)

    return -1

def organize(database, workdir, output):
    """ (str, str, str) -> Bool
        Method used to execute organization of images
    """
    filehandler = open(output, "a")
    logging.info("CONNECTING DATABASE {}".format(database))
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    plants = []

    for row in cursor.execute(
            "SELECT id, crop_common_name, crop_scientific_name, disease_common_name, disease_scientific_name, url, description, metadata FROM ANNOTATIONS WHERE crop_common_name='Cabbage__red,_white,_Savoy_' or crop_common_name='Gourd';"):
        oldAnnotation = OldAnnotation(row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7])

        plant = Plant(scientificName=oldAnnotation.cropScientificName,
                    commonName=oldAnnotation.cropCommonName)
        indexPlant = searchPlantByScientificName(plants, plant.scientificName)
        if (indexPlant == -1):
            logging.info("CREATING {}".format(plant.scientificName).replace(" ", "_"))
            os.system("mkdir -p " + workdir + "/" + plant.scientificName.replace(" ", "_"))
            filehandler.write("INSERT INTO PLANTS(scientific_name, common_name) VALUES ('{}', '{}')\n".format(plant.scientificName, plant.commonName))
        else:
            plant = plants[indexPlant]
        
        disease = Disease(plant=plant)
        if (oldAnnotation.diseaseCommonName == "" or oldAnnotation.diseaseScientificName == ""):
            disease.scientificName = "healthy"
            disease.commonName = "healthy"

        if (disease.scientificName == ""):
            disease.scientificName = "healthy"
            disease.commonName = "healthy"

        indexDisease = searchDiseaseByScientificName(disease.plant, disease.scientificName)
        logging.info("DISEASE: {}".format(disease.scientificName))
        if (indexDisease == -1):
            logging.info("CREATING {}/{}".format(plant.scientificName.replace(" ", "_"), disease.scientificName.replace(" ", "_")))
            os.system("mkdir -p "+workdir + "/" + plant.scientificName.replace(" ", "_") + "/" + disease.scientificName.replace(" ", "_"))
            filehandler.write("INSERT INTO DISEASES(id, scientific_name, common_name) VALUES ((SELECT id FROM PLANTS WHERE scientific_name = '{}' LIMIT 1),'{}', '{}')\n".format(disease.plant.scientificName, disease.scientificName, disease.commonName))
        else:
            disease = plant.diseases[indexDisease]
                  
        image = Image(disease=disease,
                    url=oldAnnotation.url,
                    description=oldAnnotation.description,
                    source=oldAnnotation.metadata)          

        regex = re.compile("[\w]+/[\w,]*\/([\w\.;]+)+")
        image.url = regex.match(image.url).group(1)

        logging.info("CREATING {}/{}/{} ".format(plant.scientificName.replace(" ", "_"), disease.scientificName.replace(" ", "_"), image.url.replace(" ", "_")))
        shutil.copyfile(workdir + "/" + plant.commonName.replace(" ", "_") + "/" + image.url, workdir + "/" + plant.scientificName.replace(" ", "_") + "/" + disease.scientificName.replace(" ", "_") + "/" + image.url)
        filehandler.write("INSERT INTO IMAGES(id_disease, url, description, source) VALUES ((SELECT id FROM DISEASES WHERE scientific_name = '{}' LIMIT 1), '{}', '{}', '{}')\n".format(image.disease.scientificName, image.url, image.description, image.source))

        disease.images.push(image)

        if (indexDisease == -1):
            plant.diseases.push(disease)
        else:
            plant.diseases[indexDisease] = disease

        if (indexPlant == -1): 
            plants.push(plant)
        else:
            plants[indexPlant] = plant

    fh.close()
    return True

if __name__=="__main__":
    parser = argparse.ArgumentParser(
            description="""This component should be used to organize directories from a sqlite database with plantvillage images information""", 
            epilog="""""")
    parser.add_argument("database", type=str, help="database.db file to connect")
    parser.add_argument("workdir", type=str, help="filepath to workdir")
    parser.add_argument("output", type=str, help="SQL output filepath")
    args = parser.parse_args()

    workdir = args.workdir
    if (workdir[len(workdir)-1] == "/"):
        workdir = workdir[:-1]

    if(organize(args.database, workdir, args.output)):
        print("Finished!")

