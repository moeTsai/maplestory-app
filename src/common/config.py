"""A collection of variables shared across multiple modules."""



#################################
#       Global Variables        #
#################################
# Describes whether the main bot loop is currently running or not
enabled = False

# Shares the video capture loop
capture = None


player_pos = None

real_player_pos = None

real_player_facing = None

locked = False


# Represents the current shortest path that the bot is taking
path = []







bot = None

# Shares the gui to all modules
gui = None
