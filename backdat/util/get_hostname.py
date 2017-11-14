import platform  # only for platform.node() to get hostname

def get_hostname():
    """ returns the hostname of the current host """
    return str(platform.node()).split(".")[0]
