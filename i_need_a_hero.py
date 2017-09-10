from resources import loading

import ast
import configparser
import os
import sys
import time

from PIL import Image, ImageFilter
from tqdm import tqdm

from resources import exception_handler
from resources import customlogger as log
from resources import namenum_converter as conv
from resources.get_counters import get_counter, get_synergy  # naming is hard


def format_counter_list(counter_list):
    formatted_counter = ''
    for pair_ in counter_list:
        just_name_ = pair_[0]
        just_num_ = pair_[1]
        full_counter = conv.fancify(just_name_) + ': ' + str(just_num_)
        formatted_counter += (full_counter + ', ')
    return formatted_counter[:-2]  # removes extra comma and space


def does_team_have_categories(team):
    team_alive = []
    for possibly_dead_hero in team:
        team_alive.append(conv.strip_dead(possibly_dead_hero))

    out_string = ""
    if not any(x in team_alive for x in heroes_dps):
        out_string += "[No DPS] "
    if not any(x in team_alive for x in heroes_tank):
        out_string += "[No tanks] "
    if not any(x in team_alive for x in heroes_heal):
        out_string += "[No healers] "
    return out_string


def remove_dead_from_team(team_list):
    alive_list = []
    for hero in team_list:
        hero = conv.strip_dead(hero)
        alive_list.append(hero)
    return alive_list


def compare_teams(new_team, old_team):
    team_diff_list = set(new_team).intersection(old_team)
    team_diff_num = 6 - len(team_diff_list)
    return team_diff_num, list(team_diff_list)


exception_handler.setup_excepthook()
log.info("START")

# defaults
refresh_delay = 0.5
max_logs = 10
dev = False
error_reporting = True

try:
    config = configparser.ConfigParser()  # load some settings
    with open('inah-settings.ini', 'r') as configfile:
        config.read('inah-settings.ini')
        refresh_delay = float(config['MAIN']['refresh_delay'])
        max_logs = float(config['MAIN']['max_logs'])
        dev = ast.literal_eval(config['MAIN']['dev'])
        error_reporting = ast.literal_eval(config['MAIN']['error_reporting'])

        settings_raw = configfile.readlines()
        settings_raw = settings_raw[0:13]
        log.info("Settings: " + str(settings_raw))
except:
    settings_error_prefix = "Couldn't load settings: "
    settings_error = exception_handler.format_caught_exception(sys.exc_info())
    print('{} "{}", reverting to default settings'.format(settings_error_prefix, sys.exc_info()[1]))
    log.error(settings_error_prefix + settings_error)

log.cleanup(max_logs)

exception_handler.sentry_mode(error_reporting)

if dev:
    print('FYI, developer mode is on.')
    exception_handler.sentry_mode(False)
    dev_file = 'testing/harder.jpg'
    log.debug("Developer mode is on, dev_file is " + dev_file)

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

filenames = ['ally1', 'ally2', 'ally3', 'ally4', 'ally5', 'ally6',
             'enemy1', 'enemy2', 'enemy3', 'enemy4', 'enemy5', 'enemy6']
allied_team_previous = []
enemy_team_previous = []

screenshots_path = os.path.expanduser('~\Documents\Overwatch\ScreenShots\Overwatch')
log.info("screenshots_path is " + screenshots_path)
try:
    inputs_before = os.listdir(screenshots_path)  # a list of every file in the screenshots folder
except FileNotFoundError:
    print("Couldn't find the screenshots folder (should be at {})".format(screenshots_path))
    log.critical("Couldn't find screenshots_path: {}".format(
        exception_handler.format_caught_exception(sys.exc_info())))
    raise SystemExit
log.info('The screenshots folder has ' + str(len(inputs_before)) + " images")

