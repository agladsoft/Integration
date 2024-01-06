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

path=/home/softit/Integration_crm
cd $path
source ${path}/venv/bin/activate

while true; do
    truncate -s 0 ${path}/nohup.out
    python3 ${path}/run.py

    if [ $? -ne 0 ]; then
        echo "Error executing python3. Restarting..."
    else
        echo "Python script executed successfully."
    fi

    # Ожидание 10 минут перед следующим запуском
    sleep 1200
done
