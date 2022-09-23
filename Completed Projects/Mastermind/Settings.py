"""
    Daniel Gonzalez
    Mastermind: Settings
"""

DEF_COLORS = ["red", "green", "blue", "purple", "yellow",
              "orange", "pink", "dark green", "cyan", "dark violet"]

BLIND_COLORS = ["midnight blue", "dark green", "light sea green",
                "light sky blue", "khaki", "pale violet red",
                "medium orchid", "maroon", "lime", "lemon chiffon"]

DEF_CONFIG = '''### DISPLAY SETTINGS ###
# Change for more personalized and accessible gameplay #
restore_default=false
colorblind=false
darkmode=false
screensize=0

### GAMEPLAY SETTINGS ###
# Change for easier/harder gameplay and bonus points #
difficulty=3
pegs=4
colors=6
repeats=false

### LEADERBOARD SETTINGS ###
# Change to affect scoring calculations and storage #
bonus_enabled=true
load_xml=false
export_xml=true'''

DEF_SETTINGS = {'restore_default': 'false', 'colorblind': 'false', 'darkmode': 'false', 'screensize': '0',
                'difficulty': '3', 'pegs': '4', 'colors': '6', 'repeats': 'false',
                'bonus_enabled': 'true', 'load_xml': 'false', 'export_xml': 'true'}


class Settings(object):

    """Settings is a singleton that all classes draw from. This is to prevent
    passing too many variables from one class to another, and avoiding situations
    where classes may mess with each other's attributes. Containing it in one place
    makes it simple and easy to follow.
    Reads settings from a config file. All objects should call get_setting() rather than
    directly accessing the final_settings variable below."""

    final_settings = {}  # The one and only source for all settings of the game

    def __new__(cls):
        """Singleton design pattern"""
        if (not hasattr(cls, 'instance')):
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """Constructor method, checks if final_settings has appropriate settings,
        generates new settings if not."""
        if len(Settings.final_settings) < 11:
            self.validate_settings(self.read_settings())

    def get_setting(self, setting):
        """get_setting() returns the setting value the caller is looking for. Returns None
        if it does not exist. Used as a way to keep other classes from meddling with the settings"""

        # Checks it exists, and returns a COPY if it's a list to avoid editing the actual values
        # Not a deepcopy, however.
        option = None
        if (setting in Settings.final_settings):
            option = Settings.final_settings[setting]
            if (isinstance(option, list)):
                option = Settings.final_settings[setting].copy()

        return option

    def read_settings(self, file_name="settings.cfg"):
        """read_settings() reads the settings from the config file
        and returns a dictionary of strings representing each setting."""

        settings = DEF_SETTINGS.copy()
        valid = True

        try:
            with open(file_name, mode='r') as infile:
                for line in infile:
                    if line[0] == '#' or len(line) == 1:
                        continue

                    # Some kind of gibberish, ignore it
                    setting = line.lower().split(sep='=')
                    if (len(setting) != 2):
                        valid = False
                        continue

                    setting[0] = setting[0].strip()
                    setting[1] = setting[1].strip()

                    # Make sure it exists, otherwise ignore it
                    if (setting[0] in settings):
                        settings[setting[0]] = setting[1]
                    else:
                        valid = False
                        continue


        except:
            print("Unable to read config file.")
            self.restore_default()

        # Config file wasn't valid, restore it
        if not valid:
            self.restore_default()

        return settings

    def restore_default(self):
        """restore_default() overwrites the config file with the default values"""
        try:
            with open('settings.cfg', mode='w') as settings:
                settings.write(DEF_CONFIG)
        except:
            print("Unable to restore config file.")

    def validate_settings(self, settings):
        """validate_settings() validates a dictionary of settings read
        from a config file. Converts strings to actual values (bool, int, etc)
        settings - dictionary needed to validate"""

        ### DISPLAY SETTINGS ###
        if (settings['restore_default'] == 'true'):
            self.restore_default()
            settings = DEF_SETTINGS.copy()


        if (settings['darkmode'] == 'true'):
            Settings.final_settings['linecolor'] = 'white'
            Settings.final_settings['bullcolor'] = 'white'
            Settings.final_settings['fillcolor'] = 'black'
        else:
            Settings.final_settings['linecolor'] = 'black'
            Settings.final_settings['bullcolor'] = 'black'
            Settings.final_settings['fillcolor'] = 'white'

        if (settings['screensize'].isnumeric()):
            size = int(settings['screensize'])
            if (size >= 9):
                settings['screensize'] = '9'
            elif (size <= 0):
                settings['screensize'] = '0'
        else:
            settings['screensize'] = '0'

        Settings.final_settings['screensize'] = float('1.' + settings['screensize'])

        ### GAMEPLAY SETTINGS ###
        difficulty = 3
        if (settings['difficulty'].isnumeric()):
            difficulty = int(settings['difficulty'])
            if (difficulty >= 5):
                difficulty = 5
            elif (difficulty <= 1):
                difficulty = 1
        Settings.final_settings['rounds'] = 18 - (2 * difficulty)

        pegs = 4
        if (settings['pegs'].isnumeric()):
            pegs = int(settings['pegs'])
            if (pegs <= 4):
                pegs = 4
            elif (pegs >= 8):
                pegs = 8
        Settings.final_settings['pegs'] = pegs

        colors = 6
        if (settings['colors'].isnumeric()):
            colors = int(settings['colors'])
            if (colors <= 6):
                colors = 6
            elif (colors >= 10):
                colors = 10

        if (settings['repeats'] == 'true'):
            Settings.final_settings['repeats'] = True
        else:
            Settings.final_settings['repeats'] = False

        # You either need repeats, more colors, or fewer pegs. I chose more colors
        if (colors < pegs and not Settings.final_settings['repeats']):
            colors = pegs

        if (settings['colorblind'] == 'true'):
            Settings.final_settings['colors'] = BLIND_COLORS[0:colors]
        else:
            Settings.final_settings['colors'] = DEF_COLORS[0:colors]

        ### LEADERBOARD SETTINGS ###

        if (settings['bonus_enabled'] == 'true'):
            Settings.final_settings['bonus_enabled'] = True
        else:
            Settings.final_settings['bonus_enabled'] = False

        bonus = 0
        bonus += colors - 6
        bonus += pegs - 4
        if (Settings.final_settings['repeats']):
            bonus += 2
        bonus *= 2

        Settings.final_settings['bonus_points'] = bonus

        if (settings['load_xml'] == 'true'):
            Settings.final_settings['load_xml'] = True
        else:
            Settings.final_settings['load_xml'] = False

        if (settings['export_xml'] == 'true'):
            Settings.final_settings['export_xml'] = True
        else:
            Settings.final_settings['export_xml'] = False
