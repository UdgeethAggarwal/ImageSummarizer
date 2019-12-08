import os,sys
import json
import requests


API_KEY = 'e5ca8ab74d9840ec9c728a304b28bdc4'
ENDPOINT = 'https://eastus.api.cognitive.microsoft.com/vision/v2.0/ocr'
DIR = '.'

def handler(pathToImage):
    text = ''
    results = get_text(pathToImage)
    text += parse_text(results)
    print(text)
    open('output.txt', 'w').write(text)
   
    return text

def parse_text(results):
    #print(results)
    text = ''
    print(results)
    for region in results['regions']:
        for line in region['lines']:
            for word in line['words']:
                text += word['text'] + ' '
            text += '\n'
    return text  

def get_text(pathToImage):
    print('Processing: ' + pathToImage)
    headers  = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params   = {
        'language': 'en',
        'detectOrientation ': 'true'
    }
    payload = open(pathToImage, 'rb').read()
    response = requests.post(ENDPOINT, headers=headers, params=params, data=payload)
    results = json.loads(response.content)
    return results


path=sys.argv[1]
handler(path)