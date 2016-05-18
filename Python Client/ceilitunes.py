import sys, os, pygame
from pygame.locals import *
import platform
import random
import requests
import json

# screen dimensions
size = width, height = 2*960, 2*540
if platform.system() != 'Windows':
    size = width, height = 1680, 1050

# assorted colors
WHITE = 255,255,255
GREY = 200,200,200
GREEN = 0,255,0
BLACK = 0,0,0
BLUE  = 0,0,255
RED   = 255,0,0

base_url = 'http://test123.podzone.net'
def get_image(image_url):
    # typical image_url is '/static/img/2.jpg
    fileName = image_url[12:]
    imagePath = 'images/' + fileName
    if not os.path.isfile(imagePath):
        # fetch the file only if not already in cache
        url = base_url + image_url
        r = requests.get(url, stream=True)
        with open(imagePath, 'wb') as fd:
            for chunk in r.iter_content(1024):
                fd.write(chunk)
    return imagePath

def setupScreen(serifHeight, sansHeight):
    pygame.init()
    if platform.system() == 'Windows':
        screen = pygame.display.set_mode(size)
        sans = pygame.font.SysFont("arial", sansHeight, bold=True)
    else:
        screen = pygame.display.set_mode(size, FULLSCREEN)
        sans = pygame.font.SysFont("freesans", sansHeight, bold=True)
    return screen, sans

def renderTextTL(string, font, color, left, top):
    screen.blit(font.render(string, True, color), (left, top))

def renderTextTR(string, font, color, right, top):
    width, height = font.size(string)
    left = right - width
    screen.blit(font.render(string, True, color), (left, top))
    
def renderTextCenter(string, font, color, center, top):
    width, height = font.size(string)
    left = center - width/2
    screen.blit(font.render(string, True, color), (left, top))
    
def openScaledImage(path, columnWidth):
    img = pygame.image.load(path)
    (iw, ih) = img.get_size()
    hwr = float(ih) / iw
    imageHeight = int(hwr * columnWidth);
    img = pygame.transform.smoothscale(img, (columnWidth, imageHeight))
    return imageHeight, img

def renderSet(setTitle, set, textHeight, columnWidth, gutterWidth, topOffset):
    screen.fill(WHITE)
    
    x = gutterWidth
    y = topOffset
    
    renderTextCenter(setTitle, sans, BLUE, x + columnWidth/2, topOffset/2)

    sans.set_underline(1)
    renderTextTL(set[0][0], sans, BLUE, x+10, y)
    renderTextTR(set[0][1], sans, BLUE, columnWidth+gutterWidth-10, y)
    sans.set_underline(0)
    y += textHeight

    imageHeight = set[0][2]
    screen.blit(set[0][3], (x, y))
    y += imageHeight

    renderTextTL(set[1][0], sans, BLUE, x+10, y)
    renderTextTR(set[1][1], sans, BLUE, columnWidth+gutterWidth-10, y)
    y += textHeight

    imageHeight = set[1][2]
    screen.blit(set[1][3], (x, y))

    y = topOffset
    x += columnWidth + gutterWidth

    renderTextTL(set[2][0], sans, BLUE, x+10, y)
    renderTextTR(set[2][1], sans, BLUE, width-gutterWidth-10, y)
    y += textHeight

    imageHeight = set[2][2]
    screen.blit(set[2][3], (x, y))
    y += imageHeight

    if len(set) > 3:
        renderTextTL(set[3][0], sans, BLUE, x+10, y)
        renderTextTR(set[3][1], sans, BLUE, width-gutterWidth-10, y)
        y += textHeight
        imageHeight = set[3][2]
        screen.blit(set[3][3], (x, y))

    pygame.display.flip()

def renderTextCenter(string, font, color, center, top):
    width, height = font.size(string)
    left = center - width/2
    screen.blit(font.render(string, True, color), (left, top))
    
