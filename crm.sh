#!/bin/bash
path=/home/softit/Integration_crm
cd path
source ${path}/venv/bin/activate
while true;
do
	python3 ${path}/run.py;
	sleep 30;
done
