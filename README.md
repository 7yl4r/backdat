# backdat
backdat data up.

An attempt at declarative backup.

A backup plan is generated according to information given about your fileset, backup resources, and other preferences. Version 1 user-interface is all text file editing. A mockup of the settings files is in [this gist](https://gist.github.com/7yl4r/01a4505ec8462268a4c69944047d1c69).

# Usage in Current State

0. define host-level settings in `/etc/opt/backdat/host-settings.cfg`
1. modify `/var/opt/backdat/backup-plan.tsv` to include backups you want
2. `sudo /home/tylar/backdat/backdat.sh` will do one of two things:
    * start the backup if within the backup window (and schedule next backup once done)
    * schedule the next run for the start of the next backup window in `/etc/cron.d/backdat`
