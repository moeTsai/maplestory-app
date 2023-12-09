"""A collection of variables shared across multiple modules."""

# Describes whether the main bot loop is currently running or not
enabled = False

# Shares the video capture loop
capture = None


# Shares the gui to all modules
gui = None


# Represents the current shortest path that the bot is taking
path = []


player_pos = None