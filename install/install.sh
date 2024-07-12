#!/bin/bash

# Get the current directory
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if start_beachbot_ap.sh exists
if [ ! -f "$CURRENT_DIR/start_beachbot_ap.sh" ]; then
    echo "Error: start_beachbot_ap.sh not found in the current directory."
    exit 1
fi

# Create a new sudoers file for the script
echo "%sudo ALL=NOPASSWD: $CURRENT_DIR/start_beachbot_ap.sh" | sudo tee /etc/sudoers.d/start_beachbot_ap

# Create the systemd service unit file
cat <<EOF > /etc/systemd/system/start_beachbot_ap.service
[Unit]
Description=Start Beachbot AP Script
After=network.target

[Service]
Type=simple
ExecStart=$CURRENT_DIR/start_beachbot_ap.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload
# Enable and start the service
sudo systemctl enable start_beachbot_ap.service
sudo systemctl start start_beachbot_ap.service
