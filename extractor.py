from PIL import Image
import os

img = Image.open('input/ScreenShot_17-05-16_18-28-51-000.jpg').resize((1920, 1080))

print(os.listdir('input'))

print("Image loaded")

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
print("All cropped")

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
print("All saved")