# builds a cache of learned images
learned_images = {}
for learned_path in os.listdir('learned'):
    if 'png' in learned_path:
        learned = Image.open('learned/' + learned_path).load()
        pixel_list_x = []
        for x in range(0, 75):
            pixel_list_y = []
            for y in range(0, 75):
                color = learned[x, y][0]
                pixel_list_y.append(color)
            pixel_list_x.append(pixel_list_y)
        learned_images[learned_path[:-4]] = pixel_list_x
log.info("The learned folder has " + str(len(learned_images)) + " images")

mask = Image.open('resources/mask.png').convert('RGBA')  # used to ignore metal winged BS
log.info("Mask opened: " + str(mask))

last_run_time = None

loading_time = loading.done()
log.info("Loaded in " + str(loading_time) + " seconds")

loops_done = 0
while True:
    if not dev:
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
        log.info("START LOOP")
        log.info("Loop number: " + str(loops_done))
        loops_done += 1

        process_time_start = time.perf_counter()

        # defaults
        delete_thresehold = 80
        process_threshold = 70
        refresh_delay = 0.5
        synergy_weight = 0.25
        low_precision = True
        include_allies_in_counters = True
        highlight_yourself = True
        show_processing_text = False
        old_counter_list = False
        dev = False
        error_reporting = True
        preview = False
        preview_scale = 0.25

        try:
            config = configparser.ConfigParser()  # load all settings
            with open('inah-settings.ini', 'r') as configfile:
                config.read('inah-settings.ini')
                delete_thresehold = int(config['MAIN']['delete_thresehold'])
                process_threshold = int(config['MAIN']['process_threshold'])
                refresh_delay = float(config['MAIN']['refresh_delay'])
                synergy_weight = float(config['MAIN']['synergy_weight'])
                low_precision = ast.literal_eval(config['MAIN']['low_precision'])
                include_allies_in_counters = ast.literal_eval(config['MAIN']['include_allies_in_counters'])
                highlight_yourself = ast.literal_eval(config['MAIN']['highlight_yourself'])
                show_processing_text = ast.literal_eval(config['MAIN']['show_processing_text'])
                old_counter_list = ast.literal_eval(config['MAIN']['old_counter_list'])
                dev = ast.literal_eval(config['MAIN']['dev'])
                error_reporting = ast.literal_eval(config['MAIN']['error_reporting'])
                preview = ast.literal_eval(config['MAIN']['preview'])
                preview_scale = float(config['MAIN']['preview_scale'])

                settings_raw = configfile.readlines()
                settings_raw = settings_raw[0:13]
                log.info("Settings: " + str(settings_raw))
        except:
            settings_error_prefix = "Couldn't load settings: "
            settings_error = exception_handler.format_caught_exception(sys.exc_info())
            print('{} "{}", reverting to default settings'.format(settings_error_prefix, sys.exc_info()[1]))
            log.error(settings_error_prefix + settings_error)

        if not dev:
            exception_handler.sentry_mode(error_reporting)

        inputs_diff = list(set(os.listdir(screenshots_path)) - set(inputs_before))
        log.info("inputs_diff is " + str(inputs_diff))
        current_filename = str(inputs_diff)[2:-2]  # removes brackets and quotes
        if dev:
            current_filename = dev_file

        postfix = ""
        if last_run_time:
            postfix = "({} seconds since last run)".format(round(time.perf_counter() - last_run_time))
        print("\nProcessing {} at {} {}".format(current_filename, str(time.strftime('%I:%M:%S %p', time.localtime())),
                                                postfix))
        last_run_time = time.perf_counter()
        log.info("Processing " + current_filename)

        if not dev:
            try:
                time.sleep(0.1)  # bug "fix"
                screenshot = Image.open(screenshots_path + '/' + inputs_diff[0])
                log.info("Screenshot opened successfully: " + str(screenshot))
            except OSError:
                print("This doesn't seem to be an image file.")
                inputs_before = os.listdir(screenshots_path)  # resets screenshot folder list
                log.error("Couldn't open screenshot file: {}".format(
                          exception_handler.format_caught_exception(sys.exc_info())))
                continue
        else:
            screenshot = Image.open(dev_file)
            log.debug("Dev screenshot opened successfully: " + str(screenshot))

        if preview:
            width, height = screenshot.size
            preview_dimensions = (round(width * preview_scale), round(height * preview_scale))
            screenshot.resize(preview_dimensions).save('preview.png')
            log.info("Saved preview {}".format(preview_dimensions))
        else:
            try:
                os.remove("preview.png")
                log.info("Deleted preview")
            except FileNotFoundError:
                log.info("No preview to delete")
                pass

        if not width:
            width, height = screenshot.size
        aspect_ratio = width / height
        log.info("Aspect ratio is {} ({} / {})".format(aspect_ratio, width, height))
        if aspect_ratio > 2:  # the aspect ratio the user is running at is 21:9
            log.info("Formatted aspect ratio is closest to 21:9, processing accordingly")
            if not (width == 2579 and height == 1080):
                screenshot = screenshot.resize((2579, 1080), resample=Image.BICUBIC)
            screenshot = screenshot.crop((329, 0, 2249, 1080))
        elif aspect_ratio < 1.7:  # aspect ratio is 16:10
            log.info("Formatted aspect ratio is closest to 16:10, processing accordingly")
            if not (width == 1920 and height == 1200):
                screenshot = screenshot.resize((1920, 1200), resample=Image.BICUBIC)
            screenshot = screenshot.crop((0, 60, 1920, 1140))
        else:  # aspect ratio is 16:9
            log.info("Formatted aspect ratio is closest to 16:9, processing accordingly")
            if not (width == 1920 and height == 1080):
                screenshot = screenshot.resize((1920, 1080), resample=Image.BICUBIC)

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
        filenames_opened.extend((ally1, ally2, ally3, ally4, ally5, ally6,
                                 enemy1, enemy2, enemy3, enemy4, enemy5, enemy6))

        allied_team = []
        enemy_team = []
        total_confidence = []
        team_confidences = []

        log.info("Starting image recognition")
        for h in tqdm(range(0, len(filenames)), file=sys.stdout, ncols=40, bar_format='{l_bar}{bar}|'):
            # loads an portrait to process
            unknown_unloaded = filenames_opened[h]
            unknown_unloaded = unknown_unloaded.filter(ImageFilter.GaussianBlur(radius=1))
            unknown_unloaded.paste(mask, (0, 0), mask)  # ...until I put on the mask
            unknown = unknown_unloaded.load()
            pixel_list_x = []
            for x in range(0, 75):
                pixel_list_y = []
                for y in range(0, 75):
                    color = unknown[x, y][0]
                    pixel_list_y.append(color)
                pixel_list_x.append(pixel_list_y)

            confidences = []
            for i in heroes:
                confidences.append(0)  # makes a hero-long list of zeroes

            for j in range(0, len(heroes)):  # the image recognition magic
                learned_image = learned_images[heroes[j]]
                for x in range(0, 75, step):
                    for y in range(0, 75, step):
                        input_color = pixel_list_x[x][y]

                        learned_color = learned_image[x][y]

                        confidences[j] += abs(input_color - learned_color)
                confidences[j] = 1 - (confidences[j] / divisor)

            if show_processing_text:
                print("For " + filenames[h] + ":")

            likely_name = ''  # find the most likely hero
            likely_num = -1
            for i in range(0, len(confidences)):
                if confidences[i] > likely_num:
                    likely_num = confidences[i]
                    likely_name = heroes[i]
            print_conf = int(likely_num * 100)
            if print_conf < 0:
                print_conf = 0
            if show_processing_text:
                print("Most likely is " + likely_name
                      + ", with a confidence of " + str(print_conf) + "%")
            total_confidence.append(print_conf)

            if 'ally' in filenames[h]:
                allied_team.append(likely_name)  # builds the team lists
            elif 'enemy' in filenames[h]:
                enemy_team.append(likely_name)

        print('\n')

        process_time_elapsed = time.perf_counter() - process_time_start
        print("Processing finished in " + str(process_time_elapsed)[0:3] + " seconds")
        log.info("Image recognition finished in " + str(process_time_elapsed) + " seconds")
        log.info("Enemy team is " + str(enemy_team))
        log.info("Allied team is " + str(allied_team))
        log.info("Confidences (allied first): " + str(total_confidence))

        enemy_team_fancy = ''
        for i in enemy_team:
            hero = conv.fancify(i)
            enemy_team_fancy += (hero + ', ')
        allied_team_fancy = ''
        for i in allied_team:
            hero = conv.fancify(i)
            allied_team_fancy += (hero + ', ')

        total_conf_average = int(sum(total_confidence) / float(len(total_confidence)))
        log.info("Image recognition had a confidence of " + str(total_conf_average))

        if total_conf_average > process_threshold:
            print("Confidence: " + str(total_conf_average) + '%')

            missing_categories_enemy = does_team_have_categories(enemy_team)
            log.info("Missing categories (enemy): {}".format(missing_categories_enemy))
            print("Enemy team: {}".format(enemy_team_fancy[:-2]))
            diff_from_previous_enemy = (0, [])
            if enemy_team_previous:
                diff_from_previous_enemy = compare_teams(remove_dead_from_team(enemy_team), enemy_team_previous)
            print("({} changed from previous analysis) {}"
                  .format(diff_from_previous_enemy[0], missing_categories_enemy))
            log.info("Diff from previous run (enemy): {}".format(diff_from_previous_enemy))

            missing_categories_allied = does_team_have_categories(allied_team)
            log.info("Missing categories (allied): {}".format(missing_categories_allied))
            print("Allied team: {}".format(allied_team_fancy[:-2]))
            diff_from_previous_allied = (0, [])
            if allied_team_previous:
                diff_from_previous_allied = compare_teams(remove_dead_from_team(allied_team), allied_team_previous)
            print("({} changed from previous analysis) {}"
                  .format(diff_from_previous_allied[0], missing_categories_allied))
            log.info("Diff from previous run (allied): {}".format(diff_from_previous_allied))
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
            log.info("The enemy team IS loading or unknown")
        else:
            log.info("The enemy team is NOT loading or unknown")

        if enemy_is_heroes:
            allied_team_previous = remove_dead_from_team(allied_team)
            enemy_team_previous = remove_dead_from_team(enemy_team)

        if total_conf_average > process_threshold and enemy_is_heroes:
            # get overall team counter advantage
            allied_team_synergy = 0
            for ally_hero1 in allied_team:
                for ally_hero2 in allied_team:
                    ally_hero1 = conv.strip_dead(ally_hero1)
                    ally_hero2 = conv.strip_dead(ally_hero2)
                    synergy = get_synergy(ally_hero1, ally_hero2, True)
                    allied_team_synergy += synergy
                            
            enemy_team_synergy = 0
            for enemy_hero1 in enemy_team:
                for enemy_hero2 in enemy_team:
                    enemy_hero1 = conv.strip_dead(enemy_hero1)
                    enemy_hero2 = conv.strip_dead(enemy_hero2)
                    synergy = get_synergy(enemy_hero1, enemy_hero2, True)
                    enemy_team_synergy += synergy

            allied_team_counter = 0
            for i in enemy_team:
                for j in allied_team:
                    cross_team_counter = get_counter(i, j)
                    allied_team_counter += cross_team_counter

            team_synergy_diff = (allied_team_synergy - enemy_team_synergy) * synergy_weight
            log.info("Team counter/synergy advantage is {}/{}".format(allied_team_counter, team_synergy_diff))
            
            if allied_team_counter > 1:
                print("Your team has an counter advantage of {}".format(round(allied_team_counter)))
            elif allied_team_counter < -1:
                print("The enemy team has an counter advantage of {}".format(-round(allied_team_counter)))
            else:
                print("Neither team has a counter advantage")
            if team_synergy_diff > 1:
                print("Your team has an synergy advantage of {}".format(round(team_synergy_diff)))
            elif team_synergy_diff < -1:
                print("The enemy team has an synergy advantage of {}".format(-round(team_synergy_diff)))
            else:
                print("Neither team has a synergy advantage")

        if enemy_is_heroes and (total_conf_average > process_threshold):  # is this valid to get counters from
            # begin getting counters
            log.info("Getting counters")

            all_counters = {}

            for any_hero in heroes_normal:  # actually gets counters
                all_counters[any_hero] = 0
                for enemy_hero in enemy_team:
                    enemy_hero = conv.strip_dead(enemy_hero)
                    if ('unknown' not in any_hero) and ('loading' not in any_hero):
                        countered = get_counter(any_hero, enemy_hero)
                        all_counters[any_hero] += countered
                for ally_hero in allied_team:
                    ally_hero = conv.strip_dead(ally_hero)
                    if ('unknown' not in any_hero) and ('loading' not in any_hero):
                        synergy = get_synergy(any_hero, ally_hero, False)
                        all_counters[any_hero] -= synergy * synergy_weight

            sorted_counters = sorted(all_counters.items(), reverse=True, key=lambda z: z[1])  # wtf
            log.info("Got " + str(len(sorted_counters)) + " counters")

            if not old_counter_list:
                dps_counters = []
                tank_counters = []
                heal_counters = []
                for pair in sorted_counters:
                    just_name = pair[0]
                    just_num = round(pair[1])

                    if just_name not in allied_team or include_allies_in_counters:
                        if just_name in heroes_dps:
                            dps_counters.append(tuple((just_name, just_num)))
                        if just_name in heroes_tank:
                            tank_counters.append(tuple((just_name, just_num)))
                        if just_name in heroes_heal:
                            heal_counters.append(tuple((just_name, just_num)))

                    if just_name == conv.strip_dead(allied_team[0]):
                        yourself = 'You (' + conv.fancify(just_name) + '): ' + str(just_num)

                # no need to sort these, sorted_counters was already sorted (duh)

                final_counters_dps = format_counter_list(dps_counters)
                final_counters_tank = format_counter_list(tank_counters)
                final_counters_heal = format_counter_list(heal_counters)
                print('\n')

                print("Results (higher is better)")
                print("DPS - " + final_counters_dps)
                print("Tanks - " + final_counters_tank)
                print("Healers - " + final_counters_heal)
            else:
                final_counters = format_counter_list(sorted_counters)
                print('\n')
                print("Results (higher is better)")
                print(final_counters)

            if highlight_yourself:
                print(yourself)
                log.info("Yourself: '" + yourself + "'")

            # end getting counters
        elif not enemy_is_heroes:
            print("\nThe enemy team appears to be all loading or unknown, which counters can't be calculated from.")

        print('\n')  # managing these is hard

        if total_conf_average > delete_thresehold and not dev:  # deletes screenshot once done
            os.remove(screenshots_path + '/' + inputs_diff[0])  # doesn't recycle, fyi
            print("Deleted " + current_filename + ' (needed ' + str(delete_thresehold)
                  + '% confidence, got ' + str(total_conf_average) + '%)')
            log.info("Deleted screenshot")
        else:
            print("Didn't delete " + current_filename + ' (needs ' + str(delete_thresehold)
                  + '% confidence, got ' + str(total_conf_average) + '%)')
            log.info("Didn't delete screenshot")
            if delete_thresehold >= 100:
                print("The delete threshold is currently 100%, which means that even tab menu screenshots aren't"
                      " deleted. Be sure to clean the screenshots folder out manually every now and then.")
        inputs_before = os.listdir(screenshots_path)  # resets screenshot folder list

        log.info("END LOOP")

        if dev:
            log.debug("Dev mode is on and a full loop has been completed, exiting")
            raise SystemExit

        print('\n')
        print('Analysis complete. Hold tab and press the "print screen" button to get a new set of counters.')
