import time


def done():
    load_t2 = time.time()
    load_time = str(load_t2 - load_t1)[0:3]
    print('Loading complete ({} seconds). Hold tab and press the "print screen" button to analyze and get counters.'
          .format(load_time))

print('Loading "I Need a Hero", by Kataiser...')  # don't overthink this
print("https://github.com/Kataiser/I-Need-a-Hero")
load_t1 = time.time()
