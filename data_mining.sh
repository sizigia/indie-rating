#!/bin/bash

set -e

source env/bin/activate

echo "Scraping IMDb movies" && python script1.py && echo "Done scraping IMDb movies" &

echo "Scraping Film Independent Spirit Awards" && python script2.py && echo "Cleaning Independent Spirit Awards CSV" && python script3.py && echo "Done"