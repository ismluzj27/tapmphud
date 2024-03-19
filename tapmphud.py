# tapmphud.py
# "ta-pum-fud"

syllabus = {
    '7 Cities': { # unit
        '1 Orig Dist Sys Cities': { # topic
            'vocab': {
                'Urbanization': {
                    'definition': 'the process of developing towns and cities',
                    'notes': '',
                },
                'Site': {
                    'definition': 'physical characteristics of a place',
                    'notes': "includes:\n"+
                        " - climate\n"+
                        " - natural features, especially water"
                },
                'Situation': {
                    'definition': 'location of a place relative to surroundings',
                    'notes': "includes:\n"
                        " - proximity to natural resources\n" +
                        " - proximity to other cities\n" +
                        " - accessibility"
                }
            },
            'notes': [ # group relevant information together
                "Two main factors influence location of cities: site and situation",
                    "Site and situation can also impact how cities function and grow\n"+
                    " - Size of cities\n"+
                    "   * Εxample: Manila has trouble growing because of physical constraints\n"+
                    " - Economic development\n"+
                    "   * Example: Singapore got very wealthy due to strategic position on shipping routes\n"+
                    " - Political/military history\n"+
                    "   * Example: Istanbul as a shatterbelt",
                "Key trend around the world -- cities are getting larger\n"+
                    "Causes\n"+
                    " 1) Population growth\n"+
                    "   * People need somewhere to live\n"+
                    " 2) Improvements in transport and communication\n"+
                    "   * Allows cities to expand -- just look at Manila",
            ]
        }
    }
}

# print(syllabus['7 Cities']['1 Orig Dist Sys Cities']['notes'][1])

def main():
    print("Welcome to the TAPMPHUD Syllabus Manager")


if __name__ == '__main__':
    main()

