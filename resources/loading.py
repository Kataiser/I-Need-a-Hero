import time
from resources import exception_handler


def done():
    load_t2 = time.perf_counter()
    load_time = str(load_t2 - load_t1)[0:3]
    print('Loading complete ({} seconds). Hold tab and press the "print screen" button to analyze and get counters.'
          .format(load_time))
    return load_time


exception_handler.setup_excepthook()

print('Loading "I Need a Hero", by Kataiser...')
print("https://github.com/Kataiser/I-Need-a-Hero")
load_t1 = time.perf_counter()

# don't overthink this
