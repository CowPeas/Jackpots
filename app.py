import sqlite3
import pickle
from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# Step 1: Database connection
conn = sqlite3.connect('player_attributes.sqlite')
conn.execute('''CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY,
                player_name TEXT,
                potential INTEGER,
                crossing INTEGER,
                finishing INTEGER,
                heading_accuracy INTEGER,
                short_passing INTEGER,
                volleys INTEGER,
                dribbling INTEGER,
                curve INTEGER,
                free_kick_accuracy INTEGER,
                long_passing INTEGER,
                ball_control INTEGER,
                acceleration INTEGER,
                sprint_speed INTEGER,
                agility INTEGER,
                reactions INTEGER,
                balance INTEGER,
                shot_power INTEGER,
                jumping INTEGER,
                stamina INTEGER,
                strength INTEGER,
                long_shots INTEGER,
                aggression INTEGER,
                interceptions INTEGER,
                positioning INTEGER,
                vision INTEGER,
                penalties INTEGER,
                marking INTEGER,
                standing_tackle INTEGER,
                sliding_tackle INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
conn.commit()

# Step 2: Load machine learning model
model = pickle.load(open('model.pkl', 'rb'))

# Step 3: Initialize LoginManager
login_manager = LoginManager(app)

# Step 4: Define User model
class User:
    def __init__(self, user_id):
        self.id = user_id

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

# Step 5: Implement function to load user
@login_manager.user_loader
def load_user(user_id):
    # Retrieve user from your database based on user_id
    return User(user_id)

# Route for player registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract data from the request
        player_data = request.form

        # Validate player data (add your own validation logic)
        if not player_data['player_name'] or not player_data['potential']:
            return jsonify({'error': 'Player name and potential are required'})

        try:
            # Start a database transaction
            with conn:
                # Store player data in the database
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO players (
                        player_name, potential, crossing, finishing, heading_accuracy, short_passing, volleys, dribbling,
                        curve, free_kick_accuracy, long_passing, ball_control, acceleration, sprint_speed, agility, reactions,
                        balance, shot_power, jumping, stamina, strength, long_shots, aggression, interceptions, positioning,
                        vision, penalties, marking, standing_tackle, sliding_tackle
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    player_data['player_name'], player_data['potential'], player_data['crossing'], player_data['finishing'],
                    player_data['heading_accuracy'], player_data['short_passing'], player_data['volleys'],
                    player_data['dribbling'], player_data['curve'], player_data['free_kick_accuracy'],
                    player_data['long_passing'], player_data['ball_control'], player_data['acceleration'],
                    player_data['sprint_speed'], player_data['agility'], player_data['reactions'], player_data['balance'],
                    player_data['shot_power'], player_data['jumping'], player_data['stamina'], player_data['strength'],
                    player_data['long_shots'], player_data['aggression'], player_data['interceptions'],
                    player_data['positioning'], player_data['vision'], player_data['penalties'], player_data['marking'],
                    player_data['standing_tackle'], player_data['sliding_tackle']
                ))
            return jsonify({'message': 'Player registered successfully'})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)})
    else:
        return render_template('register.html')


# Route for player login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Code to handle player login
        # Verify credentials, create session, or return appropriate error
        player_data = request.form

        # Validate player data (add your own validation logic)
        if not player_data['player_name'] or not player_data['potential']:
            return jsonify({'error': 'Player name and potential are required'})

        # Validate the player and log in
        user = User(player_data['player_name'])
        login_user(user)
        return jsonify({'message': 'Player logged in successfully'})
    else:
        return render_template('login.html')


# Route for player logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    # Code to handle player logout
    # Destroy session, invalidate token, or perform any necessary cleanup
    logout_user()
    return jsonify({'message': 'Player logged out successfully'})


# Route for updating player profile with stats
@app.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        # Extract data from the request
        player_data = request.form

        # Validate player data (add your own validation logic)
        if not player_data['player_id'] or not player_data['potential']:
            return jsonify({'error': 'Player ID and potential are required'})

        try:
            # Start a database transaction
            with conn:
                # Update player profile in the database
                cursor = conn.cursor()
                cursor.execute('UPDATE players SET potential=?, crossing=?, finishing=?, heading_accuracy=?, short_passing=?, '
                               'volleys=?, dribbling=?, curve=?, free_kick_accuracy=?, long_passing=?, ball_control=?, '
                               'acceleration=?, sprint_speed=?, agility=?, reactions=?, balance=?, shot_power=?, jumping=?, '
                               'stamina=?, strength=?, long_shots=?, aggression=?, interceptions=?, positioning=?, vision=?, '
                               'penalties=?, marking=?, standing_tackle=?, sliding_tackle=? WHERE player_id=?',
                               (player_data['potential'], player_data['crossing'], player_data['finishing'],
                                player_data['heading_accuracy'], player_data['short_passing'], player_data['volleys'],
                                player_data['dribbling'], player_data['curve'], player_data['free_kick_accuracy'],
                                player_data['long_passing'], player_data['ball_control'], player_data['acceleration'],
                                player_data['sprint_speed'], player_data['agility'], player_data['reactions'],
                                player_data['balance'], player_data['shot_power'], player_data['jumping'],
                                player_data['stamina'], player_data['strength'], player_data['long_shots'],
                                player_data['aggression'], player_data['interceptions'], player_data['positioning'],
                                player_data['vision'], player_data['penalties'], player_data['marking'],
                                player_data['standing_tackle'], player_data['sliding_tackle'], player_data['player_id']))
            return jsonify({'message': 'Player profile updated successfully'})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)})
    else:
        return render_template('update_profile.html')

# Route for retrieving player attributes over time
@app.route('/profile/history/<int:player_id>', methods=['GET'])
@login_required
def get_player_history(player_id):
    # Retrieve player attributes from the database
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players WHERE player_id=? ORDER BY created_at ASC',
                   (player_id,))
    rows = cursor.fetchall()

    # Format the attributes as a list of dictionaries
    attributes = [{'potential': row[2], 'created_at': row[3]} for row in rows]

    return jsonify({'player_id': player_id, 'attributes': attributes})

# Route for calculating overall rating from machine learning model
@app.route('/overall_rating', methods=['GET', 'POST'])
@login_required
def calculate_overall_rating():
    if request.method == 'POST':
        # Extract player stats from the request
        player_data = request.form

        # Validate player data (add your own validation logic)
        if not player_data['potential']:
            return jsonify({'error': 'Player potential is required'})

        # Pass player stats to the machine learning model and calculate overall rating
        rating = model.predict([[
            player_data['potential'], player_data['crossing'], player_data['finishing'],
            player_data['heading_accuracy'], player_data['short_passing'], player_data['volleys'],
            player_data['dribbling'], player_data['curve'], player_data['free_kick_accuracy'],
            player_data['long_passing'], player_data['ball_control'], player_data['acceleration'],
            player_data['sprint_speed'], player_data['agility'], player_data['reactions'],
            player_data['balance'], player_data['shot_power'], player_data['jumping'],
            player_data['stamina'], player_data['strength'], player_data['long_shots'],
            player_data['aggression'], player_data['interceptions'], player_data['positioning'],
            player_data['vision'], player_data['penalties'], player_data['marking'],
            player_data['standing_tackle'], player_data['sliding_tackle']
        ]])

        return jsonify({'overall_rating': rating.item()})  # Convert numpy float to Python float
    else:
        return render_template('overall_rating.html')


if __name__ == '__main__':
    app.run()
