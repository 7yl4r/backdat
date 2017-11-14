import logging

class DuplicateLogFilter(logging.Filter):
    """
    This filter prevents duplicate messages from being printed repeatedly.
    Adapted from https://stackoverflow.com/a/44692178/1483986
    """
    def filter(self, record):
        # add other fields if you need more granular comparison, depends on your app
        current_log = (record.module, record.levelno, record.msg)
        if current_log != getattr(self, "last_log", None):
            self.last_log = current_log
            return True
        return False
