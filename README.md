This project is connected to the Udacity course Intro to Relational Databases.
It uses the PostgreSQL database to keep track of players and matches in a game
tournament.

The game tournament use the Swiss system for pairing up players in
each round:
players are not eliminated, and each player should be paired with another player
 with the same number of wins, or as close as possible.

tournament.sql file contains database schema.
Use the command \i tournament.sql to import the whole file into psql at once.

tournament.py contains several functions:

registerPlayer(name)

Adds a player to the tournament by putting an entry in the database.

countPlayers()

Returns the number of currently registered players.

deletePlayers()

Clear out all the player records from the database.

reportMatch(winner, loser)

Stores the outcome of a single match between two players in the database.

deleteMatches()

Clear out all the match records from the database.

playerStandings()

Returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has.

swissPairings()

Given the existing set of registered players and the matches they have played, generates and returns a list of pairings according to the Swiss system. Each pairing is a tuple (id1, name1, id2, name2), giving the ID and name of the paired players.
