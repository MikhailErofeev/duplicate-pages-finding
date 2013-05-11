#!/bin/bash

while true
do
    python mincemeat.py -p changeme localhost && python mincemeat.py -p changeme localhost
    sleep 1
done