def makeButton(string, width, height, xc, yc):
    left = xc - width/2
    top = yc - height/2
    rect = Rect(left, top, width, height)
    pygame.draw.rect(screen, GREY, rect)
    pygame.draw.rect(screen, BLACK, rect, 4)
    width, height = sans.size(string)
    left = xc - width/2
    top = yc - height/2
    screen.blit(sans.render(string, True, BLUE), (left, top))
    return rect

def isSetList (chapterList):
    return len(chapterList) == 0 or len(chapterList[0]) > 2

def getTitleAndChapters (book, path):
    chapterTitles = list()
    title, chapters = book
    if len(path) > 0:
        for chapter in chapters:
            if chapter[0] == path[0]:
                return getTitleAndChapters(chapter, path[1:])
    else:
        if isSetList(chapters):
            return title, chapters
        else:
            for chapter in chapters:
                chapterTitles.append(chapter[0])
    return title, chapterTitles

# set up the screen and fonts
screen, sans = setupScreen(20, 20)
textHeight = 30
gutterWidth = 110
topOffset = 70
columnWidth = (width - 3*gutterWidth)/2

buttonWidth = 400
buttonHeight = 40
buttonSpacing = 50

def showTitleAndChapterButtons (prevTitle, title, chapterList):
    buttonRects = list()
    x = width/2
    y = buttonSpacing
    screen.fill(WHITE)
    renderTextCenter(title, sans, BLUE, 300, y)
    y += buttonSpacing
    if prevTitle is None:
        backRect = Rect(0,0,0,0)
    else:
        backRect = makeButton('BACK to ' + prevTitle, buttonWidth, buttonHeight, 300, y)
    y = buttonSpacing
    for item in chapterList:
        legend = item
        if type(item) is list:
            legend = item[0]
        buttonRects.append(makeButton(legend, buttonWidth, buttonHeight, x, y))
        y += buttonSpacing
    pygame.display.flip()
    return backRect, buttonRects

def buildDisplay(book, path, prevTitle):
    title, chapterList = getTitleAndChapters(book, path)
    backRect, buttonRects = showTitleAndChapterButtons(prevTitle, title, chapterList)
    return title, chapterList, backRect, buttonRects

def prepareSet(tunes):
    theSet = list()
    for image_url, title, repeats in tunes:
        image_path = get_image(image_url)
        imageHeight, img = openScaledImage(image_path, columnWidth)
        theSet.append((title, repeats, imageHeight, img))
    return theSet

# open the book
book = json.load(open('book.json'))
path = []
prevTitle = None
bookTitle, chapterList, backRect, buttonRects = buildDisplay(book, path, prevTitle)
title = bookTitle

def awaitClick():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                waiting = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.display.quit()
                sys.exit(0)
            elif event.type == pygame.QUIT:
                sys.exit()
        pygame.time.wait(50)

# event loop
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.display.quit()
            sys.exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            if backRect.collidepoint(event.pos):
                path = path[:-1]
                if len(path) == 0: prevTitle = None
                elif len(path) == 1: prevTitle = bookTitle
                else: prevTitle = path[-1]
                title, chapterList, backRect, buttonRects = buildDisplay(book, path, prevTitle)
            else:
                i = 0
                for rect, chapter in zip(buttonRects, chapterList):
                    if rect.collidepoint(event.pos):
                        if type(chapter) is list:
                            setTitle = chapter[0]
                            tuneSet = prepareSet(chapter[2])
                            renderSet(setTitle, tuneSet, textHeight, columnWidth, gutterWidth, topOffset)
                            awaitClick()
                            title, chapterList, backRect, buttonRects = buildDisplay(book, path, prevTitle)
                        else:
                            prevTitle = title
                            path.append(chapter)
                            title, chapterList, backRect, buttonRects = buildDisplay(book, path, prevTitle)
                    i += 1
        pygame.time.wait(50)
