import logging,requests, xmltodict, json
trainStations = ['malahide', 'portmarnock', 'clongriffin', 'sutton', 'bayside', 'howth junction', 'howth', 'kilbarrack', 'raheny', 'harmonstown', 'killester', 'clontarf road', 'dublin connolly',
            'tara street', 'dublin pearse', 'grand canal dock', 'lansdowne road', 'sandymount', 'sydney parade', 'booterstown', 'blackrock', 'seapoint', 'salthill', 'dun laoghaire',
            'sandycove', 'glenageary', 'dalkey', 'killiney', 'shankill', 'bray', 'greystones', 'kilcoole']

TRAIN_DATA = []

for s in trainStations:
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


bikeStations = ['Smithfield North', 'Parnell Square North', 'Clonmel Street', 'Mount Street Lower', 'Christchurch Place', 'Grantham Street', 'Pearse Street', 'York Street East', 'Excise Walk', 'Fitzwilliam Square West',
                'Portobello Road', 'St. James Hospital (Central)', 'Parnell Street', 'Frederick Street South', 'Fownes Street Upper','Clarendon Row', 'Custom House', 'Hanover Quay', 'Oliver Bond Street',
                'Collins Barracks Museum', 'Brookfield Road', 'Benson Street', 'Earlsfort Terrace', 'Golden Lane', 'Deverell Place', 'John Street West', 'Fenian Street', 'South Dock Road', 'City Quay', 'Exchequer Street',
                'The Point', 'Hatch Street', 'Lime Street','Charlemont Street', 'Kilmainham Gaol', 'Hardwicke Place', 'Wolfe Tone Street', 'Francis Street', 'Greek Street', 'Guild Street', 'Herbert Place', 'High Street',
                'North Circular Road', 'Western Way', 'Talbot Street', 'Newman House', "Sir Patrick's Dun", 'New Central Bank', 'King Street North', 'Herbert Street','Custom House Quay', 'Molesworth Street', 'Georges Quay',
                'Kilmainham Lane', 'Mount Brown', 'Market Street South', 'Kevin Street', 'Eccles Street East', 'Grand Canal Dock', 'Merrion Square East', 'York Street West', "St. Stephen's Green South", 'Denmark Street Great',
                'Royal Hospital', 'Heuston Station (Car Park)',"St. Stephen's Green East", 'Heuston Station (Central)', 'Townsend Street', 'Eccles Street', 'Portobello Harbour', 'Mater Hospital', 'Blessington Street',
                'James Street', 'Merrion Square West', 'Convention Centre', 'Hardwicke Street', 'Parkgate Street', 'Smithfield', 'Dame Street', 'Heuston Bridge (South)', 'Cathal Brugha Street','Sandwith Street', 'Rothe Abbey',
                "Princes Street / O'Connell Street",'Upper Sherrard Street', 'Fitzwilliam Square East','Grattan Street', 'St James Hospital (Luas)', 'Harcourt Terrace', 'Bolton Street', 'Strand Street Great',
                'Jervis Street', 'Ormond Quay Upper', 'Barrow Street', 'Mountjoy Square West','Wilton Terrace', 'Emmet Road', 'Heuston Bridge (North)', 'Leinster Street South', 'Blackhall Place']

# bikeStations = ['Smithfield', 'North', 'Parnell', 'Square', 'North', 'Clonmel', 'Street', 'Mount', 'Street', 'Lower', 'Christchurch', 'Place', 'Grantham', 'Street', 'Pearse', 'Street', 'York','East', 'Excise', 'Walk', 'Fitzwilliam',
#                 'Square', 'West','Portobello', 'Road', 'St.', 'James', 'Hospital', '(Central)','Central', 'Parnell','Frederick','South', 'Fownes','Upper','Clarendon', 'Row', 'Custom', 'House', 'Hanover', 'Quay', 'Oliver', 'Bond',
#                 'Street','Collins', 'Barracks','Museum', 'Brookfield', 'Road', 'Benson','Earlsfort', 'Terrace', 'Golden', 'Lane', 'Deverell', 'Place', 'John','West', 'Fenian', 'South', 'Dock','City','Exchequer',
#                 'The', 'Point', 'Hatch', 'Lime', 'Charlemont','Kilmainham', 'Gaol', 'Hardwicke', 'Place', 'Wolfe', 'Tone', 'Francis','Greek','Guild','Herbert', 'Place', 'High','North', 'Circular', 'Road', 'Western', 'Way',
#                 'Talbot', 'Newman', 'House', 'Sir', "Patrick's", 'Dun', 'New', 'Central', 'Bank', 'King', 'Herbert','Custom','House','Molesworth','Georges','Kilmainham', 'Lane', 'Mount', 'Brown', 'Market', 'South', 'Kevin','Eccles','East',
#                 'Grand','Canal', 'Dock', 'Merrion', 'Square', 'East', 'York', 'West', 'St.', "Stephen's", 'Green','Denmark','Great','Royal', 'Hospital', 'Heuston', 'Station', '(Car Park)', 'car','park','East','Townsend','Eccles','Portobello', 'Harbour',
#                 'Mater', 'Blessington','James', 'Merrion', 'Square', 'Convention', 'Centre', 'Hardwicke', 'Parkgate', 'Smithfield', 'Dame', 'Heuston', 'Bridge', '(South)', 'Cathal', 'Brugha', 'Sandwith', 'Rothe', 'Abbey',
#                 'Princes', "O'Connell", 'Sherrard', 'Fitzwilliam','Grattan', 'James', '(Luas)','Luas', 'Harcourt', 'Bolton', 'Strand','Great','Jervis', 'Ormond',
#                 'Barrow', 'Mountjoy','Wilton', 'Emmet', 'Bridge', '(North)', 'Leinster', 'Blackhall', 'Place']

