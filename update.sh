#!/bin/bash
echo 'Killing RamIfy Start Script'
pkill -9 -f run_RamIfy.sh
echo 'Killed.'
sleep 1
echo '5'
sleep 1
echo '4'
sleep 1
echo '3'
sleep 1
echo '2'
sleep 1
echo '1'
echo 'Updating'
git pull
echo '3'
sleep 1
echo '2'
sleep 1
echo '1'
echo 'Updating script-server (This might be broken.)'
/bin/bash script-server-upgrade.sh