import time
import os
import sys

try:
    from raven import breadcrumbs
except ImportError:
    print('Raven could not be imported, so logging will be sparse', file=sys.stderr)
    breadcrumbs = None
    pass
from resources import exception_handler


def write_log(level, message_out):
    current_time = str(time.strftime('%c'))
    time_since_start = format(time.perf_counter() - start_time, '.4f')  # the format() adds trailing zeroes
    if not os.path.exists('logs'):
        os.mkdir('logs')
    try:
        log_file = open(filename, 'a')
    except FileNotFoundError:
        return
    full_line = "[{} +{}] {}: {}\n".format(current_time, time_since_start, level, message_out)
    log_file.write(full_line)
    log_file.close()
    if to_stderr:
        print(full_line, file=sys.stderr)
    if breadcrumbs:
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
    try:
        all_logs = sorted(os.listdir('logs'))
    except FileNotFoundError:
        return
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
to_stderr = False

try:
    open(filename, 'x')
except (FileExistsError, FileNotFoundError):
    pass
