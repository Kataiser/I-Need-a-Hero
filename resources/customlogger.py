import time
import os

from raven import breadcrumbs
from resources import exception_handler


def write_log(level, message_out):
    current_time = str(time.strftime('%c'))
    time_since_start = format(time.perf_counter() - start_time, '.4f')  # the format() adds trailing zeroes
    log_file = open(filename, 'a')
    full_line = "[{} +{}] {}: {}\n".format(current_time, time_since_start, level, message_out)
    log_file.write(full_line)
    log_file.close()
    breadcrumbs.record(message=full_line, level=level)  # sentry level = custom level


def info(message_in):
    write_log('INFO', message_in)


def debug(message_in):
    write_log('DEBUG', message_in)


def error(message_in):
    write_log('ERROR', message_in)


def critical(message_in):
    write_log('CRITICAL', message_in)


def cleanup(max_logs):  # deletes older logs
    all_logs = sorted(os.listdir('logs'))
    overshoot = max_logs - len(all_logs)
    deleted = 0
    while overshoot < 0:
        deleted += 1
        log_to_delete = all_logs.pop(0)
        os.remove('logs/' + log_to_delete)
        overshoot = max_logs - len(all_logs)
    info("Deleted " + str(deleted) + " log(s)")

exception_handler.setup_excepthook()

start_time = time.perf_counter()
filename = str('logs/' + str(round(time.time())) + '.log')

try:
    open(filename, 'x')
except FileExistsError:
    pass
