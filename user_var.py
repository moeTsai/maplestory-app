import z_custom

#################################
#    Editable User Variables    #
#################################

########## EDIT HERE ##########
current_routines = {
    1: 'daemon_slime',
    2: 'ring',
}
routine_index = getattr(z_custom, 'routine_index', 1)


routine = current_routines[routine_index]


hp_percent_to_fill = 50

# if the routine is repetative
repetative = True


# disabled if repetative is True
repeat_times = 0


DEFAULT_CONFIG = z_custom.DEFAULT_CONFIG

LISTENER_CONFIG = z_custom.LISTENER_CONFIG
################################

# check if the BOT_TOKEN and CHAT_ID are set
BOT_TOKEN = getattr(z_custom, 'BOT_TOKEN', None)
CHAT_ID = getattr(z_custom, 'CHAT_ID', None)




