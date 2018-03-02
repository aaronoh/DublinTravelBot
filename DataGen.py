stations = ['malahide', 'portmarnock', 'clongriffin', 'sutton', 'bayside', 'howth junction', 'howth', 'kilbarrack', 'raheny', 'harmonstown', 'killester', 'clontarf road', 'dublin connolly',
            'tara street', 'dublin pearse', 'grand canal dock', 'lansdowne road', 'sandymount', 'sydney parade', 'booterstown', 'blackrock', 'seapoint', 'salthill', 'dun laoghaire',
            'sandycove', 'glenageary', 'dalkey', 'killiney', 'shankill', 'bray', 'greystones', 'kilcoole']

TRAIN_DATA = []

for s in stations:
    x = [
        ("{0} staion north".format(s), {
            'entities': [(0, len(s), 'STATION')]
        }),
        ("Show me {0}".format(s), {
            'entities': [(8, 8 + len(s), 'STATION')]
        }),

        ("Train from {0} south".format(s), {
            'entities': [(11, 11 + len(s), 'STATION')]
        }),

        ("Next train to {0} north".format(s), {
            'entities': [(14, 14 + len(s), 'STATION')]
        }),

        ("Where is {0} south?".format(s), {
            'entities': [(9, 9+len(s), 'STATION')]
        }),
        ("train south from {0}?".format(s), {
            'entities': [(17, 17 + len(s), 'STATION')]
        }),
        ("going north from {0}?".format(s), {
            'entities': [(17, 17 + len(s), 'STATION')]
        }),
        ("train heading north {0}?".format(s), {
            'entities': [(20, 20 + len(s), 'STATION')]
        })
    ]
    TRAIN_DATA = TRAIN_DATA + x

print(TRAIN_DATA)