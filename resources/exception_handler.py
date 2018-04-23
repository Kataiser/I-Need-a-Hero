import traceback
import sys

try:
    from raven import Client
    sentry_enabled = True
except ImportError:
    print("Raven could not be imported, so sentry is disabled.", file=sys.stderr)
    sentry_enabled = False


def log_any_uncaught_exception(*exc_info):
    tb = "".join(traceback.format_exception(*exc_info))
    log.critical("Unhandled exception: {}".format(tb))
    if sentry_enabled:
        # client.captureException(exc_info)
        pass
    raise SystemError


def format_caught_exception(exc_info):
    tb = "".join(traceback.format_exception(*exc_info))
    if sentry_enabled:
        # client.captureException(exc_info)
        pass
    return tb


def setup_excepthook():
    sys.excepthook = log_any_uncaught_exception


def sentry_mode(enabled):  # activated!
    global sentry_enabled
    if enabled != sentry_enabled:
        log.info("Sentry mode changed to {}".format(enabled))
    sentry_enabled = enabled


if sentry_enabled:
    client = Client(dsn='https://891e30a1022e4779a11e338953052327:be5cc4d0753d42fc84521b0876ab1463@sentry.io/211260',
                release='1.6')
else:
    client = None

from resources import customlogger as log  # ew
