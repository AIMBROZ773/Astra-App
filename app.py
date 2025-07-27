import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

def calculate_performance_score(player_data):
    kda_score = (player_data.get('kills', 0) * 2.2) + (player_data.get('assists', 0) * 1.8) - (player_data.get('deaths', 0) * 1.5)
    damage_score = player_data.get('damage_dealt', 0) / 10000
    gold_score = player_data.get('gold', 0) / 1000
    teamfight_score = player_data.get('teamfight_participation', 0) / 10
    return round(kda_score + damage_score + gold_score + teamfight_score, 1)

def load_mock_data():
    with open('mock_data.json', 'r') as f:
        return json.load(f)

@app.route('/analyze', methods=['POST'])
def analyze_route():
    print("SUCCESS: /analyze route was reached.")
    match_details = load_mock_data()
    winning_team_color = match_details.get('winning_team')

    for team_color in match_details['teams']:
        for player in match_details['teams'][team_color]:
            player['performance_score'] = calculate_performance_score(player)
        
        sorted_team = sorted(match_details['teams'][team_color], key=lambda p: p['performance_score'], reverse=True)
        
        for i, player in enumerate(sorted_team):
            rank = i + 1
            if rank == 1:
                if team_color == winning_team_color:
                    player['medal'] = "MVP"
                else:
                    player['medal'] = "MVP_LOSS"
            elif rank == 2:
                player['medal'] = "GOLD"
            else:
                player['medal'] = "SILVER" # Simplified for 2-player teams
    
    return jsonify(match_details)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 