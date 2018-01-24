#!/usr/bin/env python3
"""
class containing methods for doing things before or after a process
"""
import os
import subprocess

allowed_bash_cmds = ['virsh']

class ProcessWrapHandler(object):
    def __init__(self, config, file_path, parent_logger):
        """
        Parameters
        -------------
        config : dict
            Configuration dictionary of shape:
            ```
            self.config = {
                "pre": [],
                "post": [],
                "on_error": []
            }
            ```
        filename : str file path
            path to file we are processing
        """
        self.config = config
        self.filename = os.path.basename(os.path.splitext(file_path)[0])  # name, no extension
        self.logger = parent_logger  # logger passthrough (TODO: why?)

    def execute(wrapped_command):
        """
        Runs the pre-tasks, the wrapped process, then the post-tasks
        """
        try:
            self.logger.info('starting pre-job hooks...')
            self.pre()

            self.logger.info('starting wrapped job:')
            self.logger.info(str(wrapped_command))
            res_stdout = subprocess.check_output(
                wrapped_command,
                # stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            # self.logger.debug(res.args)

        except subprocess.CalledProcessError as sub_err:
            self.logger.error("wrapped subprocess failure; returned "+ str(sub_err.returncode))
            res_stdout = sub_err.output
            raise sub_err

        finally:
            self.logger.debug("\n############# BEGIN SUBPROCESS OUTPUT #############\n")
            self.logger.debug(res_stdout)

            self.logger.debug("\n#############  END SUBPROCESS OUTPUT  #############\n")
            # self.logger.info('subprocess exit w/ code ' + str(res.returncode))

            self.logger.info('starting post-job hooks...')
            self.post()

        return res_stdout

    def pre(self):
        self._do_each(self.config["pre"])

    def post(self):
        self._do_each(self.config["post"])

    def on_error(self):
        self._do_each(self.config["on_error"], logpath)

    def _do_each(self, arry):
        """ execute each task in given array """
        for task in arry:
            args = task.split()
            cmd = args[0]
            self.logger.info('executing task: ' + task + '...')
            if cmd == 'email_summary':
                self.logger.error("summary emailing disabled");
            if cmd in allowed_bash_cmds:
                bash_task = task.replace('$filename', self.filename)

                try: # subprocess.run was added in python3.5
                    res = subprocess.run(bash_task,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        universal_newlines=True,
                        shell=True
                    )
                    stdout = res.stdout
                except AttributeError as a_err: # this means python < v3.5
                    # fall back to subprocess.call
                    # https://docs.python.org/3/library/subprocess.html#call-function-trio
                    try:
                        stdout = subprocess.check_output(bash_task,
                            # stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True,
                            shell=True
                        )
                    except subprocess.CalledProcessError as p_err:
                        stdout = str(p_err)

                self.logger.debug(bash_task)

                self.logger.debug("\n############# BEGIN TASK OUTPUT #############\n")
                self.logger.debug(stdout)
                self.logger.debug("\n#############  END TASK OUTPUT  #############\n")

            else:
                raise AttributeError("unrecognized task: " + str(task))
