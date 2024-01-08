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

current_buffs = None

locked = False


# utils_game.py
# HP0_LOCATION = (262, 790)
# HP100_LOCATION = (360, 790)
HP0_LOCATION = None
HP100_LOCATION = None
HP_COLOR = None
HPs_X = None
HPs_Y = None
MP0_LOCATION = None
MP100_LOCATION = None
MP_COLOR = None
MPs_X = None
MPs_Y = None


last_buff_time = None


# Represents the current shortest path that the bot is taking
path = []







bot = None

# Shares the gui to all modules
gui = None
