#!/bin/bash

# Get install directory from argument
API_DIR="$1"

# Enter install directory
cd $API_DIR

# Create a Python virtual environment using the selected Python version
"/tools/python/python3.6/bin/python" -m venv "$API_DIR/.venv"

# Declare VARS
VENV_DIR="$API_DIR/.venv"
VENV_BIN="$VENV_DIR/bin"
VENV_LIB="$VENV_DIR/lib"
VENV_PKG="$VENV_LIB/python3.6/site-packages"

# Modify the activate script
ACTIVATE_SCRIPT="$VENV_BIN/activate"
if grep -q "export VIRTUAL_ENV" "$ACTIVATE_SCRIPT"; then
    sed -i "/export VIRTUAL_ENV/a export PYTHONPATH=\"$VENV_PKG\"" "$ACTIVATE_SCRIPT"
else
    echo "export PYTHONPATH=\"$VENV_PKG\"" >> "$ACTIVATE_SCRIPT"
fi

# Modify the activate.csh script
ACTIVATE_CSH_SCRIPT="$VENV_BIN/activate.csh"
if grep -q "setenv VIRTUAL_ENV" "$ACTIVATE_CSH_SCRIPT"; then
    sed -i "/setenv VIRTUAL_ENV/a setenv PYTHONPATH \"$VENV_PKG\"" "$ACTIVATE_CSH_SCRIPT"
else
    echo "setenv PYTHONPATH \"$VENV_PKG\"" >> "$ACTIVATE_CSH_SCRIPT"
fi

# Create a pip.conf file in the .venv directory
cat << EOF > "$API_DIR/.venv/pip.conf"
[global]
target = $VENV_PKG
no-cache-dir = true
cache-dir = $VENV_LIB/pip-cache

[install]
ignore-installed = true
EOF

# Install packages from requirements.txt
source "$ACTIVATE_SCRIPT"
echo "Updating PIP"
pip install --upgrade pip
echo "Installing requirements.txt into $VENV_DIR"
pip install -r requirements.txt
deactivate
