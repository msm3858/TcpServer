#!/usr/bin/env bash

DIRECTORY_TO_ZIP='4chanWebScrapper'
DIRECTORY="/home/msm/PycharmProjects/$DIRECTORY_TO_ZIP"

MODIFICATION_TIME_OF_DIRECTORY=$(date -r $DIRECTORY +"%Y%m%d%H%M")
OLDER_THAN_NOW_5_MIN=$(date -d '5 minutes ago' +"%Y%m%d%H%M")
OUTPUT_DIRECTORY="/data/"
echo $MODIFICATION_TIME_OF_DIRECTORY
echo $OLDER_THAN_NOW_5_MIN

if [[ $MODIFICATION_TIME_OF_DIRECTORY -ge $OLDER_THAN_NOW_5_MIN ]];
then
    echo "Directory $DIRECTORY_TO_ZIP was changed recently..."
    echo "Updating..."
    cd $DIRECTORY
    zip -r "$OUTPUT_DIRECTORY/$DIRECTORY_TO_ZIP.zip" *
fi
