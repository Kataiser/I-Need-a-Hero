def name_to_num(name):
    return table_long[name]


def num_to_name(num):
    return table_reversed[num]


def fancify(name):
    fancy = table_reversed[table_long[name]]  # inefficiency yay
    if not fancy:  # lol
        fancy = name
    return fancy


def strip_dead(name):
    if 'dead' in name:
        name = name[:-4]
    return name

table_long = {'unknown': -1, 'loading': -1, 'ana': 0, 'bastion': 1, 'dva': 2,
              'genji': 3, 'hanzo': 4, 'junkrat': 5, 'lucio': 6, 'mccree': 7,
              'mei': 8, 'mercy': 9, 'pharah': 10, 'reaper': 11, 'reinhardt': 12,
              'roadhog': 13, 'soldier': 14, 'sombra': 15, 'symmetra': 16, 'torbjorn': 17,
              'tracer': 18, 'widowmaker': 19, 'winston': 20, 'zarya': 21, 'zenyatta': 22,
              'anadead': 0, 'bastiondead': 1, 'dvadead': 2, 'genjidead': 3, 'junkratdead': 4,
              'luciodead': 6, 'mccreedead': 7, 'meidead': 8, 'pharahdead': 10, 'reaperdead': 11,
              'roadhogdead': 13, 'soldierdead': 14, 'sombradead': 15, 'torbjorndead': 17, 'tracerdead': 18,
              'zaryadead': 21, 'zenyattadead': 22, 'hanzodead': 4, 'mercydead': 9, 'orisadead': 23,
              'reinhardtdead': 12, 'symmetradead': 16, 'widowmakerdead': 19, 'winstondead': 20, 'orisa': 23,
              '': -1}

table_short = {'Ana': 0, 'Bastion': 1, 'D.Va': 2, 'Genji': 3, 'Hanzo': 4,
               'Junkrat': 5, 'Lucio': 6, 'McCree': 7, 'Mei': 8, 'Mercy': 9,
               'Pharah': 10, 'Reaper': 11, 'Reinhardt': 12, 'Roadhog': 13, 'Soldier 76': 14,
               'Sombra': 15, 'Symmetra': 16, 'Torbjorn': 17, 'Tracer': 18, 'Widowmaker': 19,
               'Winston': 20, 'Zarya': 21, 'Zenyatta': 22, 'Orisa': 23, '': -1}

table_reversed = {v: k for k, v in table_short.items()}  # again, wtf
