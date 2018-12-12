"""
A flux representation which Green eyes mobile application should be
"""
import logging
import sys
import argparse
import getpass
import requests
import base64
import json
import time
import os
import cv2
import ast
import uuid


def auth(username, password, api):
    """
    Authenticate user

    Args:
        username: User name
        password: User password
        api: API URL

    Returns:
        The authentication token
    """
    creds = base64.b64encode(bytes(
                username+":"+password,
                'utf-8')).decode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Basic %s' % creds
    }
    resp = requests.post(
        api + '/token/',
        headers=headers)
    resp = resp.json()
    return resp['response']


def insert_image(filepath, api, token):
    """
    Image filepath

    Args:
        filepath: Image filepath
        api: API URL
        token: Token

    Returns:
        A inserted image
    """
    with open(filepath, 'rb') as fh:
        img_b64 = base64.b64encode(fh.read()).decode('utf-8')
    image = {
              "id": 0,
              "description": '',
              "idDisease": 50,
              "size": 1,
              "source": '',
              "url": img_b64
          }
    headers = {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Authorization': 'Bearer %s' % token['token']
              }
    resp = requests.post(
        api + '/images/',
        data=json.dumps(image),
        headers=headers).json()
    return resp['response']


def create_analysis(image_id, api_url, token, id_classifier=1):
    """
    Create analysis

    Args:
        image: Image to be anlyzed
        api_url: API URL
        token: User token
        id_classifier: Classifier identifier

    Returns:
        A analysis
    """
    data = {
                "id": 0,
                "idImage": image_id,
                "idClassifier": id_classifier,
                "idUser": token['id_user']
            }
    headers = {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Authorization': 'Bearer %s' % token['token']
              }
    resp = requests.post(
        api_url + '/analysis/',
        data=json.dumps(data),
        headers=headers).json()
    return resp['response']


def search_analysis_results(id_analysis, api_url, token):
    """
    Search by analysis

    Args:
        id_analysis: Analysis identifier
        token: Token
        api_url: API URL

    Returns:
        A list of analysis results
    """
    data = {
                "action": "searchByID",
                "id": id_analysis,
            }
    headers = {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Authorization': 'Bearer %s' % token['token']
              }
    resp = requests.get(
        api_url + '/analysis/',
        params=data,
        headers=headers).json()
    return resp['response']['analysis_results']


def calculateProbs(analysis_results):
    total = 0
    counter = {}
    for i in range(len(analysis_results)):
        stringified_id = analysis_results[i]['disease']['id']
        if(analysis_results[i]['disease']['id'] != '62'):
            if (analysis_results[i]['disease']['id'] not in counter):
                counter[stringified_id] = []
        counter[stringified_id].append(analysis_results[i])
        total += 1
    probs = {}
    for key in counter:
        probs[key] = (len(counter[key]) / total) * 100
    return probs


def detailDiseases(analysis_results, probs):
    details = {}
    keys = list(probs.keys())
    for i in range(len(keys)):
        for j in range(len(analysis_results)):
            if(analysis_results[j]['disease']['id'] == keys[i]):
                details[analysis_results[j]['disease']['id']] = {
                    'id': analysis_results[j]['disease']['id'],
                    'scientificName': analysis_results[j]['disease']['scientificName'],
                    'percentage': probs[analysis_results[j]['disease']['id']]}
                break
    return details


def sort_results(results_details):
    temp = results_details
    keys = results_details.keys()
    sorted_object = {}
    for i in range(len(keys)):
        index = 0
        aux = {'id': 0, 'scientificName': '', 'percentage': 0}
        for key in temp:
            if(temp[key]['percentage'] > aux['percentage']):
                index = key
                aux = temp[key]
        sorted_object[i] = temp[index]
        del temp[index]
    return sorted_object


if __name__ == '__main__':
    logging.basicConfig(
        filename='',
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.INFO)
    parser = argparse.ArgumentParser(
        prog='green_eyes.py',
        usage='python3 green_eyes.py <args>',
        description="""A flux representation which Green eyes mobile \
            application should be """,
        version='1.0')
    parser.add_argument('image', type=str, help='Image to be analyzed')
    parser.add_argument('api_url', type=str, help='API URL')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    username = input("Username: ")
    password = getpass.getpass('Password: ')
    logging.info('Authenticating...')
    try:
        token = auth(username, password, args.api_url)
    except Exception as ex:
        logging.error('Error on authentication: %s' % str(ex))
        sys.exit(0)
    logging.info('Uploading image...')
    img = insert_image(args.image, args.api_url, token)
    logging.info('Creating analysis...')
    analysis = create_analysis(
        img['id'], args.api_url, token, id_classifier=1)
    results = []
    while not results:
        time.sleep(5)
        logging.info('Searching for results...')
        results = search_analysis_results(analysis['id'], args.api_url, token)
    logging.info('Building image with results...')
    img = cv2.imread(args.image)
    colors = {53: (255, 0, 0), 56: (0, 0, 255), 52: (203, 66, 244)}
    for anal_res in results:
        if anal_res['disease']['id'] in colors:
            frame = ast.literal_eval(anal_res['frame'])
            cv2.rectangle(
                img,
                (frame[0], frame[2]),
                (frame[1], frame[3]),
                colors[anal_res['disease']['id']],
                2)
    filepath = os.path.join('/tmp', str(uuid.uuid4()) + '.jpg')
    logging.info('Writing image result: %s' % filepath)
    cv2.imwrite(filepath, img)
    a = sort_results(
        detailDiseases(
            results,
            calculateProbs(results)))
    logging.info('Probs: %s' % str(a))
