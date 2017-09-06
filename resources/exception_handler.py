import traceback
import sys

from raven import Client


def log_any_uncaught_exception(*exc_info):
    tb = "".join(traceback.format_exception(*exc_info))
    log.critical("Unhandled exception: {}".format(tb))
    if sentry_enabled:
        client.captureException(exc_info)
    raise SystemError


def format_caught_exception(exc_info):
    tb = "".join(traceback.format_exception(*exc_info))
    if sentry_enabled:
        client.captureException(exc_info)
    return tb


def setup_excepthook():
    sys.excepthook = log_any_uncaught_exception


def disable_sentry():
    global sentry_enabled
    sentry_enabled = False

client = Client('https://891e30a1022e4779a11e338953052327:be5cc4d0753d42fc84521b0876ab1463@sentry.io/211260')
sentry_enabled = True

from resources import customlogger as log  # ew
