import os, sys, platform, random
import pygame
from pygame.locals import *
import requests, json

import books, images, tunesets, rendering

# screen dimensions
screenSize = width, height = 2*960, 2*540
fontHeight = 20
textHeight = 30
gutterWidth = 110
topOffset = 70
columnWidth = (width - 3*gutterWidth)/2
buttonWidth = 300
buttonHeight = 40
buttonSpacing = 50

# set up the screen and fonts
rendering.setupWindow(screenSize, fontHeight)

def buildDisplay(book, path, prevTitle, buttonWidth, buttonHeight, buttonSpacing):
    title, chapterList = tunesets.getTitleAndChapters(book, path)
    backRect, buttonRects = rendering.showTitleAndChapterButtons(prevTitle, title, chapterList, buttonWidth, buttonHeight, buttonSpacing)
    return title, chapterList, backRect, buttonRects

# open the book and set up initial display showing book structure
book = json.load(open(books.fetch('/book_json/1', force=True)))
path = []
prevTitle = None
bookTitle, chapterList, backRect, buttonRects = buildDisplay(book, path, prevTitle, buttonWidth, buttonHeight, buttonSpacing)
title = bookTitle

def awaitClickOrKey():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                waiting = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit(0)
                else:
                    return event.key
            elif event.type == pygame.QUIT:
                sys.exit()
        pygame.time.wait(50)
    return None

def displaySet(set):
    setTitle = set[0]
    repeat = set[1]
    pageOffset = 0
    tuneSet = tunesets.prepareSet(set[2], columnWidth)
    
    while True:
        rendering.renderSet(setTitle, tuneSet, repeat, pageOffset, textHeight, columnWidth, gutterWidth, topOffset)
        keyPressed = awaitClickOrKey()
        if keyPressed is None:
            break
        elif keyPressed == K_DOWN:
            pageOffset += 1
        elif keyPressed == K_UP:
            if pageOffset > 0: pageOffset -= 1

# Main event loop: Display chapter structure
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.display.quit()
                sys.exit(0)
            elif event.key == K_DOWN:
                print 'Down'
                continue
            elif event.key == K_UP:
                print 'Up'
                continue
        elif event.type == MOUSEBUTTONDOWN:
            if backRect.collidepoint(event.pos):
                # user clicked back button: display chapter 1 level up
                path = path[:-1]
                if len(path) == 0: prevTitle = None
                elif len(path) == 1: prevTitle = bookTitle
                else: prevTitle = path[-1]
                title, chapterList, backRect, buttonRects = buildDisplay(book, path, prevTitle, buttonWidth, buttonHeight, buttonSpacing)
            else:
                i = 0
                for rect, chapter in zip(buttonRects, chapterList):
                    if rect.collidepoint(event.pos):
                        # user clicked on a chapter or set button
                        if type(chapter) is list:
                            # display set
                            displaySet(chapter)
                            # return to current chapter display level when done
                            title, chapterList, backRect, buttonRects = buildDisplay(book, path, prevTitle, buttonWidth, buttonHeight, buttonSpacing)
                        else:
                            # open and display chapter 1 level down
                            prevTitle = title
                            path.append(chapter)
                            title, chapterList, backRect, buttonRects = buildDisplay(book, path, prevTitle, buttonWidth, buttonHeight, buttonSpacing)
                    i += 1
        pygame.time.wait(50)
