import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

def get_db_connection(db_path='database.db') -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def execute_sql_script(script_path: str, conn: sqlite3.Connection, db_path='database.db'):
    try:
        c = conn.cursor()
        with open(script_path, 'r') as file:
            sql_script = file.read()
        c.executescript(sql_script)
    except sqlite3.OperationalError as e:
        print(f"Error when executing {script_path}\nError: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()
    return True

def init_db(script_path, db_path='database.db'):

    if (input("Are you sure you want to reset the database? (y/n): ") != 'y'):
        return
    
    # delete the database
    if(os.path.exists(db_path)):
        os.remove(db_path)
    
    conn = get_db_connection()

    # Execute init script
    print(f"Executing init script {script_path}...")
    execute_sql_script(script_path, conn)

    print("Database initialized successfully.")

def upgrade_database(script_path, db_path='database.db'):
    conn = get_db_connection()

    print(f"Executing upgrade script {script_path}...")
    execute_sql_script(script_path, conn)
    print("Database upgraded successfully.")

def read_img(img_path):
    with open(img_path, 'rb') as file:
        img = file.read()
    return img

def add_init_data(script_path: str):
    conn = get_db_connection()
    c = conn.cursor()

    try:
        # Add intial data
        c.execute("INSERT INTO players (firstname, lastname, username, password, image) VALUES (?, ?, ?, ?, ?)",
                  ('Rok', 'Ivancic', 'rivancic', generate_password_hash('rivancic123'), 'https://cosylab-hrm.my.salesforce.com/_slds/images/themes/lightning_lite/lightning_lite_profile_avatar_200.png'))
        c.execute("INSERT INTO players (firstname, lastname, username, password, image) VALUES (?, ?, ?, ?, ?)",
                  ('Anja', 'Parkelj', 'aparkelj', generate_password_hash('aparkelj456'), 'https://cosylab-hrm.file.force.com/profilephoto/7295q000000oNrD/F'))
        c.execute("INSERT INTO players (firstname, lastname, username, password, image) VALUES (?, ?, ?, ?, ?)",
                  ('Janez', 'Krusic', 'jkrusic', generate_password_hash('jkrusic465'), 'https://cosylab-hrm.file.force.com/profilephoto/72909000000M6EK/F'))
        c.execute("INSERT INTO players (firstname, lastname, username, password, image) VALUES (?, ?, ?, ?, ?)",
                  ('Blaz', 'Kusnik', 'bkusnik', generate_password_hash('bkusnik312'), 'https://cosylab-hrm.file.force.com/profilephoto/72909000000M6E1/F'))
        c.execute("INSERT INTO players (firstname, lastname, username, password, image) VALUES (?, ?, ?, ?, ?)",
                  ('Aljaz', 'Gerecnik', 'agerecnik', generate_password_hash('agerecnik654'), 'https://cosylab-hrm.my.salesforce.com/servlet/servlet.FileDownload?file=00P09000004a3CLEAY'))
        c.execute("INSERT INTO players (firstname, lastname, username, password, image) VALUES (?, ?, ?, ?, ?)",
                  ('Martin', 'Gladovic', 'mgladovic', generate_password_hash('mgladovic112'), 'https://cosylab-hrm.file.force.com/servlet/servlet.FileDownload?file=00P09000004a3E1EAI'))
                
        
        # Execute matches data script
        print(f"Executing init script {script_path}...")
        execute_sql_script(script_path, conn)

        print("Database initialized successfully.")
        # # Rok wins
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (1, 2, 1, 2, 0, '2024-02-15', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (1, 2, 1, 2, 0, '2024-02-15', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (1, 2, 1, 2, 0, '2024-02-12', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (1, 2, 1, 2, 0, '2024-02-22', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (1, 2, 1, 2, 0, '2024-02-29', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (1, 4, 1, 4, 1, '2024-02-29', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (1, 2, 1, 2, 0, '2024-03-05', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (1, 2, 1, 2, 0, '2024-03-12', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (1, 2, 1, 2, 0, '2024-03-25', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (1, 3, 1, 3, 1, '2024-03-25', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (1, 5, 1, 5, 0, '2024-03-29', 1)")

        # # Anja wins
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (2, 1, 2, 1, 0, '2024-02-15', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (2, 1, 2, 1, 0, '2024-02-15', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (2, 1, 2, 1, 1, '2024-02-12', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (2, 1, 2, 1, 0, '2024-02-22', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (2, 1, 2, 1, 0, '2024-02-29', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (2, 1, 2, 1, 1, '2024-02-29', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (2, 3, 2, 3, 1, '2024-03-05', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (2, 4, 2, 4, 1, '2024-03-12', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (2, 1, 2, 1, 0, '2024-03-12', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (2, 1, 2, 1, 0, '2024-03-27', 1)")

        # # Janez wins
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (3, 2, 3, 2, 0, '2024-03-12', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (3, 2, 3, 2, 0, '2024-03-12', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (3, 2, 3, 2, 0, '2024-03-12', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (3, 2, 3, 2, 0, '2024-03-19', 1)")
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (3, 5, 3, 5, 0, '2024-03-29', 1)")

        # # Aljaz wins
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (5, 1, 5, 1, 0, '2024-03-29', 1)")

        # # Blaz wins
        # c.execute("INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id) VALUES (4, 2, 4, 2, 0, '2024-02-15', 1)")
    except Exception as e:
        print(f"Error adding initial data: {e}")

    print("Initial data added successfully.")



if __name__ == "__main__":
    init_db('sql/init.sql')
    upgrade_database('sql/upgrade1.sql')
    add_init_data('sql/matches_202404030911.sql')
    