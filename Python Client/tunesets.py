import images

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

def prepareSet(tunes, columnWidth):
    theSet = list()
    for image_url, title, repeats in tunes:
        image_path = images.fetch(image_url)
        imageHeight, img = images.openScaledImage(image_path, columnWidth)
        theSet.append((title, repeats, imageHeight, img))
    return theSet
