import re


def cut_off_command(command_message):
    """return command without '/' and the rest message"""
    result = re.match(r"/(\w+) (.*)", command_message)
    return result.group(1), result.group(2)