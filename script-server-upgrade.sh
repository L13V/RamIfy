#!/bin/bash
#
# Script-Server upgrade script
#
# Usage: upgrade.sh <Version>
# Usage: sudo upgrade.sh <Version>
# Usage: echo "myPAssw0rd" | sudo -S upgrade.sh <Version>
# Usage: echo "$SUDO_PASSWD" | sudo -S upgrade.sh <Version>
#
# Setting bash strict mode. See http://redsymbol.net/articles/unofficial-bash-strict-mode/
# Script will stop if error occurs
set -euo pipefail
# 
# scriptServerService: The name of the Script-Server service
scriptServerService="script-server"
# 
# scriptServerUser: The name of the user who run the service
scriptServerUser="script-server"
# 
# scriptServerInstall: Folder of the source files.
scriptServerInstall="/root/RamIfy-Server-and-Scripts/script-server"
#
#
datestr=`date +"%Y-%m-%dT%H-%M-%S"`
#
#
# Upgrade begin
cd /tmp/
echo "Backing up sources to ${scriptServerInstall}-${datestr}"
cp -r ${scriptServerInstall} ${scriptServerInstall}-${datestr}
echo "Cleaning temp files"
rm -rf script-server 2>/dev/null || true
rm -f script-server.zip 2>/dev/null || true
echo "Downloading new script-server sources"
wget https://github.com/bugy/script-server/releases/download/dev/script-server.zip
echo "Exracting..."
mkdir script-server
unzip ./script-server.zip -d ./script-server
echo "Stopping service"
service ${scriptServerService} stop
echo "Removing current sources."
rm -rf "${scriptServerInstall}/.*"
echo "Moving new source files"
cp -r ./script-server/* ${scriptServerInstall}
echo "Starting service"
service ${scriptServerService} start