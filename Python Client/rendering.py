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
    
def renderSet(setTitle, set, repeat, wrapto, pageOffset, textHeight, columnWidth, gutterWidth, topOffset):
    theScreen.fill(WHITE)
    
    x = gutterWidth - pageOffset * (columnWidth + gutterWidth)
    y = topOffset
    
    renderTextCenter(setTitle, theFont, BLACK, screenWidth/2, topOffset/2)
    
    moreToTheLeft = pageOffset > 0
    moreToTheRight = False
    firstTuneInView = False
    
    i = 0
    while True:
        if (not repeat) and i >= (len(set) - 1):
            break

        tuneIndex = i
        while tuneIndex >= len(set):
            tuneIndex -= (len(set) - wrapto)
        tune = set[tuneIndex]
        tuneTitle = tune[0]
        repeats = tune[1]
        imageHeight = tune[2]
        tuneImage = tune[3]
        i += 1
        
        if (y + imageHeight) > screenHeight:
            x += columnWidth + gutterWidth
            y = topOffset
        if (x + columnWidth) > screenWidth:
            moreToTheRight = True
            break
        
        if x >= 0:
            if repeat and tuneIndex == 0:
                if firstTuneInView:
                    break
                firstTuneInView = True
            if repeat and tuneIndex == wrapto:
                theFont.set_underline(1)
            renderTextTL(tuneTitle, theFont, BLUE, x+10, y)
            renderTextTR(repeats, theFont, BLUE, x+columnWidth-10, y)
            if repeat and tuneIndex == wrapto:
                theFont.set_underline(0)
        y += textHeight
        
        if x >= 0:
            theScreen.blit(tuneImage, (x, y))
        y += imageHeight
    
    if moreToTheLeft:
        renderTextTL("<< More", theFont, BLACK, gutterWidth/2, topOffset - textHeight)
    if moreToTheRight:
        renderTextTR("More >>", theFont, BLACK, screenWidth - gutterWidth/2, topOffset - textHeight)

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
    x = 600
    y = buttonSpacing
    theScreen.fill(WHITE)
    renderTextCenter(title, theFont, BLUE, 200, y)
    y += buttonSpacing
    if prevTitle is None:
        backRect = Rect(0,0,0,0)
    else:
        backRect = makeButton('BACK to ' + prevTitle, buttonWidth, buttonHeight, 200, y)
    y = buttonSpacing
    for item in chapterList:
        legend = item
        if type(item) is list:
            legend = item[0]
        buttonRects.append(makeButton(legend, buttonWidth, buttonHeight, x, y))
        y += buttonSpacing
        if (y + buttonSpacing) > screenHeight:
            x += 350
            y = buttonSpacing
    pygame.display.flip()
    return backRect, buttonRects
