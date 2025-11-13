import pandas as pd

leaguesInFocus = ["E0", "E1", "F1", "D1", "SP1", "SP2", "I1", "I2", "N1", "P1", "B1", "T1", "NOR", "DEN", "SC0"]

df = pd.read_csv("data/Matches.csv")
df = df[df["Division"].isin(leaguesInFocus)]

df["MatchDate"] = pd.to_datetime(df["MatchDate"], format="%Y-%m-%d")
training = df.loc[(df["MatchDate"] >= "2001-01-01") & (df["MatchDate"] <= "2023-01-01")]
training.to_csv("data/training_data.csv", index=False)

validation = df.loc[(df["MatchDate"] > "2023-01-01") & (df["MatchDate"] <= "2025-06-01")]
validation.to_csv("data/validation_data.csv", index=False)

test = df.loc[(df["MatchDate"] >= "2001-01-01") & (df["MatchDate"] <= "2003-01-01")]
test.to_csv("data/test_data.csv", index=False)

row_count = 0
form_at_home = []
form_while_away = []
home_name_index = 3
away_name_index = 4
has_home_form_dict = {}
has_away_form_dict = {}

def find_form(team_name, form_type, data, row_index):
    """ Finds the form of team when home or away from the last 3 games"""
    if form_type == "Home":
        form_at_home = 0
        count = 0
        while count < 3:
            pass  
    elif form_type == "Away":
        pass       

for row in test:
    home_name = row[home_name_index]
    away_name = row[away_name_index]
    if home_name in has_home_form_dict.keys():
        pass
    else:
        find_form(home_name, "Home")
    if away_name in has_away_form_dict.keys():
        pass
    else:
        find_form(away_name, "Away")
     