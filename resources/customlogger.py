import time
import os


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


def cleanup(max_logs):
    all_logs = sorted(os.listdir('logs'))
    overshoot = max_logs - len(all_logs)
    deleted = 0
    while overshoot < 0:
        deleted += 1
        log_to_delete = all_logs.pop(0)
        os.remove('logs/' + log_to_delete)
        overshoot = max_logs - len(all_logs)
    info("Deleted " + str(deleted) + " log(s)")


filename = str('logs/' + str(round(time.time())) + '.log')

try:
    open(filename, 'x')
except FileExistsError:
    pass
