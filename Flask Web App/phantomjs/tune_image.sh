#!/bin/sh
./phantomjs tune_image.js $1
convert temp.png -trim -bordercolor White -border 40 $2/$1.png
