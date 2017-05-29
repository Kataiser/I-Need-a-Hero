try:
    import openpyxl
except (ImportError, ModuleNotFoundError):
    print("You didn't run setup.bat first! Try again after you do that.")
    raise SystemExit

import namenum_converter as conv

def get_counter(hero1, hero2):
    if hero1 == 'unknown' or hero1 == 'loading':
        return 0
    if hero2 == 'unknown' or hero1 == 'loading':
        return 0

    x = conv.strip_dead(hero1)
    y = conv.strip_dead(hero2)
    posx = hero_reference.index(x) + 2  # because python lists start at 0
    posy = hero_reference.index(y) + 2  # and the counter table starts at 2

    #print(posx)
    #print(posy)

    result = sheet.cell(row=posx, column=posy).value
    if not result:
        result = 0
    return int(result)

wb = openpyxl.load_workbook('counters.xlsx')
sheet = wb.get_sheet_by_name('Sheet1')

hero_reference = []

for i in range(2, 26):
    to_add = sheet.cell(row=i, column=1).value.lower()
    hero_reference.append(to_add)

hero_reference.append('unknown')
hero_reference.append('loading')

#print(hero_reference)

#print(get_counter('hanzo', 'bastion'))
