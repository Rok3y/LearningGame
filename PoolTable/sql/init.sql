CREATE TABLE players 
(id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, username TEXT, password TEXT);

CREATE TABLE matches 
    (id INTEGER PRIMARY KEY, player1_id INTEGER, player2_id INTEGER, winner_id INTEGER, loser_id INTEGER, win_black BOOLEAN, game_played DATE, writer_id INTEGER, writer_ip TEXT,
    FOREIGN KEY(player1_id) REFERENCES players(id), 
    FOREIGN KEY(player2_id) REFERENCES players(id), 
    FOREIGN KEY(winner_id) REFERENCES players(id), 
    FOREIGN KEY(loser_id) REFERENCES players(id),
    FOREIGN KEY(writer_id) REFERENCES players(id));