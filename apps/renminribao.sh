#!/bin/bash

YEAR=$(date +%Y)
MONTH=$(date +%m)
DAY=$(date +%d)

FILE_NAME_PDF="rmrb${YEAR}${MONTH}${DAY}01.pdf"
FILE_OUTPUT_PATH="output"
FILE_DOWNLOAD_PATH="output/downloads"
FILE_PATH_CANVAS="${FILE_OUTPUT_PATH}/canvas.BMP"
FILE_NAME_BMP="rmrb${YEAR}${MONTH}${DAY}01.bmp"
FILE_NAME_BMP_RESIZE="rmrb${YEAR}${MONTH}${DAY}01-resize.bmp"
FILE_NAME_BMP_FINAL="rmrb${YEAR}${MONTH}${DAY}01-final.bmp"
FILE_URL="http://paper.people.com.cn/rmrb/images/${YEAR}-${MONTH}/${DAY}/01/${FILE_NAME_PDF}"


if [ ! -f "${FILE_DOWNLOAD_PATH}/${FILE_NAME_PDF}" ]; then
  mkdir -p "${FILE_DOWNLOAD_PATH}"
  echo "$(date) Download and save file to ${FILE_DOWNLOAD_PATH}/${FILE_NAME_PDF}"
  curl "$FILE_URL" -o "${FILE_DOWNLOAD_PATH}/${FILE_NAME_PDF}"
  echo "$(date) Downloaded"
fi

echo "$(date) Convert: From PDF to initial BMP file"
convert -rotate 270 -density 100 "${FILE_DOWNLOAD_PATH}/${FILE_NAME_PDF}" "${FILE_OUTPUT_PATH}/${FILE_NAME_BMP}"

echo "$(date) Convert: Resize file to 1812x1404"
convert -resize 1812x1404 "${FILE_OUTPUT_PATH}/${FILE_NAME_BMP}" "${FILE_OUTPUT_PATH}/${FILE_NAME_BMP_RESIZE}"

if [ ! -f "$FILE_PATH_CANVAS" ]; then
  echo "$(date) Creating canvas file"
  convert -size 1872x1404 xc:white "$FILE_PATH_CANVAS"
fi
echo "$(date) Convert: Attach to empty canvas"
convert "$FILE_PATH_CANVAS" "${FILE_OUTPUT_PATH}/${FILE_NAME_BMP_RESIZE}" \
    -geometry +30+61 -composite "${FILE_OUTPUT_PATH}/${FILE_NAME_BMP_FINAL}"

echo "$(date) Sending to ePaper"
sudo ./pf "${FILE_OUTPUT_PATH}/${FILE_NAME_BMP_FINAL}"

echo "$(date) Clean generated files"
rm -f "${FILE_OUTPUT_PATH}/${FILE_NAME_BMP}" "${FILE_OUTPUT_PATH}/${FILE_NAME_BMP_RESIZE}" \
    "${FILE_OUTPUT_PATH}/${FILE_NAME_BMP_FINAL}"
