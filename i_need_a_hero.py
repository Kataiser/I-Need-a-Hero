import loading

from PIL import Image, ImageFilter
import os
import time
import configparser
import ast

from get_counters import get_counter  # naming is hard
import namenum_converter as conv


def format_counter_list(counter_list):
    formatted_counter = ''
    for pair_ in counter_list:
        just_name_ = pair_[0]
        just_num_ = pair_[1]
        full_counter = conv.fancify(just_name_) + ': ' + str(just_num_)
        formatted_counter += (full_counter + ', ')
    return formatted_counter[:-2]  # removes extra comma and space


# defaults
refresh_delay = 0.5
process_allies = True
dev = False

try:
    config = configparser.ConfigParser()  # load some settings
    with open('inah-settings.ini', 'r') as configfile:
        config.read('inah-settings.ini')
        refresh_delay = float(config['MAIN']['refresh_delay'])
        process_allies = ast.literal_eval(config['MAIN']['process_allies'])
        dev = ast.literal_eval(config['MAIN']['dev'])
except FileNotFoundError as error:
    print("Couldn't load inah-settings.ini:", error)
    raise SystemExit


heroes = ['ana', 'bastion', 'dva', 'genji', 'hanzo',
          'junkrat', 'lucio', 'mccree', 'mei', 'mercy',
          'pharah', 'reaper', 'reinhardt', 'roadhog', 'soldier',
          'sombra', 'symmetra', 'torbjorn', 'tracer', 'widowmaker',
          'winston', 'zarya', 'zenyatta', 'unknown', 'loading',
          'anadead', 'bastiondead', 'dvadead', 'genjidead', 'junkratdead',
          'luciodead', 'mccreedead', 'meidead', 'pharahdead', 'reaperdead',
          'roadhogdead', 'soldierdead', 'sombradead', 'torbjorndead', 'tracerdead',
          'zaryadead', 'zenyattadead', 'hanzodead', 'mercydead', 'orisadead',
          'reinhardtdead', 'symmetradead', 'widowmakerdead', 'winstondead', 'orisa',
          'doomfist', 'doomfistdead']

heroes_dps = ['bastion', 'genji', 'hanzo', 'junkrat', 'mccree',
              'mei', 'pharah', 'reaper', 'soldier', 'sombra',
              'symmetra', 'torbjorn', 'tracer', 'widowmaker', 'doomfist']
heroes_tank = ['dva', 'reinhardt', 'roadhog', 'winston', 'zarya', 'orisa']
heroes_heal = ['ana', 'lucio', 'mercy', 'zenyatta']

heroes_normal = []  # a list of heroes, not fancy, without unknown, loading, or dead
for i in heroes:
    hero = conv.strip_dead(i)
    if ('unknown' not in hero) and ('loading' not in hero):
        heroes_normal.append(hero)

if process_allies:
    filenames = ['ally1', 'ally2', 'ally3', 'ally4', 'ally5', 'ally6',
                 'enemy1', 'enemy2', 'enemy3', 'enemy4', 'enemy5', 'enemy6']
else:
    filenames = ['enemy1', 'enemy2', 'enemy3', 'enemy4', 'enemy5', 'enemy6']
if dev:
    print('FYI, developer mode is on.')
    dev_file = 'testing/cropit.jpg'

screenshots_path = os.path.expanduser('~\Documents\Overwatch\ScreenShots\Overwatch')
inputs_before = os.listdir(screenshots_path)  # a list of every file in the screenshots folder

loading.done()

