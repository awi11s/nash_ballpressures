import math

# function that will match a Nashville player number in the tracking data with the number in the metadata json file,
# and return the Nashville player's name

def off_name_replace(i, game):
    for p in game['homePlayers']:
        while (p['number'] == i):
            return p['name']

# same as the above function, except for Atlanta players

def def_name_replace(i, game):
    for p in game['awayPlayers']:
        while (p['number'] == i):
            return p['name']

# A function that takes in a line of the tracking data, and finds which Nashville player
# had possession of the ball. This was done by checking first that play was live, and that Nashville had the last touch.
# A distance formula was used to find which Nashville player was closes to the ball (or within 1 meter).
# The function returns a list with the number of the player possessing the ball, along with their x and y coordinates on the pitch.

def player_off(event):
    lis = []
    if event['live'] is True and event['lastTouch'] == 'home':
        ball = [event['ball']['xyz'][0], event['ball']['xyz'][1]]
        for i in event['homePlayers']:
            player = [i['xyz'][0], i['xyz'][1]]
            distance = math.sqrt(((ball[0] - player[0]) ** 2) + ((ball[1] - player[1]) ** 2))
            if distance < 1.0:
                lis.append(i['number'])
                lis.append(i['xyz'][0])
                lis.append(i['xyz'][1])
                return lis
            else:
                pass

    else:
        pass

# This function takes in a line of the tracking data as a parameter After making sure that play is live and Nashville
# had the last touch, the function finds the closest defender to the ball, within 5 yards (or 4.5 meters).
# Needs improvement:
#       using the coordinates of the offensive player possessing the ball, instead of the ball's coordinates.

def player_def(event):
    lis = []
    if event['live'] is True and event['lastTouch'] == 'home':
        ball = [event['ball']['xyz'][0], event['ball']['xyz'][1]]
        for i in event['awayPlayers']:
            player = [i['xyz'][0], i['xyz'][1]]
            distance = math.sqrt(((ball[0] - player[0]) ** 2) + ((ball[1] - player[1]) ** 2))
            if distance < 4.5:
                lis.append(i['number'])
                lis.append(i['xyz'][0])
                lis.append(i['xyz'][1])
                return lis
            else:
                pass

# Once the coordinates of the offensive player and his defender are returned,
# this function will get the distance between both the offensive player and his defender.
def get_dist(list):
        distance = math.sqrt(((list[0][1] - list[1][1]) ** 2) + ((list[0][2] - list[1][2]) ** 2))
        return distance


# Since we want to make sure the defender is moving towards the offensive player,
# this function is used to make sure that the distance between both players is decreasing over time.

def is_approaching(list):
    g_list = []
    for i in range(len(list)):
        if list[i][-1] < list[i-1][-1]:
            g_list.append(list[i])
        else:
            pass
    return g_list





