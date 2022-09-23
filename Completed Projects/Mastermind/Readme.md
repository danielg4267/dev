# Mastermind

I recommend reading a little bit about Mastermind on its wikipedia page, found here: https://en.wikipedia.org/wiki/Mastermind_(board_game)

However, I will summarize.

Mastermind is a board game in which one player (the mastermind) generates a code of colors and the other player tries to guess what it is. For example, if the mastermind's code is [red, green, blue, yellow], the other player will need to guess that exact sequence of colors. They do this by placing pegs in slots on the board that represent a single round. When the player is done submitting their guess, the mastermind will alert them to correct colors using another, smaller set of pegs used to represent the number of colors a player got correct in that round - these are called bulls and cows. A bull represents a correct color in the correct space, and a cow represents a correct color in the wrong space. For example, if a player guessed [red, blue, orange, green] for the previous code example, They would have one bull (red) and two cows (blue, green). Orange is just a wrong color, and there is no indicator for that. Bull and cow pegs are placed in random order - they do not identify which slot is a bull, or which slot is a cow. It is up to the player to figure that out. As the game progresses, the player can use these clues to hopefully guess the mastermind's code before the last round. However, if they do not, the mastermind wins.

My final project of my first semester of the MSCS program was to recreate this game using Python, specifically its turtle module. We had not learned about OOD at the time, but my professor asked that we try to do research on our own about this design paradigm, and use it to implement our code, however it was not required. Otherwise, the requirements were relatively simple: Implement the game Mastermind, and keep track of scores.

I had a lot of fun with this project. It was certainly my favorite for a while. I felt it had a lot of potential, and refactored it to have some extra features. Namely, it can export high scores in an organized manner (I chose an XML file) for human readability, and import those scores back into the database. In addition, I added a config file, that changes how the game is played and what it looks like (some of which provide bonus points!). I also have scores saved in a SQLite database, rather than a simple text file, for consitency's sake. Lastly, I added some inheritance, to reduce code repetition.

Run the "Start.py" 
