-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;
\c tournament
CREATE TABLE players (id SERIAL, name VARCHAR(50));
ALTER TABLE players ADD PRIMARY KEY (id);
CREATE TABLE matches (winner INTEGER REFERENCES players(id),
                      loser INTEGER REFERENCES players(id),
                      PRIMARY KEY (winner, loser));
CREATE TABLE standings (player_id INTEGER REFERENCES players(id),
                        wins INTEGER default 0,
                        matches INTEGER default 0);
ALTER TABLE matches add column id SERIAL;
