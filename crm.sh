#!/bin/bash
path=/home/softit/Integration_crm
cd path
source ${path}/venv/bin/activate

while true;
do
  truncate -s 0 nohup.out
	python3 ${path}/run.py;
	sleep 60;
done
