phantomjs.exe tune_image.js %1
magick convert temp.png -trim -bordercolor White -border 40 %2/%1.png
