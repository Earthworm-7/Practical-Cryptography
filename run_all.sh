#!/bin/bash
source project_venv/bin/activate &
python3 access_control.py &
python3 database.py &
python3 data_encryption.py &
python3 data_transmission.py &
python3 gui.py &
python3 main.py &
python3 user_auth.py &
wait
