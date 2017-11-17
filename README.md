# backdat
backdat data up.

An attempt at declarative backup.

A backup plan is generated according to information given about your fileset, backup resources, and other preferences. Version 1 user-interface is all text file editing. A mockup of the settings files is in `/docs/example_files`.

# Usage in Current State

1. define host-level settings in `/etc/opt/backdat/host-settings.cfg`
2. list files you want backed up in `/etc/opt/backdat/fileset.tsv`
3. `sudo /opt/backdat/backdat.py plan` to generate a backup plan
4. `sudo /opt/backdat/backdat.py backup` will do one of two things:
    * if within the window from host-settings: start the backup then schedule next backup once done
    * else: schedule the next run for the start of the next backup window using `/etc/cron.d/backdat`
5. Done! backups should now run forever.

If you change your fileset, you will need to run `plan` again.
To check on your backups do `sudo /opt/backdat/backdat.py status` at any time.

## pre & post backup hooks with .backdatconfig
Commands can be run before or after the backup of a file.
One example usage is to pause a VM during the backup and resume on completion.
These pre & post hooks are controlled by adding a json .backdatconfig file to the directory you wish to hook.
See `./docs/example_files/.backdatconfig` for an example.

Bash commands that are allowed are listed in `ProcessWrapHandler.allowed_bash_cmds`.
Variables can be used in backup commands (actually just one for now):

* `$filename` - the name of the file being backed up
