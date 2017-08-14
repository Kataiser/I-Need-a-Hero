from PIL import Image
import os
import random as r
import time

files = os.listdir('bulk-input')
print(files)

r.seed(time.time())

i = 0
for i in range(0, len(files)):
    img = Image.open('bulk-input/' + files[i]).resize((1920, 1080))

    ally1 = img.crop((443, 584, 519, 660))
    ally2 = img.crop((634, 584, 710, 660))
    ally3 = img.crop((826, 584, 902, 660))
    ally4 = img.crop((1019, 584, 1095, 660))
    ally5 = img.crop((1210, 584, 1286, 660))
    ally6 = img.crop((1402, 584, 1478, 660))
    enemy1 = img.crop((443, 279, 519, 355))
    enemy2 = img.crop((634, 279, 710, 355))
    enemy3 = img.crop((826, 279, 902, 355))
    enemy4 = img.crop((1019, 279, 1095, 355))
    enemy5 = img.crop((1210, 279, 1286, 355))
    enemy6 = img.crop((1402, 279, 1478, 355))

    ally1.save('bulk-output/' + files[i][11:-4] + str(r.randrange(100000)) + '.png')
    ally2.save('bulk-output/' + files[i][11:-4] + str(r.randrange(100000)) + '.png')
    ally3.save('bulk-output/' + files[i][11:-4] + str(r.randrange(100000)) + '.png')
    ally4.save('bulk-output/' + files[i][11:-4] + str(r.randrange(100000)) + '.png')
    ally5.save('bulk-output/' + files[i][11:-4] + str(r.randrange(100000)) + '.png')
    ally6.save('bulk-output/' + files[i][11:-4] + str(r.randrange(100000)) + '.png')
    enemy1.save('bulk-output/' + files[i][11:-4] + str(r.randrange(100000)) + '.png')
    enemy2.save('bulk-output/' + files[i][11:-4] + str(r.randrange(100000)) + '.png')
    enemy3.save('bulk-output/' + files[i][11:-4] + str(r.randrange(100000)) + '.png')
    enemy4.save('bulk-output/' + files[i][11:-4] + str(r.randrange(100000)) + '.png')
    enemy5.save('bulk-output/' + files[i][11:-4] + str(r.randrange(100000)) + '.png')
    enemy6.save('bulk-output/' + files[i][11:-4] + str(r.randrange(100000)) + '.png')

    print(files[i] + " done")
