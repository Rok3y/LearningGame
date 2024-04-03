from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "b'\xfb=Q233\xe4\xaf\x1d\xe5\x1a_\xdaB+\xfa\xf6L~\x12\x9d\x98U`\x07\x89'" # This is used to encrypt session data
# For production use, store the secret key in a separate file and read it here instead of generating it every time
auth = HTTPBasicAuth()

def get_db_connection():
    conn = sqlite3.connect("database.db") # r'C:\Users\rivancic\OneDrive - cosylab.com\database_cslpool.db'
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

# Placeholder for table data
rows = []
players = []

@auth.verify_password
def verify_password(username, password):
    conn = get_db_connection()
    auth_user = conn.execute(f'SELECT * FROM players WHERE username = ?', (username,)).fetchone()
    if auth_user is None or not check_password_hash(auth_user['password'], password):
        return False
    # Store user information in session or another secure place
    session['auth_user'] = {'id': auth_user['id'], 'username': auth_user['username'], 'profile_picture': auth_user['image'], 'full_name': auth_user['firstname'] + ' ' + auth_user['lastname']}
    return True

@app.route('/logout')
def logout():
    session.pop('auth_user', None)
    return redirect(url_for('index'))

@app.route('/login')
@auth.login_required
def login():
    return redirect(url_for('index'))

@app.route('/', methods=['POST'])
@auth.login_required
def table():
    conn = get_db_connection()
    sender_ip = request.remote_addr
    # Retrieve data from form
    p1 = request.form['Player1']
    p2 = request.form['Player2']
    win = request.form['Winner']
    win_black = 'win_black' in request.form
    
    # Get player IDs
    player1 = conn.execute('SELECT id, firstname, lastname, image FROM players WHERE firstname = ? AND lastname = ?', (p1.split()[0], p1.split()[1])).fetchone()
    player2 = conn.execute('SELECT id, firstname, lastname FROM players WHERE firstname = ? AND lastname = ?', (p2.split()[0], p2.split()[1])).fetchone()
    winner = player1 if win == p1 else player2
    loser = player1 if win == p2 else player2
    winner_name = winner['firstname'] + ' ' + winner['lastname']
    #loser_name = loser['firstname'] + ' ' + loser['lastname']

    # Check if the players are the same
    if player1['id'] == player2['id']:
        flash('Players must be different', 'danger')
        return redirect(url_for('index'))
    
    # Check if the winner is the same as the player1 or player2
    if winner['id'] != player1['id'] and winner['id'] != player2['id']:
        flash('Winner must be one of the players', 'danger')
        return redirect(url_for('index'))
    
    player1_id = player1['id']
    player2_id = player2['id']
    winner_id = winner['id']
    loser_id = loser['id']

    try:
        # Add the new row to our data structure
        conn.execute('INSERT INTO matches (player1_id, player2_id, winner_id, loser_id, win_black, game_played, writer_id, writer_ip) VALUES (?, ?, ?, ?, ?, CURRENT_DATE, ?, ?)',
                        (player1_id, player2_id, winner_id, loser_id, win_black, session['auth_user']['id'], sender_ip))
        conn.commit()
        flash(f'Tekma dodana!', 'success')
        flash(f'{winner_name} je zmagal!', 'success')
    except Exception as e:
        flash(f'Error adding match: {e}', 'danger')
    
    return redirect(url_for('table'))

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()    
    # Retrieve all entries from the database
    matches = conn.execute("""
        SELECT m.id, 
            p1.firstname || ' ' || p1.lastname AS player1_name, 
            p2.firstname || ' ' || p2.lastname AS player2_name, 
            pw.firstname || ' ' || pw.lastname AS winner_name, 
            pl.firstname || ' ' || pl.lastname AS loser_name, 
            m.game_played,
            m.win_black
        FROM matches m
            JOIN players p1 ON m.player1_id = p1.id
            JOIN players p2 ON m.player2_id = p2.id
            JOIN players pw ON m.winner_id = pw.id
            JOIN players pl ON m.loser_id = pl.id
        ORDER BY DATE(m.game_played) DESC;
        """).fetchall()

    players_data = conn.execute('SELECT * FROM players').fetchall()
    players = [(player['firstname'] + ' ' + player['lastname']) for player in players_data]
    players.insert(0, 'Select player')

    common = []

    # write sql query to get all wins and losses for each player
    for player in players_data:
        wins = conn.execute('SELECT COUNT(*) FROM matches WHERE winner_id = ?', (player['id'],)).fetchone()[0]
        losses = conn.execute('SELECT COUNT(*) FROM matches WHERE loser_id = ?', (player['id'],)).fetchone()[0]
        wins_with_black = conn.execute('SELECT COUNT(*) FROM matches WHERE winner_id = ? and win_black = 1', (player['id'],)).fetchone()[0]
        profile_picture = player['image']
        
        common.append({'player': player['firstname'] + ' ' + player['lastname'], 'profile_picture': profile_picture, 'wins': wins, 'losses': losses, 'wins_with_black': wins_with_black})
        
    conn.close()
    
    return render_template('index.html', common=common, matches=matches, player1_options=players)

if __name__ == '__main__':
    app.run(debug=True)
