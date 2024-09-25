#!/bin/bash

# Get name from user
read -p "Enter a name for your API: " api_title
API_TITLE=$(echo "$api_title" | tr '[:upper:]' '[:lower:]')
API_TITLE_UPPER=$(echo "$API_TITLE" | tr '[:lower:]' '[:upper:]')
# export API_TITLE="$API_TITLE"

# Create dir
API_DIR="$PWD/$API_TITLE""_api"
echo "Creating flask app in $API_DIR"
mkdir -p "$API_DIR"

# Generate .env file + source
ENV_DIR="$API_DIR/.env"

env_contents=""
env_contents+="# Add environment variables here"$'\n'
env_contents+=$'\n'
env_contents+="API_TITLE=$API_TITLE"
env_contents+=$'\n'
env_contents+="# DB Settings here"$'\n'
env_contents+="$API_TITLE_UPPER""_DB_HOST=\"db_host_dns_or_ip\""$'\n'
env_contents+="$API_TITLE_UPPER""_DB_USER=\"db_username\""$'\n'
env_contents+="$API_TITLE_UPPER""_DB_PASSWORD=\"db_password\""$'\n'
env_contents+="$API_TITLE_UPPER""_DB_SCHEMA=\"db_schema\""$'\n'
env_contents+=$'\n'
env_contents+="# Flask Settings here"$'\n'
env_contents+="$API_TITLE_UPPER""_API_PORT=5000"$'\n'
env_contents+="$API_TITLE_UPPER""_API_THREADS=4"$'\n'
env_contents+=""$'\n'
env_contents+="# Cache Settings here"$'\n'
env_contents+="CACHE_TYPE=\"rediscache\""$'\n'
env_contents+=""$'\n'

echo "$env_contents" > $ENV_DIR

# Copy files
SOURCE_DIR=$(dirname $(realpath $0))
cp -R $SOURCE_DIR/app "$API_DIR"
cp -R $SOURCE_DIR/nginx "$API_DIR"
cp $SOURCE_DIR/docker-compose.yml "$API_DIR"

# Replace env var names in 'app.py'
APP_PY_FILE="$API_DIR/app/app.py"
echo "Now editing $APP_PY_FILE"
sed -i "s/%API_TITLE_UPPER/$API_TITLE_UPPER/g" "$APP_PY_FILE"

SETUP_PY_FILE="$API_DIR/app/extensions/setup.py"
echo "Now editing $SETUP_PY_FILE"
sed -i "s/%API_TITLE_UPPER/$API_TITLE_UPPER/g" "$SETUP_PY_FILE"
sed -i "s/%API_TITLE/$API_TITLE/g" "$SETUP_PY_FILE"

DOCKER_COMPOSE_FILE="$API_DIR/docker-compose.yml"
echo "Now editing $DOCKER_COMPOSE_FILE"
sed -i "s|%API_DIR|$API_DIR|g" "$DOCKER_COMPOSE_FILE"
sed -i "s/%API_TITLE/$API_TITLE/g" "$DOCKER_COMPOSE_FILE"

NGINX_CONF_FILE="$API_DIR/nginx/nginx.conf"
echo "Now editing $NGINX_CONF_FILE"
sed -i "s/%API_TITLE/$API_TITLE/g" "$NGINX_CONF_FILE"

# exit 0

if [[ "$@" == *-docker* ]]; then
    # Open permissions on logs dir (docker volume)
    chmod 777 $API_DIR/app/logs

    # Run docker-compose
    cd $API_DIR
    docker-compose up --build -d --scale app=2

else
    # Install venv + requirements
    echo "Installing python virtual environment"
    "$SOURCE_DIR"/create_py_env.sh "$API_DIR"

    # Create systemctl file
    SYSD_PATH="/etc/systemd/system"
    SYSD_NAME="$API_TITLE.service"

    systemd_file=""
    systemd_file+="[Unit]"$'\n'
    systemd_file+="Description=$API_TITLE_UPPER flask web service"$'\n'
    systemd_file+="After=network.target"$'\n'
    systemd_file+=$'\n'
    systemd_file+="[Service]"$'\n'
    systemd_file+="User=$USER"$'\n'
    systemd_file+="WorkingDirectory=$API_DIR"$'\n'
    systemd_file+="ExecStart=/bin/bash $API_DIR/bin/runflask.sh"$'\n'
    systemd_file+="Restart=always "$'\n'
    systemd_file+=$'\n'
    systemd_file+="[Install]"$'\n'
    systemd_file+="WantedBy=multi-user.target"$'\n'

    # sudo echo "$systemd_file" > "$SYSD_PATH/$SYSD_NAME"
    echo "$systemd_file" | sudo tee "$SYSD_PATH/$SYSD_NAME" > /dev/null

    # Start service
    sudo systemctl enable "$SYSD_NAME"
    sudo systemctl start "$SYSD_NAME"
fi

