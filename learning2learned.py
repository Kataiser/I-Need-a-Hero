from PIL import Image
import os

import namenum_converter as conv


def average_images(*arg):
    input_num = len(arg)
    print("Averaging", input_num, "images")
    print("From " + arg[0] + " to " + arg[-1])

    if input_num == 1:
        return Image.open(arg[0])

    opened_images = []
    for filename in arg:
        opened_images.append(Image.open(filename).convert('RGBA'))

    output = Image.blend(opened_images[0], opened_images[1], 0.5)

    if input_num > 2:
        for inputs in range(2, input_num):
            alpha = 1 / (inputs + 1)
            output = Image.blend(output, opened_images[inputs], alpha)

    mask = Image.open('mask.png').convert('RGBA')
    output.paste(mask, (0, 0), mask)
    return output.convert('RGB')

heroes = ['ana', 'bastion', 'dva', 'genji', 'hanzo',
          'junkrat', 'lucio', 'mccree', 'mei', 'mercy',
          'pharah', 'reaper', 'reinhardt', 'roadhog', 'soldier',
          'sombra', 'symmetra', 'torbjorn', 'tracer', 'widowmaker',
          'winston', 'zarya', 'zenyatta', 'unknown', 'loading',
          'anadead', 'bastiondead', 'dvadead', 'genjidead', 'junkratdead',
          'luciodead', 'mccreedead', 'meidead', 'pharahdead', 'reaperdead',
          'roadhogdead', 'soldierdead', 'sombradead', 'torbjorndead', 'tracerdead',
          'zaryadead', 'zenyattadead', 'hanzodead', 'mercydead', 'orisadead',
          'reinhardtdead', 'symmetradead', 'widowmakerdead', 'winstondead', 'orisa']

learning_files = os.listdir('learning')

for hero in heroes:
    av_table = []

    for learning in learning_files:
        if 'dead' not in hero:
            if hero in learning and 'dead' not in learning:
                av_table.append('learning/' + learning)
        elif 'dead' in hero:
            if conv.strip_dead(hero) in learning and 'dead' in learning:
                av_table.append('learning/' + learning)
        else:
            print("welp")
            raise SystemExit

    av = average_images(*av_table)
    av.save('learned/' + hero + '.png')