# bikeStations = ['SmithfieldNorth', 'ParnellSquareNorth', 'ClonmelStreet', 'MountStreetLower', 'ChristchurchPlace', 'GranthamStreet', 'PearseStreet', 'YorkStreetEast', 'ExciseWalk', 'FitzwilliamSquareWest', 'PortobelloRoad',
#                 'St.JamesHospital(Central)', 'ParnellStreet', 'FrederickStreetSouth', 'FownesStreetUpper', 'ClarendonRow', 'CustomHouse', 'HanoverQuay', 'OliverBondStreet', 'CollinsBarracksMuseum', 'BrookfieldRoad',
#                 'BensonStreet', 'EarlsfortTerrace', 'GoldenLane', 'DeverellPlace', 'JohnStreetWest', 'FenianStreet', 'SouthDockRoad', 'CityQuay', 'ExchequerStreet', 'ThePoint', 'HatchStreet', 'LimeStreet', 'CharlemontStreet',
#                 'KilmainhamGaol', 'HardwickePlace', 'WolfeToneStreet', 'FrancisStreet', 'GreekStreet', 'GuildStreet', 'HerbertPlace', 'HighStreet', 'NorthCircularRoad', 'WesternWay', 'TalbotStreet', 'NewmanHouse',
#                 "SirPatrick'sDun", 'NewCentralBank', 'KingStreetNorth', 'HerbertStreet', 'CustomHouseQuay', 'MolesworthStreet', 'GeorgesQuay', 'KilmainhamLane', 'MountBrown', 'MarketStreetSouth', 'KevinStreet',
#                 'EcclesStreetEast', 'GrandCanalDock', 'MerrionSquareEast', 'YorkStreetWest', "St.Stephen'sGreenSouth", 'DenmarkStreetGreat', 'RoyalHospital', 'HeustonStation(CarPark)', "St.Stephen'sGreenEast",
#                 'HeustonStation(Central)', 'TownsendStreet', 'EcclesStreet', 'PortobelloHarbour', 'MaterHospital', 'BlessingtonStreet', 'JamesStreet', 'MerrionSquareWest', 'ConventionCentre', 'HardwickeStreet',
#                 'ParkgateStreet', 'Smithfield', 'DameStreet', 'HeustonBridge(South)', 'CathalBrughaStreet', 'SandwithStreet', 'RotheAbbey', "PrincesStreet/O'ConnellStreet", 'UpperSherrardStreet', 'FitzwilliamSquareEast',
#                 'GrattanStreet', 'StJamesHospital(Luas)', 'HarcourtTerrace', 'BoltonStreet', 'StrandStreetGreat', 'JervisStreet', 'OrmondQuayUpper', 'BarrowStreet', 'MountjoySquareWest', 'WiltonTerrace', 'EmmetRoad',
#                 'HeustonBridge(North)', 'LeinsterStreetSouth', 'BlackhallPlace']


BIKE_DATA = []
for b in bikeStations:
    y = [
        ("Are there any bikes available at the {0} station".format(b), {
            'entities': [(35, 35 + len(b), 'BIKE')]
        }),
        ("Bikes {0}".format(b), {
            'entities': [(6, 6 + len(b), 'BIKE')]
        }),
        ("bike {0}".format(b), {
            'entities': [(5, 5 + len(b), 'BIKE')]
        }),
        ("Any bikes at {0}?".format(b), {
            'entities': [(13, 13 + len(b), 'BIKE')]
        }),
        ("Can I get a bike at {0} station?".format(b), {
            'entities': [(19, 19 + len(b), 'BIKE')]
        }),
        ("Can I get a bike at {0} station?".format(b), {
            'entities': [(19, 19 + len(b), 'BIKE')]
        }),
        ("Free bike at {0}?".format(b), {
            'entities': [(13, 13 + len(b), 'BIKE')]
        }),
        ("Where is {0}?".format(b), {
            'entities': [(9, 9+len(b), 'BIKE')]
        })
    ]
    BIKE_DATA = BIKE_DATA + y


ALLTRAININGDATA = TRAIN_DATA + BIKE_DATA;

print(ALLTRAININGDATA)

# d = []
# for b in bikeStations:
#     b.replace(" ", "")
#     d.append(b.replace(" ", ""))
# print(d)