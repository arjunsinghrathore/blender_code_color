import config
import os


def announce(message, token="", num=None, force=False):
    """
    If VERBOSE, print announcement
    """
    if config.VERBOSE or force:
        if len(token):
            if num is None:
                # gets the number of columns in the shell
                # to pretty print a token all the way across
                try:
                    _, columns = os.popen('stty size', 'r').read().split()
                except ValueError:
                    columns = 50
                columns = int(columns)
            else:
                columns = num
            print(token * columns)
        print(message)
