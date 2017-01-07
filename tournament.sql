-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (id SERIAL PRIMARY KEY, name VARCHAR(50));

CREATE TABLE matches (id SERIAL PRIMARY KEY,
                      winner INTEGER REFERENCES players(id),
                      loser INTEGER REFERENCES players(id)
                    );

CREATE VIEW v_standings AS
  SELECT p.id, p.name, count(m.winner) AS wins,
          count(m1.loser) + count(m.winner) AS matches
    FROM players p LEFT JOIN matches m ON m.winner = p.id
    LEFT JOIN matches m1 ON m1.loser = p.id
  GROUP BY p.id, p.name
  ORDER BY wins DESC;
