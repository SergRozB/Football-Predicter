import network
import create_data_file
import numpy as np

training_data, validation_data = create_data_file.create_data()

net = network.load("test_network")

def return_prediction(date, team):
    data = create_data_file.find_data(date, team)
    if data != None:
        raw = net.give_prediction(data[0])
        home_team = data[1][0][0]
        away_team = data[1][0][1]
        home_score = int(data[1][0][2])
        away_score = int(data[1][0][3])
        result = ""
        if home_score > away_score:
            result += home_team + " wins"
        elif home_score == away_score:
            result += "Draw"
        else:
            result += away_team + " wins"
        prediction = np.argmax(raw)
        prediction_text = ""
        if prediction == 0:
            prediction_text = home_team + " wins"
        elif prediction == 1:
            prediction_text = "Draw"
        else:
            prediction_text = away_team + " wins"
        result += f", score (Home - Away) was {home_score} - {away_score}."
        oddsHome = (raw[0]/(raw[0] + raw[1] + raw[2]))
        oddsDraw = (raw[1]/(raw[0] + raw[1] + raw[2]))
        oddsAway = (raw[2]/(raw[0] + raw[1] + raw[2]))
        print("Match:", home_team, "-", away_team, "| Raw output:", raw, "| Network prediction:", prediction_text, "| Odds: H -", 
              oddsHome, "D -", oddsDraw, "A -", oddsAway, "| Actual result:", result)
    else:
        print("Match not found in database")

#return_prediction("2025-03-15", "Brighton")
return_prediction("2025-05-11", "Barcelona")