
path=/home/softit/Integration_crm
while true;
do
  cd path
  source ${path}/venv/bin/activate
	python3 ${path}/run.py;
	sleep 30;
done
