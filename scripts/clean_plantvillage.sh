#!/bin/bash

# This script remove all JPG or jpg files into plants directory 
# this files are duplicate and the most of then will be found into 
# categorical folder, healthy or some disesase directory for example.

SOURCE_DIR=$1 #plantvillage/thumb

# remove NON categorical images from SOURCE_DIR
for plant_dir in ${SOURCE_DIR}/*; do # Apple
	if [ -d "${plant_dir}" ]; then
		echo "clean up ${plant_dir}"
		if [ "$(ls -1 ${plant_dir}/*.jpg | wc -l)" -gt 1 ]; then
			rm ${plant_dir}/*.jpg 
		fi
		if [ "$(ls -1 ${plant_dir}/*.JPG | wc -l)" -gt 1 ]; then
			rm ${plant_dir}/*.JPG
		fi
		if [ "$(ls -1 ${plant_dir}/*.png | wc -l)" -gt 1 ]; then
			rm ${plant_dir}/*.png
		fi
		if [ "$(ls -1 ${plant_dir}/*.PNG | wc -l)" -gt 1 ]; then
			rm ${plant_dir}/*.PNG
		fi
	fi
done

