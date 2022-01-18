echo 'Starting API'
sudo /home/pi/ice-website/ice-library-api/venv/bin/python3 /home/pi/ice-website/ice-library-api/waitress_server.py > /home/pi/ice-website/ice-library-api/waitresslogs.txt 2>&1 &