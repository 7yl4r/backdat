#!/usr/bin/env python3
"""
class containing methods for doing things before or after a process
"""
import os
import subprocess

#from gdrive_backup import emailer

allowed_bash_cmds = ['virsh']

class ProcessWrapHandler(object):
    def __init__(self, config, file_path, parent_logger):
        self.config = config
        self.filename = os.path.basename(os.path.splitext(file_path)[0])  # name, no extension
        self.logger = parent_logger  # logger passthrough

    def pre(self):
        self._do_each(self.config["pre"])

    def post(self, logpath):
        self._do_each(self.config["post"], logpath)

    def on_error(self, logpath):
        self._do_each(self.config["on_error"], logpath)

    def _do_each(self, arry, logpath=None):
        """ execute each task in given array """
        for task in arry:
            args = task.split()
            cmd = args[0]
            self.logger.info('executing task: ' + task + '...')
            if cmd == 'email_summary':
                #emailer.email_summary(args[1], logpath)
                self.logger.error("summary emailing disabled");
            if cmd in allowed_bash_cmds:
                bash_task = task.replace('$filename', self.filename)

                res = subprocess.run(bash_task,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    shell=True
                )
                self.logger.debug(res.args)

                self.logger.debug("\n############# BEGIN TASK OUTPUT #############\n")
                self.logger.debug(res.stdout)
                self.logger.debug("\n#############  END TASK OUTPUT  #############\n")

            else:
                raise AttributeError("unrecognized task: " + str(task))
