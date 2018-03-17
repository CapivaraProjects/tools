#!/bin/bash

# This script create a set of images in TARGET_DIR with the number 
# of samples defined by paramater NIMAGES for each class that the
# model has been training 

MISSING_ARGS=4
if [ $# -lt "$MISSING_ARGS" ]; then
	echo "No arguments provided"
	echo "  usege: ${0} SOURCE_DIR TARGET_DIR NMAGES TEST"
	echo "  where:
        SOURCE_DIR 	the original images directory
        TARGET_DIR 	where the samples will be copy
        NMAGES 		how many images you want for this sample
        TEST 		if test put '1' else '0'; this ignore the number of images"
	exit 0
fi 

SOURCE_DIR=$1 #plantvillage/thumb (+/Apple to a specifc plant)
TARGET_DIR=$2 #plantvillage/sample
NIMAGES=$3 # number of images for each training class
TEST=$4
IS_TEST=1


for candidate_class in ${SOURCE_DIR}/*; do
	if [ -d "${candidate_class}" ]; then
		if [ "$(ls -1 ${candidate_class}/* | wc -l)" -ge ${NIMAGES} ]; then
			candidate=${candidate_class:19:${#candidate_class}}
            echo "CAND ${candidate}"
			plant_sample=${TARGET_DIR}/${candidate}
			mkdir -p ${plant_sample}
            echo "coping from ${candidate_class} to ${plant_sample})"
	    	if [ "${TEST}" -eq "${IS_TEST}" ] ; then
			    cp -r $(ls -1 ${candidate_class}/* | sort -R | head -2) ${plant_sample}
			else
				cp -r $(ls -1 ${candidate_class}/* | sort -R | head -${NIMAGES}) ${plant_sample}
			fi				
		fi
    fi
done
