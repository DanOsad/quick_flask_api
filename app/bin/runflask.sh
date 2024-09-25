#!/bin/bash

# RUNS FLASK SERVER WITH WAITRESS ON HOST MACHINE

export ENABLE_MONITORING=0
export SCRIPT_DIR=$(dirname $(realpath $0))
export API_DIR=$(dirname $SCRIPT_DIR)
export LOG_DIR="$API_DIR/logs"

# Create LOG_DIR if not exists
[[ ! -d "$LOG_DIR" ]] && mkdir -p "$LOG_DIR"

cd $API_DIR
source .venv/bin/activate
# waitress-serve --url-prefix=/ --listen=0.0.0.0:4040 app:app
python app.py
deactivate