import numpy as np
import pandas as pd
considered_columns = ["HomeElo", "AwayElo", "Form3Home", "Form5Home", "Form3Away", "Form5Away", "HomeShots", "AwayShots", "HomeTarget", "AwayTarget", 
                          "HomeFouls", "AwayFouls", "HomeCorners", "AwayCorners", "HomeYellow", "AwayYellow", "HomeRed", "AwayRed"]

def create_data():
    training = pd.read_csv("data/training_data.csv")
    validation = pd.read_csv("data/validation_data.csv")
    
    training = training.dropna(axis=0, subset=considered_columns)
    validation = validation.dropna(axis=0, subset=considered_columns)

    reduced_training_input = training[considered_columns].to_numpy(np.set_printoptions(suppress=True))
    reduced_training_output = training[["FTResult"]].to_numpy(np.set_printoptions(suppress=True))

    reduced_validation_input = validation[considered_columns].to_numpy(np.set_printoptions(suppress=True))
    reduced_validation_output = validation[["FTResult"]].to_numpy(np.set_printoptions(suppress=True))

    # Put the inputs in vertical vector form

    temp_list = [np.zeros((11, 1)) for item in reduced_training_input]
    for i in range(len(reduced_training_input)):
        temp_list[i][0][0] = get_diff(reduced_training_input[i][0], reduced_training_input[i][1])
        temp_list[i][1][0] = reduced_training_input[i][2]/9
        temp_list[i][2][0] = reduced_training_input[i][3]/15
        temp_list[i][3][0] = reduced_training_input[i][4]/9
        temp_list[i][4][0] = reduced_training_input[i][5]/15
        temp_list[i][5][0] = get_diff(reduced_training_input[i][6], reduced_training_input[i][7])
        temp_list[i][6][0] = get_diff(reduced_training_input[i][8], reduced_training_input[i][9])
        temp_list[i][7][0] = get_diff(reduced_training_input[i][10], reduced_training_input[i][11])
        temp_list[i][8][0] = get_diff(reduced_training_input[i][12], reduced_training_input[i][13])
        temp_list[i][9][0] = get_diff(reduced_training_input[i][14], reduced_training_input[i][15])
        temp_list[i][10][0] = get_diff(reduced_training_input[i][16], reduced_training_input[i][17])
    reduced_training_input = temp_list

    temp_list = [np.zeros((11, 1)) for item in reduced_validation_input]
    for i in range(len(reduced_validation_input)):
        temp_list[i][0][0] = get_diff(reduced_validation_input[i][0], reduced_validation_input[i][1])
        temp_list[i][2][0] = reduced_validation_input[i][3]/15
        temp_list[i][3][0] = reduced_validation_input[i][4]/9
        temp_list[i][4][0] = reduced_validation_input[i][5]/15
        temp_list[i][5][0] = get_diff(reduced_validation_input[i][6], reduced_validation_input[i][7])
        temp_list[i][6][0] = get_diff(reduced_validation_input[i][8], reduced_validation_input[i][9])
        temp_list[i][7][0] = get_diff(reduced_validation_input[i][10], reduced_validation_input[i][11])
        temp_list[i][8][0] = get_diff(reduced_validation_input[i][12], reduced_validation_input[i][13])
        temp_list[i][9][0] = get_diff(reduced_validation_input[i][14], reduced_validation_input[i][15])
        temp_list[i][10][0] = get_diff(reduced_validation_input[i][16], reduced_validation_input[i][17])
    reduced_validation_input = temp_list
    #for i in range(len(reduced_training_input)):
        #print("G:", reduced_training_input[i], "| shape:", np.shape(reduced_training_input[i]))
        #reduced_training_input[i] = np.reshape(reduced_training_input[i], (6, 1))
        #reduced_training_input[i] = [[reduced_training_input[i][0]], [reduced_training_input[i][1]], [reduced_training_input[i][2]], [reduced_training_input[i][3]],
                                     #[reduced_training_input[i][4]],
                                     #[reduced_training_input[i][5]]]
    #for i in range(len(reduced_validation_input)):
        #reduced_validation_input[i] = np.reshape(reduced_validation_input[i], (6, 1))
        #reduced_validation_input[i] = [[reduced_validation_input[i][0]], [reduced_validation_input[i][1]], [reduced_validation_input[i][2]], [reduced_validation_input[i][3]], 
                                       #[reduced_validation_input[i][4]], 
                                       #[reduced_validation_input[i][5]]]

    # Form of output (Home win, Draw, Away win). If home win, (1, 0, 0), if draw, (0, 1, 0) etc.
    training_output_vector = []
    validation_output_vector = []
    for result in reduced_training_output:
        vector = 0
        if result == "H": vector = [1, 0, 0]
        if result == "D": vector =[0, 1, 0]
        if result == "A": vector = [0, 0, 1]
        vector = np.reshape(vector, (3, 1))
        training_output_vector.append(vector)
    reduced_training_output = np.asarray(training_output_vector)

    for result in reduced_validation_output:
        vector = 0
        if result == "H": vector = [1, 0, 0]
        if result == "D": vector = [0, 1, 0]
        if result == "A": vector = [0, 0, 1]
        vector = np.reshape(vector, (3, 1))
        validation_output_vector.append(vector) 
    reduced_validation_output = np.asarray(validation_output_vector)

    training_data = list(zip(reduced_training_input, reduced_training_output))
    validation_data = list(zip(reduced_validation_input, reduced_validation_output))
    #print("val:", validation_data)
    return training_data, validation_data

