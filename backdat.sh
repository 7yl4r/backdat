#!/bin/bash
# This script loosely wraps backdat.py for debugging purposes.
# You should probably call backdat.py directly.
echo $(date)
echo "----------------------------------------------------"
echo $PATH
echo "----------------------------------------------------"
echo $PYTHONPATH
echo "----------------------------------------------------"
echo $LD_LIBRARY_PATH
echo "----------------------------------------------------"
cd /opt/backdat
/usr/bin/env python3 /opt/backdat/backdat.py #&> /var/opt/backdat/cronjob.log
