import pygame
from pygame.locals import *
import tunesets

# assorted colors
WHITE = 255,255,255
GREY = 200,200,200
GREEN = 0,255,0
BLACK = 0,0,0
BLUE  = 0,0,255
RED   = 255,0,0

screenWidth = 1024
screenHeight = 768
theScreen = None
theFont = None

def setupWindow(screenSize, fontHeight):
    global screenWidth, screenHeight, theScreen, theFont
    pygame.init()
    screenWidth, screenHeight = screenSize
    theScreen = pygame.display.set_mode(screenSize)
    theFont = pygame.font.SysFont("arial", fontHeight, bold=True)

def setupFullscreen(screenSize, fontHeight):
    global screenWidth, screenHeight, theScreen, theFont
    pygame.init()
    screenWidth, screenHeight = screenSize
    theScreen = pygame.display.set_mode(screenSize, FULLSCREEN)
    theFont = pygame.font.SysFont("freesans", fontHeight, bold=True)

def renderTextTL(string, font, color, left, top):
    theScreen.blit(font.render(string, True, color), (left, top))

def renderTextTR(string, font, color, right, top):
    screenWidth, screenHeight = font.size(string)
    left = right - screenWidth
    theScreen.blit(font.render(string, True, color), (left, top))
    
def renderTextCenter(string, font, color, center, top):
    screenWidth, screenHeight = font.size(string)
    left = center - screenWidth/2
    theScreen.blit(font.render(string, True, color), (left, top))
    
def renderSet(setTitle, set, textHeight, columnWidth, gutterWidth, topOffset):
    theScreen.fill(WHITE)
    
    x = gutterWidth
    y = topOffset
    
    renderTextCenter(setTitle, theFont, BLUE, x + columnWidth/2, topOffset/2)

    theFont.set_underline(1)
    renderTextTL(set[0][0], theFont, BLUE, x+10, y)
    renderTextTR(set[0][1], theFont, BLUE, columnWidth+gutterWidth-10, y)
    theFont.set_underline(0)
    y += textHeight

    imageHeight = set[0][2]
    theScreen.blit(set[0][3], (x, y))
    y += imageHeight

    renderTextTL(set[1][0], theFont, BLUE, x+10, y)
    renderTextTR(set[1][1], theFont, BLUE, columnWidth+gutterWidth-10, y)
    y += textHeight

    imageHeight = set[1][2]
    theScreen.blit(set[1][3], (x, y))

    y = topOffset
    x += columnWidth + gutterWidth

    renderTextTL(set[2][0], theFont, BLUE, x+10, y)
    renderTextTR(set[2][1], theFont, BLUE, screenWidth-gutterWidth-10, y)
    y += textHeight

    imageHeight = set[2][2]
    theScreen.blit(set[2][3], (x, y))
    y += imageHeight

    if len(set) > 3:
        renderTextTL(set[3][0], theFont, BLUE, x+10, y)
        renderTextTR(set[3][1], theFont, BLUE, screenWidth-gutterWidth-10, y)
        y += textHeight
        imageHeight = set[3][2]
        theScreen.blit(set[3][3], (x, y))

    pygame.display.flip()

def renderTextCenter(string, font, color, center, top):
    screenWidth, screenHeight = font.size(string)
    left = center - screenWidth/2
    theScreen.blit(font.render(string, True, color), (left, top))
    
def makeButton(string, screenWidth, screenHeight, xc, yc):
    left = xc - screenWidth/2
    top = yc - screenHeight/2
    rect = Rect(left, top, screenWidth, screenHeight)
    pygame.draw.rect(theScreen, GREY, rect)
    pygame.draw.rect(theScreen, BLACK, rect, 4)
    screenWidth, screenHeight = theFont.size(string)
    left = xc - screenWidth/2
    top = yc - screenHeight/2
    theScreen.blit(theFont.render(string, True, BLUE), (left, top))
    return rect

def showTitleAndChapterButtons (prevTitle, title, chapterList, buttonWidth, buttonHeight, buttonSpacing):
    buttonRects = list()
    x = screenWidth/2
    y = buttonSpacing
    theScreen.fill(WHITE)
    renderTextCenter(title, theFont, BLUE, 300, y)
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
