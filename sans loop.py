from PIL import Image
import re

screenshot = Image.open('input/unknown (4).png').resize((1920, 1080))

ally1 = screenshot.crop((443, 584, 519, 660))
ally2 = screenshot.crop((634, 584, 710, 660))
ally3 = screenshot.crop((826, 584, 902, 660))
ally4 = screenshot.crop((1019, 584, 1095, 660))
ally5 = screenshot.crop((1210, 584, 1286, 660))
ally6 = screenshot.crop((1402, 584, 1478, 660))
enemy1 = screenshot.crop((443, 279, 519, 355))
enemy2 = screenshot.crop((634, 279, 710, 355))
enemy3 = screenshot.crop((826, 279, 902, 355))
enemy4 = screenshot.crop((1019, 279, 1095, 355))
enemy5 = screenshot.crop((1210, 279, 1286, 355))
enemy6 = screenshot.crop((1402, 279, 1478, 355))

ally1.save('output/ally1.png')
ally2.save('output/ally2.png')
ally3.save('output/ally3.png')
ally4.save('output/ally4.png')
ally5.save('output/ally5.png')
ally6.save('output/ally6.png')
enemy1.save('output/enemy1.png')
enemy2.save('output/enemy2.png')
enemy3.save('output/enemy3.png')
enemy4.save('output/enemy4.png')
enemy5.save('output/enemy5.png')
enemy6.save('output/enemy6.png')

heroes = ['ana', 'bastion', 'dva', 'genji', 'hanzo',
          'junkrat', 'lucio', 'mccree', 'mei', 'mercy',
          'pharah', 'reaper', 'reinhardt', 'roadhog', 'soldier',
          'sombra', 'symmetra', 'torbjorn', 'tracer', 'widowmaker',
          'winston', 'zarya', 'zenyatta', 'unknown', 'loading',
          'anadead', 'bastiondead', 'dvadead', 'genjidead', 'junkratdead',
          'luciodead', 'mccreedead', 'meidead', 'pharahdead', 'reaperdead',
          'roadhogdead', 'soldierdead', 'sombradead', 'torbjorndead', 'tracerdead',
          'zaryadead', 'zenyattadead', 'hanzodead', 'mercydead', 'orisadead',
          'reinhardtdead', 'symmetradead', 'widowmakerdead', 'winstondead']

filenames = ['ally1', 'ally2', 'ally3', 'ally4', 'ally5', 'ally6',
             'enemy1', 'enemy2', 'enemy3', 'enemy4', 'enemy5', 'enemy6']

allied_team = []
enemy_team = []

h = 0
for h in range(0, len(filenames)):
    unknown = Image.open('output/' + filenames[h] + '.png').load()

    confidences = []
    for i in heroes:
        confidences.append(0)
    #print(confidences)

    x = 0
    y = 0
    j = 0
    for j in range(0, len(heroes)):
        learned_image = Image.open('learned/' + heroes[j] + '.png').load()
        for x in range(0, 75):
            for y in range(0, 75):
                input_color = unknown[x, y]
                input_color = int(re.sub('[^0-9]', '', str(input_color)[1:4]))  # sorry

                learned_color = learned_image[x, y]
                learned_color = int(re.sub('[^0-9]', '', str(learned_color)[1:4]))

                confidences[j] += abs(input_color - learned_color)
        confidences[j] = 1 - (confidences[j] / 1434375)

    likely_name = ''
    likely_num = 0
    i = 0
    for i in range(0, len(confidences)):
        #print(heroes[i] + ': ' + str(confidences[i]))
        if confidences[i] > likely_num:
            likely_num = confidences[i]
            likely_name = heroes[i]

    if 'ally' in filenames[h]:
        allied_team.append(likely_name)
    elif 'enemy' in filenames[h]:
        enemy_team.append(likely_name)

    print('\n')
    print("For " + filenames[h] + ":")

    print("Most likely is " + likely_name + ", with a confidence score of " + str(int(likely_num * 100)) + "%")

    prev_name = likely_name
    likely_name = ''
    likely_num = 0
    i = 0
    for i in range(0, len(confidences)):
        if confidences[i] > likely_num and heroes[i] != prev_name:
            likely_num = confidences[i]
            likely_name = heroes[i]
    print("Second most is " + likely_name + ", with a confidence score of " + str(int(likely_num * 100)) + "%")

print('\n')
print("Allied team: " + str(allied_team))
print("Enemy team: " + str(enemy_team))
