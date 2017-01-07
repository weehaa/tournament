#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE from matches")
    c.execute("UPDATE standings SET matches = 0, wins = 0")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    # TBD: cascade deletion in DB?
    c.execute("DELETE from standings")
    c.execute("DELETE from players")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(1) from players")
    cnt = int(c.fetchone()[0])
    db.close()
    return cnt

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    # TBD: trigger insert into standings in DB for a new player
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    c.execute("INSERT INTO standings (player_id) SELECT id FROM players WHERE name = (%s)", (name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute('''SELECT p.id, p.name, s.wins, s.matches FROM players p, standings s
                WHERE p.id = s.player_id ORDER BY s.wins DESC''')
    rows = c.fetchall()
    db.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser))
    c.execute("UPDATE standings SET matches = matches + 1 WHERE player_id IN (%s, %s)", (winner, loser))
    c.execute("UPDATE standings SET wins = wins + 1 WHERE player_id = (%s)", (winner,))
    db.commit()
    db.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairs = []
    s = playerStandings()
    for i in range(0, len(s), 2):
        pairs.append((s[i][0], s[i][1], s[i+1][0], s[i+1][1]))
    return pairs
