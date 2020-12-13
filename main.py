import json
import pandas as pd
import jsonlines
from utils import *

meta = open('json/NSH_ATL_meta.json')

# a list that will contain time-series lists of on-ball pressures
nested = []

# loading match metadata to a variable
game_info = json.load(meta)

# loading match tracking data, and parsing through it.
with jsonlines.open('json/NSH_ATL_tracking.jsonl') as tracking:
    for line in tracking.iter():
        op_loc = player_off(line)   # Getting a list of ball handler's number, x location, and y location.
        dp_loc = player_def(line)   # Getting a list of on-ball defenders' number, x location, and y location.
        if op_loc != None and dp_loc != None:   # Only loop through lists if they contain a value
            op_loc.append(line['gameClock'])
            dp_loc.append(line['gameClock'])
            if op_loc[-1] == dp_loc[-1]:    # Combining the ball handler's coordinates and defender coordinates, if the game clock is the same.
                combined = [op_loc, dp_loc]
            player_dist = get_dist(combined) # Now that both players' coordinates are in a list, get distance between defender and offensive player.

            # For each line in the tracking data file, create a list that contains:
            # [current period, time of the game in seconds, ball handler's number, defender's number, distance between the two]
            # then add each list to a nested list

            newlist = [str(line['period']), op_loc[-1], op_loc[0], dp_loc[0], player_dist]
            nested.append(newlist)

# filters the data so that the list only contains moments where the defender is approaching the ball handler.
filter = is_approaching(nested)

# replaces each players number with their name.
for i in filter:
    for j in range(len(i)):
        if i[j] == i[2]:
            i[j] = off_name_replace(i[j], game_info)
        elif i[j] == i[3]:
            i[j] = def_name_replace(i[j], game_info)
        else:
            pass

# The last step in cleaning the parsed data is to only allow 1 row per instance of ball pressure.
# Since each line of tracking data is 0.04 seconds of a game, one instance of ball pressure might take up hundreds of rows.
# To solve this, the first row of ball pressure is returned and appended to a new list.
# This allows us to know the name of the ball handler, the name of the defender, the time in the period (seconds)
# that the pressure started, and the distance the defender was from the ball handler (in meters).

final = []
for i in range(len(filter)-1):
    if filter[i][2] != filter[i+1][2]:
        final.append(filter[i])
    else:
        pass

# A Pandas DataFrame is created with the cleaned data and sent off to a CSV file.

csv_headers = ['period', 'game_time', 'player_off', 'player_def', 'distance_away']

df = pd.DataFrame(final, columns=csv_headers)

df.to_csv('csv_data/pressures_vs_atl.csv', index=False)

meta.close()

