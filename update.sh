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
echo "This will error if the paths aren't set correctly in the script-server-upgrade file."
/bin/bash script-server-upgrade.sh
cat << "EOF"
  ____                   _ 
 |  _ \  ___  _ __   ___| |
 | | | |/ _ \| '_ \ / _ \ |
 | |_| | (_) | | | |  __/_|
 |____/ \___/|_| |_|\___(_)
                           
  ____  _             _     ____            _       _     _   _               
 / ___|| |_ __ _ _ __| |_  / ___|  ___ _ __(_)_ __ | |_  | \ | | _____      __
 \___ \| __/ _` | '__| __| \___ \ / __| '__| | '_ \| __| |  \| |/ _ \ \ /\ / /
  ___) | || (_| | |  | |_   ___) | (__| |  | | |_) | |_  | |\  | (_) \ V  V / 
 |____/ \__\__,_|_|   \__| |____/ \___|_|  |_| .__/ \__| |_| \_|\___/ \_/\_/  
                                             |_|                              
EOF
