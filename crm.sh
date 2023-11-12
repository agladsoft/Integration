#!/bin/bash
##path=/home/softit/Integration_crm
#path=/home/uventus/PycharmProjects/Integration_crm/
#cd path
#source ${path}/venv/bin/activate
#
#while true;
#do
#  truncate -s 0 nohup.out
#	python3 ${path}/run.py;
#	sleep 60;
#done

path=path=/home/softit/Integration_crm
cd $path
source ${path}/venv/bin/activate
while true; do
    truncate -s 0 ${path}/nohup.out
    python3 ${path}/run.py >> ${path}/nohup.out 2>&1
    if [ $? -ne 0 ]; then
        echo "Error executing python3. Exiting..."
        break
    fi
    sleep 60
done