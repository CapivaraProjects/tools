"""
This script read XML files and crop images
"""
import os
import sys
import uuid
import logging
import argparse
import cv2
import xmltodict


def read_xml(xml):
    """Read XML file and return a dict

    Args:
        xml: XML filepath

    Returns:
        The XML parsed to dict
    """
    filehandler = open(xml, 'r')
    content = filehandler.read()
    filehandler.close()
    return xmltodict.parse(content)


def crop_images_from_xml(xml, output):
    """Crop images from XML

    Arguments:
        xml: XML to be readed
        output: Output filepath

    Returns:
        None
    """
    logging.info('reading xml')
    xml_content = read_xml(xml)
    print(xml_content)
    logging.info('reading img')
    img = cv2.imread(xml_content['annotation']['path'])
    objs = {}
    logging.info('croping...')
    logging.info('annotations: %s' % str(type(xml_content['annotation']['object'])))
    if 'list' in str(type(xml_content['annotation']['object'])):
        for obj in xml_content['annotation']['object']:
            os.makedirs(
                os.path.join(
                    output,
                    obj['name']),
                exist_ok=True)
            bndbox = obj['bndbox']
            crop = img[
                int(bndbox['ymin']):int(bndbox['ymax']),
                int(bndbox['xmin']):int(bndbox['xmax'])]
            cv2.imwrite(
                os.path.join(
                    output,
                    obj['name'],
                    str(uuid.uuid4()) + '.jpg'),
                crop)
            if obj['name'] not in objs:
                objs[obj['name']] = []
            objs[obj['name']].append([bndbox['xmin'],
                                      bndbox['xmax'],
                                      bndbox['ymin'],
                                      bndbox['ymax']])
    else:
        obj = xml_content['annotation']['object']
        os.makedirs(
            os.path.join(
                output,
                obj['name']),
            exist_ok=True)
        bndbox = obj['bndbox']
        crop = img[
            int(bndbox['ymin']):int(bndbox['ymax']),
            int(bndbox['xmin']):int(bndbox['xmax'])]
        cv2.imwrite(
            os.path.join(
                output,
                obj['name'],
                str(uuid.uuid4()) + '.jpg'),
            crop)
        if obj['name'] not in objs:
            objs[obj['name']] = []
        objs[obj['name']].append([bndbox['xmin'],
                                  bndbox['xmax'],
                                  bndbox['ymin'],
                                  bndbox['ymax']])
    return objs


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        prog='crop_images_from_xml.py',
        usage='python3 crop_images_from_xml.py <xml> <output>',
        description='Read XML files and crop images',
        epilog='This script should create dirs on output for respective label')
    PARSER.add_argument('xml', type=str, help='XML file to be readed')
    PARSER.add_argument('output', type=str, help='Output dir put results')
    if len(sys.argv) == 1:
        PARSER.print_help(sys.stderr)
        sys.exit(1)
    ARGS = PARSER.parse_args()
    logging.basicConfig(
        filename='',
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.INFO)
    crop_images_from_xml(ARGS.xml, ARGS.output)
    logging.info('Finished!')
