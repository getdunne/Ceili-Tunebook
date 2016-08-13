import os
import requests
import pygame

base_url = 'http://test123.podzone.net'
#base_url = 'http://127.0.0.1:5000'

def fetch(image_url):
    # typical image_url is '/static/img/2.jpg
    fileName = image_url[image_url.rfind('/')+1:]
    imagePath = 'cache/' + fileName
    if not os.path.isfile(imagePath):
        # fetch the file only if not already in cache
        url = base_url + image_url
        r = requests.get(url, stream=True)
        with open(imagePath, 'wb') as fd:
            for chunk in r.iter_content(1024):
                fd.write(chunk)
    return imagePath

def openScaledImage(path, columnWidth):
    img = pygame.image.load(path)
    (iw, ih) = img.get_size()
    hwr = float(ih) / iw
    imageHeight = int(hwr * columnWidth);
    img = pygame.transform.smoothscale(img, (columnWidth, imageHeight))
    return imageHeight, img