#print(create_data())
#create_data()
def get_diff(home, away):
    total = home+away
    if total > 0:
        return (home-away)/(home+away)
    else:
        return 0
    
def find_data(date, team):
    """ Finds the match with the corresponding date and team and returns the data in a way 
    which can be inputted into the neural network, along with an array containing the teams 
    involved and the full time result and scores. The date must be a string in the 
    format year-month-day like so: "xxxx-xx-xx". The team string must match the way it is 
    spelt in the data file. The match must meet some requirements: it must be a league match, 
    the league must be part of the 'selected leagues', all data in the 'considered columns' 
    must be present and the date must be between 2010-01-01 and 2025-06-01. Returns None if no
    match is found."""

    training = pd.read_csv("data/training_data.csv")
    validation = pd.read_csv("data/validation_data.csv")
    training = training.dropna(axis=0, subset=considered_columns)
    validation = validation.dropna(axis=0, subset=considered_columns)

    validation = validation.loc[(validation["MatchDate"] == date) & ((validation["HomeTeam"] == team) | (validation["AwayTeam"] == team))]
    if validation.size == 0:
        training = training.loc[(training["MatchDate"] == date) & ((training["HomeTeam"] == team) | (training["AwayTeam"] == team))]
        if training.size == 0:
            return None
        else:
            result = training[["HomeTeam", "AwayTeam", "FTHome", "FTAway"]]
            result = result.to_numpy()
            return (convert(training), result)
    else:
        result = validation[["HomeTeam", "AwayTeam", "FTHome", "FTAway"]]
        result = result.to_numpy()
        return (convert(validation), result)
    
def convert(row):
    """Converts the inputted row (which is a data frame) into a numpy array containing the 'considered columns'
    which can be inputted into the neural net."""
    row = row[considered_columns]
    row = row.to_numpy(np.set_printoptions(suppress=True))
    temp_list = np.zeros((11, 1))
    temp_list[0][0] = get_diff(row[0][0], row[0][1])
    temp_list[1][0] = row[0][2]/9
    temp_list[2][0] = row[0][3]/15
    temp_list[3][0] = row[0][4]/9
    temp_list[4][0] = row[0][5]/15
    temp_list[5][0] = get_diff(row[0][6], row[0][7])
    temp_list[6][0] = get_diff(row[0][8], row[0][9])
    temp_list[7][0] = get_diff(row[0][10], row[0][11])
    temp_list[8][0] = get_diff(row[0][12], row[0][13])
    temp_list[9][0] = get_diff(row[0][14], row[0][15])
    temp_list[10][0] = get_diff(row[0][16], row[0][17])
    return temp_list