while True:
    time.sleep(refresh_delay)  # to stop high cpu usage while waiting
    continue_ = False
    inputs_after = os.listdir(screenshots_path)
    if len(inputs_after) > len(inputs_before):  # if a file is added
        continue_ = True
    if len(inputs_after) < len(inputs_before):  # if a file is removed
        continue_ = False
        inputs_before = os.listdir(screenshots_path)
    if continue_ or dev:
        # starting analysis

        process_time_start = time.time()

        # defaults
        delete_thresehold = 80
        process_threshold = 70
        refresh_delay = 0.5
        low_precision = False
        process_allies = True
        include_allies_in_counters = True
        highlight_yourself = True
        show_processing_text = False
        old_counter_list = False
        dev = False
        preview = False

        try:
            config = configparser.ConfigParser()  # load all settings
            with open('inah-settings.ini', 'r') as configfile:
                config.read('inah-settings.ini')
                delete_thresehold = int(config['MAIN']['delete_thresehold'])
                process_threshold = int(config['MAIN']['process_threshold'])
                refresh_delay = float(config['MAIN']['refresh_delay'])
                low_precision = ast.literal_eval(config['MAIN']['low_precision'])
                process_allies = ast.literal_eval(config['MAIN']['process_allies'])
                include_allies_in_counters = ast.literal_eval(config['MAIN']['include_allies_in_counters'])
                highlight_yourself = ast.literal_eval(config['MAIN']['highlight_yourself'])
                show_processing_text = ast.literal_eval(config['MAIN']['show_processing_text'])
                old_counter_list = ast.literal_eval(config['MAIN']['old_counter_list'])
                dev = ast.literal_eval(config['MAIN']['dev'])
                preview = ast.literal_eval(config['MAIN']['preview'])
        except FileNotFoundError as error:
            print("Couldn't load inah-settings.ini:", error)
            raise SystemExit

        inputs_diff = list(set(os.listdir(screenshots_path)) - set(inputs_before))
        current_filename = str(inputs_diff)[2:-2]  # removes brackets and quotes
        if dev:
            current_filename = dev_file
        print("\nProcessing " + current_filename + " at " + str(time.strftime('%I:%M:%S %p', time.localtime())))

        if not dev:
            try:
                time.sleep(0.1)  # bug "fix"
                screenshot = Image.open(screenshots_path + '/' + inputs_diff[0])
            except OSError:
                print("This doesn't seem to be an image file.")
                inputs_before = os.listdir(screenshots_path)  # resets screenshot folder list
                continue
        else:
            screenshot = Image.open(dev_file)

        width, height = screenshot.size
        aspect_ratio = width / height
        if aspect_ratio > 2:  # the aspect ratio the user is running at is 21:9
            screenshot = screenshot.resize((2560, 1080))
            screenshot = screenshot.crop((315, 0, 2235, 1080))
        elif aspect_ratio < 1.7:  # aspect ratio is 16:10
            screenshot = screenshot.resize((1920, 1200))
            screenshot = screenshot.crop((0, 60, 1920, 1140))
        else:  # aspect ratio is 16:10
            screenshot = screenshot.resize((1920, 1080))

        if preview:
            screenshot.save('preview.png')
        else:
            try:
                os.remove("preview.png")
            except FileNotFoundError:
                pass

        if low_precision:
            step = 2  # skips every other pixel
            divisor = 64000  # scary magic math
        else:
            step = 1
            divisor = 256000

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

        filenames_opened = []
        if process_allies:
            filenames_opened.append(ally1)
            filenames_opened.append(ally2)
            filenames_opened.append(ally3)
            filenames_opened.append(ally4)
            filenames_opened.append(ally5)
            filenames_opened.append(ally6)
        filenames_opened.append(enemy1)
        filenames_opened.append(enemy2)
        filenames_opened.append(enemy3)
        filenames_opened.append(enemy4)
        filenames_opened.append(enemy5)
        filenames_opened.append(enemy6)

        allied_team = []
        enemy_team = []
        total_confidence = []
        mask = Image.open('mask.png').convert('RGBA')  # used to ignore metal winged BS

        for h in range(0, len(filenames)):  # every ally or enemy
            unknown_unloaded = filenames_opened[h]
            unknown_unloaded = unknown_unloaded.filter(ImageFilter.GaussianBlur(radius=2))
            unknown_unloaded.paste(mask, (0, 0), mask)  # ...until I put on the mask
            unknown = unknown_unloaded.load()

            confidences = []
            for i in heroes:
                confidences.append(0)  # makes a hero-long list of zeroes

            for j in range(0, len(heroes)):  # the image recognition magic
                learned_image = Image.open('learned/' + heroes[j] + '.png').load()  # inefficiency yay
                for x in range(0, 75, step):
                    for y in range(0, 75, step):
                        input_color = unknown[x, y]
                        input_color = input_color[0]

                        learned_color = learned_image[x, y]
                        learned_color = learned_color[0]

                        confidences[j] += abs(input_color - learned_color)
                confidences[j] = 1 - (confidences[j] / divisor)

            if show_processing_text:
                print("For " + filenames[h] + ":")

            likely_name = ''  # find the most likely hero
            likely_num = 0
            for i in range(0, len(confidences)):
                if confidences[i] > likely_num:
                    likely_num = confidences[i]
                    likely_name = heroes[i]
            print_conf = int(likely_num * 100)
            if show_processing_text:
                print("Most likely is " + likely_name
                      + ", with a confidence of " + str(print_conf) + "%")
            total_confidence.append(print_conf)

            if 'ally' in filenames[h]:
                allied_team.append(likely_name)  # builds the team lists
            elif 'enemy' in filenames[h]:
                enemy_team.append(likely_name)

        print('\n')

        process_time_elapsed = time.time() - process_time_start
        print("Processing finished in " + str(process_time_elapsed)[0:3] + " seconds")

        enemy_team_fancy = ''
        for i in enemy_team:
            hero = conv.fancify(i)
            enemy_team_fancy += (hero + ', ')
        if process_allies:
            allied_team_fancy = ''
            for i in allied_team:
                hero = conv.fancify(i)
                allied_team_fancy += (hero + ', ')

        total_conf_average = int(sum(total_confidence) / float(len(total_confidence)))

        if total_conf_average > process_threshold:
            print("Enemy team: " + enemy_team_fancy[:-2])
            print("Allied team: " + allied_team_fancy[:-2])
            print("Confidence: " + str(total_conf_average) + '%')
        else:
            print("This screenshot doesn't seem to be of the tab menu " +
                  "(needs " + str(process_threshold) + "% confidence, got " + str(total_conf_average) + "%)")

        enemy_is_heroes = True
        j = 0
        for i in enemy_team:
            if (i == 'loading') or (i == 'unknown'):
                j += 1
        if j == 6:
            enemy_is_heroes = False  # if everyone on the enemy team is loading or unknown

        if total_conf_average > process_threshold and process_allies and enemy_is_heroes:
            # get overall team counter advantage

            allied_team_counter = 0
            for i in enemy_team:
                for j in allied_team:
                    cross_team_counter = get_counter(i, j)
                    allied_team_counter -= cross_team_counter
            if allied_team_counter < 0:
                print("Your team has an counter advantage of " + str(-allied_team_counter))
            elif allied_team_counter > 0:
                print("The enemy team has an counter advantage of " + str(allied_team_counter))
            elif allied_team_counter == 0:
                print("Neither team has a counter advantage")
            else:
                raise ValueError  # sure why not

        if enemy_is_heroes and (total_conf_average > process_threshold):  # is this valid to get counters from
            # begin getting counters

            all_counters = {}

            for any_hero in heroes_normal:  # actually gets counters
                all_counters[any_hero] = 0
                for enemy_hero in enemy_team:
                    enemy_hero = conv.strip_dead(enemy_hero)
                    if ('unknown' not in any_hero) and ('loading' not in any_hero):
                        countered = get_counter(any_hero, enemy_hero)
                        all_counters[any_hero] -= countered

            sorted_counters = sorted(all_counters.items(), reverse=True, key=lambda z: z[1])  # wtf

            if not old_counter_list:
                dps_counters = []
                tank_counters = []
                heal_counters = []

                for pair in sorted_counters:
                    just_name = pair[0]
                    just_num = pair[1]

                    if just_name not in allied_team or include_allies_in_counters:
                        if just_name in heroes_dps:
                            dps_counters.append(tuple((just_name, just_num)))
                        if just_name in heroes_tank:
                            tank_counters.append(tuple((just_name, just_num)))
                        if just_name in heroes_heal:
                            heal_counters.append(tuple((just_name, just_num)))

                    if just_name == conv.strip_dead(allied_team[0]):
                        yourself = conv.fancify(just_name) + '): ' + str(just_num)

                # no need to sort these, sorted_counters was already sorted (duh)

                final_counters_dps = format_counter_list(dps_counters)
                final_counters_tank = format_counter_list(tank_counters)
                final_counters_heal = format_counter_list(heal_counters)
                print('\n')

                print("Counters (higher is better)")
                print("DPS: " + final_counters_dps)
                print("Tanks: " + final_counters_tank)
                print("Healers: " + final_counters_heal)
            else:
                final_counters = format_counter_list(sorted_counters)
                print('\n')
                print("Counters (higher is better)")
                print(final_counters)

            if highlight_yourself:
                print("You (" + yourself)

            # end getting counters
        elif not enemy_is_heroes:
            print("\nThe enemy team appears to be all loading or unknown, which counters can't be calculated from.")

        print('\n')  # managing these is hard

        if total_conf_average > delete_thresehold and not dev:  # deletes screenshot once done
            os.remove(screenshots_path + '/' + inputs_diff[0])  # doesn't recycle, fyi
            print("Deleted " + current_filename + ' (needed ' + str(delete_thresehold)
                  + '% confidence, got ' + str(total_conf_average) + '%)')
        else:
            print("Didn't delete " + current_filename + ' (needs ' + str(delete_thresehold)
                  + '% confidence, got ' + str(total_conf_average) + '%)')
            if delete_thresehold >= 100:
                print("The delete threshold is currently 100%, which means that even tab menu screenshots aren't"
                      " deleted. Be sure to clean the screenshots folder out manually every now and then.")
        inputs_before = os.listdir(screenshots_path)  # resets screenshot folder list

        if dev:
            raise SystemExit

        print('\n')
        print('Analysis complete. Hold tab and press the "print screen" button to get a new set of counters.')
