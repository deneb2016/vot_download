import urllib.request
import json
import requests
from zipfile import ZipFile
import os
from os.path import join as join
import sys

year = sys.argv[1]

assert year in ['2016', '2017', '2018', '2019']

base_url = 'https://data.votchallenge.net/vot%s/main/' % year
base_path = './VOT%s' % year

if not os.path.exists(base_path):
    os.mkdir(base_path)

print('Downloading json file...')
description = urllib.request.urlopen(base_url + 'description.json').read()
description = json.loads(description)
sequences = description['sequences']

for i, seq in enumerate(sequences):
    print('Downloading %s sequence %d/%d...' % (seq['name'], i + 1, len(sequences)))
    here_path = join(base_path, seq['name'])
    if not os.path.exists(here_path):
        os.mkdir(here_path)

    # download and unzip annotations
    anno_path = join(here_path, 'anno.zip')
    anno = requests.get(base_url + seq['annotations']['url'])
    with open(anno_path, 'wb') as file:
        file.write(anno.content)
        file.flush()
        zipObj = ZipFile(anno_path, 'r')
        zipObj.extractall(here_path)
        os.remove(anno_path)

    # downad and unzip images
    img_path = join(here_path, 'img.zip')
    img = requests.get(base_url + seq['channels']['color']['url'])
    with open(img_path, 'wb') as file:
        file.write(img.content)
        file.flush()
        zipObj = ZipFile(img_path, 'r')
        zipObj.extractall(here_path)
        os.remove(img_path)