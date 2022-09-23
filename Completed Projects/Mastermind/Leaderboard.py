"""
    Daniel Gonzalez
    Mastermind: Leaderboard
"""

from Quad import *
from Settings import Settings
from re import sub
import xml.etree.ElementTree as xtree
import sqlite3


class Leaderboard(Quad):

    """Leaderboard is a quad that displays the top ten scores
    from a SQL database. Handles loading, saving, and exporting scores.
    Can also import scores from an external XML file."""

    def __init__(self, x, y, height, width, pen=None):
        """Constructor method, loads scores from database, resets
            database if taken from XML
            x, y - (x,y) coordinates for center of quad
            height (int/float) - heigh of the quad
            width (int/float) - width of the quad
            pen - turtle object used for drawing/writing"""

        Quad.__init__(self, x, y, height, width, pen)
        self.best_pen = self.new_pen()  # Used to write the best score, and nothing else
        self.personal_best = 0  # Best score this iteration of the game
        self.scores = []
        if Settings().get_setting('load_xml'):
            self.load_xml()
        self.scores = self.load_sql()

    def draw(self):
        """draw() draws the quad of the leaderboard,
        then writes the data the leaderboard stored on the screen inside it"""

        # Leaderboard design:
        #
        #               LEADERBOARD
        # Difficulty: Normal    Personal Best: 0
        # ---------------------------------------
        #          Name             Score
        #          ...               ...

        # LEADERBOARD
        self.pen.width(4)
        Quad.draw(self)
        self.move_pen_to(self.x, self.y + self.height / 2.75)
        self.pen.write("LEADERBOARD", move=False, align='CENTER',
                       font=('Comic Sans MS', int(turtle.screensize()[1] / 24), 'bold'))

        # Difficulty: Normal
        self.move_pen_to(self.x - self.width / 2.15, self.y + self.height / 3.25)
        diff = "Difficulty: " + self.get_difficulty()
        self.pen.write(diff, move=False, align='LEFT',
                       font=('Comic Sans MS', int(turtle.screensize()[1] / 44), 'bold'))
        self.move_pen_to(self.x + self.width / 2.15, self.y + self.height / 3.25)

        # Personal Best: 0
        self.display_best()

        # ---------------------------
        #   Name            Score
        self.move_pen_to(self.x + self.width / 2, self.y + self.height / 3.5)
        self.pen.pendown()
        self.pen.goto(self.x - self.width / 2, self.y + self.height / 3.5)
        self.write_scores()

    def load_sql(self):
        """load_sql() loads the top ten scores for the given difficulty
            from the sql database and returns them as a list of tuples (name, score)."""

        curs = self.init_sql()
        if not curs is None:
            select_scores = '''SELECT players.name AS name, total_score - {bonus} AS score
            FROM scores
            INNER JOIN players
            ON players.playerid = scores.playerid
            WHERE scores.difficulty = {difficulty}
            ORDER BY score DESC
            LIMIT 10'''

            # Format string with values from Settings
            rounds = Settings().get_setting('rounds')
            bonus_points = 0
            scores = []
            if not Settings().get_setting('bonus_enabled'):
                bonus_points = 'bonus_points'

            try:
                top_ten = curs.execute(select_scores.format(bonus=bonus_points, difficulty=rounds))
                scores = top_ten.fetchall()
            except:
                print("Unable to load scores from SQL database.")

            self.close_sql(curs)
            return scores

    def get_difficulty(self):
        """get_difficulty() takes an integer and returns a string
            for the difficulty."""
        difficulty = Settings().get_setting('rounds')
        if (isinstance(difficulty, int)):
            if (difficulty < 10):
                difficulty = 'Master'
            elif (difficulty >= 10 and difficulty < 12):
                difficulty = 'Hard'
            elif (difficulty >= 12 and difficulty < 14):
                difficulty = 'Normal'
            elif (difficulty >= 14 and difficulty < 16):
                difficulty = 'Easy'
            elif (difficulty >= 16):
                difficulty = 'Beginner'
        else:
            difficulty = 'Custom'
        return difficulty

    def set_best(self, score):
        """Sets the personal best value to the new score value
            score (int) - new personal best"""
        if score >= self.personal_best:
            self.personal_best = score

    def display_best(self):
        """Rewrites the personal best at the top of the leaderboard"""
        self.best_pen.clear()
        self.best_pen.penup()
        self.best_pen.goto(self.x + self.width / 2.15, self.y + self.height / 3.25)
        self.best_pen.write('Personal Best: ' + str(self.personal_best), move=False, align='RIGHT',
                            font=('Comic Sans MS', int(turtle.screensize()[1] / 44), 'bold'))

    def write_scores(self):
        """write_scores() writes the top ten scores on the leaderboard"""

        if len(self.scores) > 0:

            # Start at the top, under the header, iterate down
            y_start = self.y + self.height / 5
            y_space = self.height - self.height / 3.5
            y_offset = y_space / 10
            # Left for name, right for score
            left_x = self.x - self.width / 3
            right_x = self.x + self.width / 3

            for i in range(len(self.scores)):
                y = y_start - (y_offset * i)
                self.move_pen_to(left_x, y)
                self.pen.write(self.scores[i][0], move=False, align='LEFT',
                               font=('Comic Sans MS', int(turtle.screensize()[1] / 44), 'bold'))
                self.move_pen_to(right_x, y)
                self.pen.write(self.scores[i][1], move=False, align='RIGHT',
                               font=('Comic Sans MS', int(turtle.screensize()[1] / 44), 'bold'))

        # No scores in the list
        else:
            self.move_pen_to(self.x, self.y)
            self.pen.write("NO SCORES TO DISPLAY", move=False, align='CENTER',
                           font=('Comic Sans MS', int(turtle.screensize()[1] / 44), 'bold'))

    def init_sql(self):
        """
        init_sql() opens a connection to the database and returns a cursor for it.
        Returns None if connection failed.
        """
        curs = None
        try:
            leaderboard_db = sqlite3.connect('leaderboard.db')
            curs = leaderboard_db.cursor()

            # Make sure these tables exist!
            curs.execute('''CREATE TABLE IF NOT EXISTS
                            players(playerid INTEGER PRIMARY KEY AUTOINCREMENT,
                            name VARCHAR(16) NOT NULL,
                            session DATE NOT NULL,
                            UNIQUE(name, session));''')
            curs.execute('''CREATE TABLE IF NOT EXISTS
                            difficulty(rounds INT NOT NULL,
                            name VARCHAR(16) NOT NULL,
                            PRIMARY KEY(rounds)
                            UNIQUE(name));''')
            # Difficulty is a lookup table, needs specified values
            curs.execute('''INSERT OR IGNORE INTO difficulty(rounds, name) 
                            VALUES  (8, 'Master'),
                                    (10, 'Hard'),
                                    (12, 'Normal'),
                                    (14, 'Easy'),
                                    (16, 'Beginner');''')
            curs.execute('''CREATE TABLE IF NOT EXISTS
                            scores(playerid INT NOT NULL,
                            difficulty INT NOT NULL,
                            total_score INT NOT NULL,
                            bonus_points INT NOT NULL,
                            PRIMARY KEY(playerid),
                            FOREIGN KEY (playerid) REFERENCES players(playerid),
                            FOREIGN KEY (difficulty) REFERENCES difficulty(rounds));''')
            leaderboard_db.commit()
        except:
            print("Unable to initialize SQL database")

        return curs

    def close_sql(self, curs):
        """close_sql() handles closing the connection to the database as well as the cursor associated with it.
        curs - cursor object to a database."""
        if (curs is not None):
            connection = curs.connection
            curs.close()
            connection.close()

    def save_score(self, name):
        """save_score() saves the player's score in the database, along with the given name.
            Returns True if successful, False otherwise."""
        success = False
        curs = self.init_sql()
        if curs is not None:
            # Inset into players table before scores table to keep reference constraints
            add_player = "INSERT INTO players(playerid, name, session) " \
                         "VALUES ({playerid}, '{name}', datetime('now'))"

            save_score = "INSERT INTO scores(playerid, difficulty, total_score, bonus_points) " \
                         "VALUES ({playerid}, {difficulty}, {total_score}, {bonus_points})"

            bonus_points = Settings().get_setting('bonus_points')
            total_score = self.personal_best
            # Even if the player did not want bonus_points displayed, they are still saved for the future
            if (not Settings().get_setting('bonus_enabled')):
                total_score += bonus_points
            difficulty = Settings().get_setting('rounds')

            # Make sure name has no ridiculous characters to mess with our database!
            name = ''.join(filter(str.isalnum, name))
            if (len(name) < 1):
                return success

            try:
                # Attempt to execute statements and save!
                playerid = curs.execute("SELECT MAX(playerid) FROM players").fetchone()[0]
                if (playerid is None):
                    playerid = 0
                else:
                    playerid += 1
                curs.execute(add_player.format(playerid=playerid, name=name))
                curs.execute(save_score.format(playerid=playerid, difficulty=difficulty,
                                               total_score=total_score, bonus_points=bonus_points))
                curs.connection.commit()
            except:
                print("Unable to save scores!")

            self.close_sql(curs)
            success = True

        return success

    def load_xml(self, file='leaderboard.xml'):
        """load_xml() loads scores from an XML file, erases the SQL database,
        then inputs the scores into the SQL database."""

        # If data is corrupt or non-existent, ignore it. This does not bother
        # trying to figure out what a user meant by a score like "eighty-two"

        diff = {'Master': 8, 'Hard': 10,
                'Normal': 12, 'Easy': 14,
                'Beginner': 16}

        tree = None
        curs = self.init_sql()

        #Delete database, get XML tree
        try:
            tree = xtree.parse(file)
            curs.execute('DELETE FROM scores;')
            curs.execute('DELETE FROM players;')
            curs.connection.commit()
        except:
            print("Unable to load from XML file and save in database.")
            return

        playerid = 0
        if tree is not None:
            root = tree.getroot()
            ####### GET DIFFICULTY #######
            gamemodes = root.findall('./GameMode')
            for mode in gamemodes:
                if ('Difficulty' not in mode.attrib):
                    continue
                difficulty = mode.attrib['Difficulty']
                if (difficulty not in diff):
                    continue
                difficulty = diff[difficulty]

                ####### GET INFO ON PLAYERS #######
                # Only store top 10, to avoid an insanely long load time.
                players = mode.findall('./Player')
                if (len(players) > 10):
                    players = players[0:10]

                for player in players:
                    ####### GET SESSION DATA 'DddmmyyyyThhmmss' #######
                    if ('Session' not in player.attrib):
                        continue
                    session = player.attrib['Session']
                    if (not session[0] == 'D'):
                        continue
                    session = session[1:].split('T')
                    if (not len(session) == 2
                            or not len(session[0]) == 8
                            or not len(session[1]) == 6
                            or not session[0].isnumeric()
                            or not session[1].isnumeric()):
                        continue
                    # 'DD-MM-YYYY HH:MM:SS'
                    session = session[0][:2] + '-' + session[0][2:4] + '-' + session[0][4:] \
                              + ' ' \
                              + session[1][:2] + ':' + session[1][2:4] + ':' + session[1][4:]

                    ####### GET NAME DATA #######
                    name = player.findall('./Name')
                    if (len(name) < 1):
                        continue
                    name = ''.join(filter(str.isalnum, name[0].text))[0:16]
                    if (len(name) < 1):
                        continue

                    ####### GET SCORE DATA #######
                    # Can't have one without the other, no 0 scores either!
                    base_score = player.findall('./BaseScore')
                    bonus_points = player.findall('./BonusPoints')
                    if (len(base_score) < 1 or len(bonus_points) < 1):
                        continue
                    base_score = base_score[0].text
                    bonus_points = bonus_points[0].text
                    if (not base_score.isnumeric() or not bonus_points.isnumeric()):
                        continue
                    bonus_points = int(bonus_points)
                    base_score = int(base_score)
                    if (base_score > 100 or base_score <= 0
                            or bonus_points < 0 or bonus_points > 20):
                        continue
                    # SQL database expects total_score, not base_score
                    total_score = bonus_points + base_score
                    insert_player = "INSERT INTO players(playerid, name, session) " \
                                    "VALUES({playerid},'{name}', '{session}');".format(playerid=playerid, name=name,
                                                                                       session=session)
                    insert_score = "INSERT INTO scores(playerid, difficulty, total_score, bonus_points) " \
                                   "VALUES ({playerid}, {difficulty}, {total_score}, {bonus_points});".format(
                        playerid=playerid, difficulty=difficulty,
                        total_score=total_score, bonus_points=bonus_points)

                    # ALL DATA OBTAINED, INSERT!
                    try:
                        curs.execute(insert_player)
                        curs.execute(insert_score)
                        curs.connection.commit()
                        playerid += 1
                    except:
                        print("Failed to input score for player:", name, "with score:", total_score)
                        continue
        self.close_sql(curs)

    def export_xml(self, file='leaderboard.xml'):
        """export_xml() takes the data from the SQL database and saves the top ten scores
        to an XML file for users to read, analyze, or use in another installation."""

        """<!DOCTYPE HighScores [
            <!ELEMENT HighScores (GameMode+)>
            <!ELEMENT GameMode (Player*)>
            <!ATTLIST GameMode Difficulty ID #REQUIRED>
            <!--BaseScore + BonusPoints = TotalScore-->
            <!ELEMENT Player (Name, BaseScore, BonusPoints)>
            <!--Session is a timestamp-->
            <!ATTLIST Player Session ID #REQUIRED>
            <!ELEMENT Name (#PCDATA)>
            <!ELEMENT BaseScore (#PCDATA)>
            <!ELEMENT BonusPoints (#PCDATA)>
            ]>"""

        curs = self.init_sql()
        select_all = '''SELECT players.name, players.session, 
                            scores.total_score - bonus_points AS base_score, 
                            bonus_points, 
                            difficulty.name AS difficulty
                        FROM players 
                        INNER JOIN scores 
                        ON scores.playerid = players.playerid 
                        INNER JOIN difficulty 
                        ON difficulty.rounds = scores.difficulty 
                        WHERE difficulty.rounds = {difficulty}
                        ORDER BY rounds, total_score DESC
                        LIMIT 10'''

        root = xtree.Element("HighScores")
        root.text = '\n\t'  # New lines and tabs for pretty printing
        for difficulty in range(8, 18, 2):
            select_scores = select_all.format(difficulty=difficulty)
            scores = curs.execute(select_scores).fetchall()

            if (len(scores) > 0):
                gamemode = xtree.SubElement(root, 'GameMode', {'Difficulty': scores[0][4]})
                gamemode.text = '\n\t\t'
                gamemode.tail = '\n\t'

                for score in scores:
                    name = score[0]
                    # Format session
                    session = "D" + sub(' ', 'T', sub(':|-', '', score[1]))
                    base_score = str(score[2])
                    bonus_points = str(score[3])
                    player_elem = xtree.SubElement(gamemode, 'Player', {'Session': session})
                    player_elem.text = '\n\t\t\t'
                    player_elem.tail = '\n\t\t'

                    xtree.SubElement(player_elem, 'Name').text = name
                    xtree.SubElement(player_elem, 'BaseScore').text = base_score
                    xtree.SubElement(player_elem, 'BonusPoints').text = bonus_points
                    player_elem[0].tail = '\n\t\t\t'
                    player_elem[1].tail = '\n\t\t\t'
                    player_elem[2].tail = '\n\t\t'

                gamemode[-1].tail = '\n\t'

        root[-1].tail = '\n'
        tree = xtree.ElementTree(root)
        tree.write(file, xml_declaration=True)
