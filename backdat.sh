#!/bin/bash
echo $(date)
echo "----------------------------------------------------"
echo $PATH
echo "----------------------------------------------------"
echo $PYTHONPATH
echo "----------------------------------------------------"
echo $LD_LIBRARY_PATH
echo "----------------------------------------------------"
cd /home/tylar/backdat
/usr/bin/env python3 /home/tylar/backdat/backdat.py &> /var/opt/backdat/cronjob.log
