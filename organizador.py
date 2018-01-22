
import os
import argparse

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
        if (plant.commonName == name):
            return plants.index(plant)

    return -1


def test_searchPlantByScientificName():
    """
        Test function created for analyze searchPlantByScientificName
    """
    plants = [Plant(commonName="orange"), 
            Plant(commonName="banana"), 
            Plant(commonName="grape") ]
    assert searchPlantByScientificName(plants, "grape") == 2

def searchDiseaseByScientificName(plant, name):
    """ (Plant, str) -> int
        Method used to realize search plant by diseases with the scientific name
    """
    for disease in plant.diseases:
        if (disease.scientificName == name):
            return plant.diseases.index(disease)

    return -1

def organize(database, workdir, output, size):
    """ (str, str, str, str) -> Bool

        Method used to execute organization of images
    """
    filehandler = open(output, "a")
    logging.info("CONNECTING DATABASE {}".format(database))
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    plants = []
    
    scriptPlants = ""
    scriptDiseases = ""
    scriptImages = ""                                                                                                                                                   

    for row in cursor.execute(
            "SELECT id, crop_common_name, crop_scientific_name, disease_common_name, disease_scientific_name, url, description, metadata FROM ANNOTATIONS;"):
        oldAnnotation = OldAnnotation(row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7])

        if (oldAnnotation.url == "" or  oldAnnotation.cropScientificName == ""):
            continue

        indexPlant = searchPlantByScientificName(plants, oldAnnotation.cropCommonName)
        plant = Plant()
        if (indexPlant == -1):
            plant = Plant(scientificName=oldAnnotation.cropScientificName,

                    commonName=oldAnnotation.cropCommonName, diseases=[])
            logging.info("CREATING {}".format(plant.commonName).replace(" ", "_").replace(";", "").replace("(", "_").replace(")", "_").replace("<i>", "").replace("</i>", ""))
            os.system("mkdir -p " + workdir + "/" + plant.commonName.replace(" ", "_").replace(";", "").replace("(", "_").replace(")", "_").replace("<i>", "").replace("</i>", ""))
            #filehandler.write("INSERT INTO PLANTS(scientific_name, common_name) VALUES ('{}', '{}')\n".format(plant.scientificName, plant.commonName))
            scriptPlants += "INSERT INTO PLANTS(scientific_name, common_name) VALUES ('{}', '{}');\n".format(plant.scientificName, plant.commonName);
        else:
            logging.info("index: {} - plant: {}".format(str(indexPlant), plants[indexPlant].scientificName))
            plant = plants[indexPlant]
        
        disease = Disease(plant=plant, commonName=oldAnnotation.diseaseCommonName, scientificName=oldAnnotation.diseaseScientificName)

        if (oldAnnotation.diseaseCommonName == "" or oldAnnotation.diseaseScientificName == "" or "Healthy" in oldAnnotation.description or "healthy" in oldAnnotation.description):
            disease.scientificName = "healthy"
            disease.commonName = "healthy"

        indexDisease = searchDiseaseByScientificName(disease.plant, disease.scientificName)
        logging.info("DISEASE: {} - {} - {}".format(disease.scientificName, plant.scientificName, indexDisease))
        if (indexDisease == -1):
            logging.info("CREATING {}/{}".format(plant.commonName.replace(" ", "_").replace(";", "").replace("(", "_").replace(")", "_").replace("<i>", "").replace("</i>", ""), disease.scientificName.replace(" ", "_").replace(";", "").replace("(", "_").replace(")", "_").replace("<i>", "").replace("</i>", "")))
            os.system("mkdir -p "+workdir + "/" + plant.commonName.replace(" ", "_").replace(";", "").replace("(", "_").replace(")", "_").replace("<i>", "").replace("</i>", "") + "/" + disease.scientificName.replace(" ", "_").replace(";", "").replace("(", "_").replace(")", "_").replace("<i>", "").replace("</i>", ""))
            scriptDiseases += "INSERT INTO DISEASES(id_plant, scientific_name, common_name) VALUES ((SELECT id FROM PLANTS WHERE scientific_name = '{}' LIMIT 1),'{}', '{}');\n".format(plant.scientificName, disease.scientificName, disease.commonName)
            #filehandler.write("INSERT INTO DISEASES(id, scientific_name, common_name) VALUES ((SELECT id FROM PLANTS WHERE scientific_name = '{}' LIMIT 1),'{}', '{}')\n".format(disease.plant.scientificName, disease.scientificName, disease.commonName))
        else:
            disease = plant.diseases[indexDisease]
                  
        image = Image(disease=disease,
                    url=oldAnnotation.url.replace("<i>", "").replace("</i>", ""),
                    description=oldAnnotation.description,
                    source=oldAnnotation.metadata)          

        regex = re.compile("[\w]+/[\w,;\-]*\/([\w\.;\-,]+)+")
        logging.info(image.url)
        if (not regex.match(image.url) == None):
            logging.info(image.url)
            image.url = regex.match(image.url).group(1)
            if ("large" in image.url):
                continue
        else:
            logging.info(image.url)
            continue

        if ("large" in disease.scientificName):
            continue
        logging.info("CREATING {}/{}/{} ".format(plant.commonName.replace(" ", "_"), disease.scientificName.replace(" ", "_"), image.url.replace(" ", "_")))
        os.makedirs(workdir + "/" + plant.commonName.replace(" ", "_").replace(";", "").replace("(", "_").replace(")", "_").replace("<i>", "").replace("</i>", "") + "/" + disease.scientificName.replace(" ", "_").replace(";", "").replace("(", "_").replace(")", "_").replace("<i>", "").replace("</i>", "") + "/", exist_ok=True)
        dir1 = workdir + "/" + plant.commonName.replace(" ", "_").replace("(", "_").replace(")", "_").replace("<i>", "").replace("</i>", "") + "/" + image.url
        dir2 = workdir + "/" + plant.commonName.replace(" ", "_").replace(";", "").replace("(", "_").replace(")", "_").replace("<i>", "").replace("</i>", "") + "/" + disease.scientificName.replace(" ", "_").replace(";", "").replace("(", "_").replace(")", "_").replace("<i>", "").replace("</i>", "") + "/" + image.url
        logging.info(dir1)
        logging.info(dir2)

        if("large" in dir2):
            continue

        try:
            shutil.copyfile(dir1,dir2)     
        except FileNotFoundError:
            continue

        #filehandler.write("INSERT INTO IMAGES(id_disease, url, description, source) VALUES ((SELECT id FROM DISEASES WHERE scientific_name = '{}' AND id_plant = (SELECT id FROM PLANTS WHERE scientific_name = '{}' LIMIT 1) LIMIT 1), '{}', '{}', '{}')\n".format(image.disease.scientificName, image.disease.plant.scientificName, image.url, image.description, image.source))
        scriptImages += "INSERT INTO IMAGES(id_disease, url, description, source, size) VALUES ((SELECT id FROM DISEASES WHERE scientific_name = '{}' AND id_plant = (SELECT id FROM PLANTS WHERE scientific_name = '{}' LIMIT 1) LIMIT 1), '{}', '{}', '{}', (SELECT id FROM TYPES WHERE value='{}' AND description='image-size' LIMIT 1));\n".format(disease.scientificName, plant.scientificName, image.url, image.description, image.source, size)


        disease.images.append(image)

        if (indexDisease == -1):
            plant.diseases.append(disease)
        else:
            plant.diseases[indexDisease] = disease

        if (indexPlant == -1): 
            plants.append(plant)
        else:
            plants[indexPlant] = plant

    filehandler.write(scriptPlants)
    filehandler.write(scriptDiseases)
    filehandler.write(scriptImages)

    filehandler.close()
    return True

if __name__=="__main__":
    parser = argparse.ArgumentParser(
            description="""This component should be used to organize directories from a sqlite database with plantvillage images information""", 
            epilog="""""")
    parser.add_argument("database", type=str, help="database.db file to connect")
    parser.add_argument("workdir", type=str, help="filepath to workdir")
    parser.add_argument("output", type=str, help="SQL output filepath")
    parser.add_argument("size", type=str, help="Image size", choices=["thumb", "medium", "large"])
    args = parser.parse_args()

    workdir = args.workdir
    if (workdir[len(workdir)-1] == "/"):
        workdir = workdir[:-1]

    if(organize(args.database, workdir, args.output, args.size)):
        print("Finished!")

