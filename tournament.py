#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection
    and a cursor."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("ERROR: Can't connect to {} database".format(database_name))
        quit()


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()

    query = "TRUNCATE TABLE matches"
    cursor.execute(query)

    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()

    query = "TRUNCATE TABLE players CASCADE"
    cursor.execute(query)

    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()

    query = "SELECT count(1) from players"
    cursor.execute(query)
    cnt = int(cursor.fetchone()[0])

    db.close()
    return cnt


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()

    query = "INSERT INTO players (name) VALUES (%s)"
    params = (name,)
    cursor.execute(query, params)

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
    db, cursor = connect()

    query = "SELECT * FROM v_standings"
    cursor.execute(query)
    rows = cursor.fetchall()

    db.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()

    query = '''INSERT INTO matches (winner, loser)
                VALUES (%s, %s)'''
    params = (winner, loser,)
    cursor.execute(query, params)

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
