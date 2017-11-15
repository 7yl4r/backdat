#!/bin/bash
#
# collection of quick metrics for monitoring collectors like telegraf
printf "{\n"
printf "\t\"backdat.plan_len\": `cat /var/opt/backdat/backup-plan.tsv | wc -l`\n"
printf "}\n"
