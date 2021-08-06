#!/bin/bash

chmod +x ./monitor.py
sudo chown root:root ./monitor.py
sudo chmod u+s ./monitor.py
pip3 install -r ./requirements.txt
