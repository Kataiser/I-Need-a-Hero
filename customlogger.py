import time


def info(message):
    current_time = str(time.strftime('%c'))
    log_file = open(filename, 'a')
    log_file.write("[{}] INFO: {}\n".format(current_time, message))
    log_file.close()


def debug(message):
    current_time = str(time.strftime('%c'))
    log_file = open(filename, 'a')
    log_file.write("[{}] DEBUG: {}\n".format(current_time, message))
    log_file.close()


def error(message):
    current_time = str(time.strftime('%c'))
    log_file = open(filename, 'a')
    log_file.write("[{}] ERROR: {}\n".format(current_time, message))
    log_file.close()


def critical(message):
    current_time = str(time.strftime('%c'))
    log_file = open(filename, 'a')
    log_file.write("[{}] CRITICAL: {}\n".format(current_time, message))
    log_file.close()


def clear():
    open(filename, 'w').close()

filename = str('logs/' + str(round(time.time())) + '.log')

try:
    open(filename, 'x')
except FileExistsError:
    pass
