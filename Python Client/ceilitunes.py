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
buttonWidth = 400
buttonHeight = 40
buttonSpacing = 50

# set up the screen and fonts
rendering.setupWindow(screenSize, fontHeight)

def buildDisplay(book, path, prevTitle, buttonWidth, buttonHeight, buttonSpacing):
    title, chapterList = tunesets.getTitleAndChapters(book, path)
    backRect, buttonRects = rendering.showTitleAndChapterButtons(prevTitle, title, chapterList, buttonWidth, buttonHeight, buttonSpacing)
    return title, chapterList, backRect, buttonRects

# open the book
book = json.load(open(books.fetch('/book_json/1')))
path = []
prevTitle = None
bookTitle, chapterList, backRect, buttonRects = buildDisplay(book, path, prevTitle, buttonWidth, buttonHeight, buttonSpacing)
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
                path = path[:-1]
                if len(path) == 0: prevTitle = None
                elif len(path) == 1: prevTitle = bookTitle
                else: prevTitle = path[-1]
                title, chapterList, backRect, buttonRects = buildDisplay(book, path, prevTitle, buttonWidth, buttonHeight, buttonSpacing)
            else:
                i = 0
                for rect, chapter in zip(buttonRects, chapterList):
                    if rect.collidepoint(event.pos):
                        if type(chapter) is list:
                            setTitle = chapter[0]
                            tuneSet = tunesets.prepareSet(chapter[2], columnWidth)
                            rendering.renderSet(setTitle, tuneSet, textHeight, columnWidth, gutterWidth, topOffset)
                            awaitClick()
                            title, chapterList, backRect, buttonRects = buildDisplay(book, path, prevTitle, buttonWidth, buttonHeight, buttonSpacing)
                        else:
                            prevTitle = title
                            path.append(chapter)
                            title, chapterList, backRect, buttonRects = buildDisplay(book, path, prevTitle, buttonWidth, buttonHeight, buttonSpacing)
                    i += 1
        pygame.time.wait(50)
