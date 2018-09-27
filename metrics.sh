#!/bin/bash
#
# collection of quick metrics for monitoring collectors like telegraf
printf "{\n"
printf "\t\"backdat.plan_len\": `cat /var/opt/backdat/backup-plan.tsv | wc -l`,\n"
# printf "\t\"backdat.max_period\": `sudo /opt/backdat/backdat.py status --max_period`,\n"
# this next part is a bit hackish...
cat /var/opt/backdat/backup-stats.json | tr -d '{}'

printf "\n}\n"
