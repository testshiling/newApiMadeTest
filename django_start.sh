docker run -d --name lxl_code3 -v /root/newApiMadeTest:/usr/src/app -w /usr/src/app -p 80:8000 python:3.7.2 bash -c "/usr/src/app/run.sh"
