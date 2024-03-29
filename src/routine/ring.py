"""automatic ring routine"""

import cv2
import time
from src.common import config, utils
from user_var import DEFAULT_CONFIG
from src.common.vkeys import press, click, key_down, key_up
from src.common.message import send_message_in_thread, send_photo_in_thread
from src.common.utils_game import reset_keys


cap = config.capture
bot = config.bot

attact = DEFAULT_CONFIG['Attack']
interact = DEFAULT_CONFIG['Interact']
buff1 = DEFAULT_CONFIG['Buff1']
buff2 = DEFAULT_CONFIG['Buff2']
tp = DEFAULT_CONFIG['Tp']
jump = DEFAULT_CONFIG['Jump']
heal = DEFAULT_CONFIG['Heal']
feed_pet = DEFAULT_CONFIG['Feed pet']

npc = cv2.imread('assets/routine/ring/npc.png', 0)
fight_req = cv2.imread('assets/routine/ring/fight_request.png', 0)
tomb = cv2.imread('assets/routine/ring/tomb.png', 0)
three = cv2.imread('assets/routine/ring/three.png', 0)
four = cv2.imread('assets/routine/ring/four.png', 0)

threshold = 0.98

BOT_TEMPLATE_LF = cv2.imread('assets/routine/ring/bot_lf.png', 0)
BOT_TEMPLATE_RT = cv2.imread('assets/routine/ring/bot_rt.png', 0)
HORSE_TEMPLATE_LF = cv2.imread('assets/routine/ring/horse_lf.png', 0)
HORSE_TEMPLATE_RT = cv2.imread('assets/routine/ring/horse_rt.png', 0)
SUMMON_TEMPLATE = cv2.imread('assets/routine/ring/summon_loc.png', 0)
TP_TEMPLATE = cv2.imread('assets/routine/ring/tp.png', 0)

REAL_PLAYER_TEMPLATE = cv2.imread('assets/routine/ring/real_player.png', 0)
is_alt = False
alt_has_died = False

## clear console
CURCOR_UP = '\033[1A'
CLEAR = '\x1b[1A'
CLEAR_LINE = CURCOR_UP + CLEAR



@utils.run_if_enabled
def _main():
    """
    automatic ring routine
    """

    frame = cap.frame
    if frame is None:
        print(' -  No frame captured')
        return
    
    entry()
    wait_for_request()
    times = 'infinite' if bot.repetative else bot.repeat_times
    message = f'Remaining {times} times'
    send_message_in_thread(message + ' (starts).')
    send_photo_in_thread(frame)
    fight()
    expfix()
    # alt_expfix()
    send_message_in_thread(message + ' (ends).')
    out()
    alt_out()
    time.sleep(1)


def expfix():
    print(' -  exp fixing...')
    time.sleep(0.3)
    press('enter', 1)
    time.sleep(0.3)
    press('up', 1)
    time.sleep(0.3)
    press('enter', 1)
    time.sleep(0.3)
    press('enter', 1)

def alt_expfix():
    switch_alt()
    expfix()
    switch_alt()

def threefour():
    three_pos = utils.multi_match(cap.frame, three, threshold=0.98)
    four_pos = utils.multi_match(cap.frame, four, threshold=0.98)
    if len(three_pos) > 0:
        return (three_pos[0][0] + cap.window['left'], three_pos[0][1] + cap.window['top'])
                
    if len(four_pos) > 0:
        return (four_pos[0][0] + cap.window['left'], four_pos[0][1] + cap.window['top'])

    return None

def find_image_console(image, message = 'waiting'):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    dot_num = 1
    count = 0
    first = True
    image_pos = utils.multi_match(cap.frame, image, threshold=threshold)
    while len(image_pos) == 0 and config.enabled:
        # if first:
        #     first = False
        # else:
        #     print(LINE_UP, end=LINE_CLEAR)
        image_pos = utils.multi_match(cap.frame, image, threshold=threshold)
        count += 1
        if count > 5:
            print(message + dot_num * '.')
            dot_num %= 5
            dot_num += 1
            count = 0
        time.sleep(0.1)
    
    return image_pos

def entry():
    global alt_has_died
    alt_has_died = False
    npc_pos = find_image_console(npc, message = ' -  finding npc')
        
    if not config.enabled:
        return

    print(f' -  npc detected at {npc_pos}')
    while True:
        click(npc_pos[0])
        time.sleep(2)
        pos = threefour()
        print(pos)
        if pos:
            click(pos)
            time.sleep(0.25)
            break
        press("Esc",1)
        time.sleep(0.25)

def wait_for_request():
    find_image_console(fight_req, message = ' -  finding request')
    
    if not config.enabled:
        return
    
    press(interact, 1)
    time.sleep(0.5)
    press(buff1, 2)
    time.sleep(0.5)
    press(buff2, 2)

    adding_ability(sec = 5)
    time.sleep(5)
    
    
def fight():
    # TODO
    entry_time = time.time()
    summon_time = time.time()
    dead_time = time.time()
    buff_time = None
    alt_time = None
    alt_time = time.time()
    pet_time = time.time()
    stop_after = 260

    while time.time() - entry_time < 601:
        if not config.enabled or config.locked:
            time.sleep(0.1)
            continue
        if alt_time is None:
            alt_time = time.time()
            # alt_inting()
        elif time.time() - dead_time > 10:
            dead_time = time.time()
            print(' -  dead checking...')
            if check_dead():
                buff_time = None
                print('buff time reset')
        # elif time.time() - alt_time > 60:
        #     alt_time = time.time()
        #     print(' -  active alt')
        #     key_up('left')
        #     alt_active()
        if time.time() - summon_time > 13:
            summon_time = time.time()
            print(' -  summoning...')
            summon()
        if not buff_time or time.time() - buff_time > 120:
            buff_time = time.time()
            print(' -  buffing...')
            time.sleep(0.5)
            press(buff2, 1)
            time.sleep(1)
            press(buff1, 1)
        
        if time.time() - pet_time > 300:
            pet_time = time.time()
            press(feed_pet, 1)
            print(f' - feeding...')
        
        if time.time() - entry_time < stop_after:
            attack_monster()
        time.sleep(0.01)
    # time.sleep(0.1)

def check_dead():
    global alt_has_died
    def walk_out(down = True, need_heal = True):
        print('...walking out...')
        time.sleep(2.5)
        key_up('left')
        key_down('right')
        count = 0
        while len(utils.multi_match(cap.frame, TP_TEMPLATE, threshold=threshold)) > 0 or count > 300:
            if count > 3000:
                break
            count += 1
            key_down('right')
            press('up', 1)
            time.sleep(0.01)
                
        key_up('right')
        if need_heal:
            switch_alt()
            time.sleep(0.3)
            press(heal, 2)
            time.sleep(0.3)
            press(heal, 2)
            switch_alt()
        if down:
            key_down('down')
            for _ in range(5):
                press(jump, 1)
                time.sleep(0.3)
            key_up('down')

        time.sleep(1)
    
    if not alt_has_died:
        switch_alt()
        time.sleep(0.5)
        dead_pos = utils.multi_match(cap.frame, tomb, threshold=threshold)
        if len(dead_pos) > 0:
            # print(' -  dead detected')
            alt_has_died = True
            print(' -  alt has died')
            dead_pos = dead_pos[0]
            click((cap.window['left'] + dead_pos[0] + 100, cap.window['top'] + dead_pos[1] + 65))    
            walk_out(down = False, need_heal = False)
        switch_alt()

    dead_pos = utils.multi_match(cap.frame, tomb, threshold=threshold)
    if len(dead_pos) > 0:
        dead_pos = dead_pos[0]
        click((cap.window['left'] + dead_pos[0] + 100, cap.window['top'] + dead_pos[1] + 65))
        walk_out(down = False, need_heal = alt_has_died)
        return True

def alt_walk():

    pass

def alt_inting():
    switch_alt()

    key_down('right')
    press(tp, 2)
    time.sleep(0.1)
    press(tp, 2)
    key_up('right')
    time.sleep(0.1)

    switch_alt()

def alt_active():
    switch_alt()
    press(attact, 2)
    time.sleep(0.1)
    press(attact, 2)
    switch_alt()

def alt_out():
    switch_alt()
    time.sleep(0.5)
    last_pos = None
    # again if it fails
    while True:
        # npc_pos[0] == (958, 586)
        npc_pos = utils.multi_match(cap.frame, npc, threshold=threshold)
        while len(npc_pos) == 0 and config.enabled:
            print(' -  finding npc...(out)')
            npc_pos = utils.multi_match(cap.frame, npc, threshold=threshold)
            time.sleep(0.1)

        
        if last_pos is None:
            last_pos = npc_pos[0]
        
        if npc_pos[0] != last_pos:
            break
        if not config.enabled:
            return
        
        adding_ability(sec = 3)

        print(f' -  npc detected at {npc_pos}')
        time.sleep(0.2)

        npc_pos = (npc_pos[0][0] + cap.window['left'], npc_pos[0][1] + cap.window['top'] + 10)
        click(npc_pos)
        time.sleep(0.5)
        press('enter', 1)
        time.sleep(0.2)

    switch_alt()

def attack_monster():
    player_pos = config.real_player_pos
    frame = cap.frame
    if frame is None:
        print(' -  No frame captured')
        return
    
    # bias = 20
    bot_lf = utils.multi_match(frame, BOT_TEMPLATE_LF, threshold=threshold)
    bot_rt = utils.multi_match(frame, BOT_TEMPLATE_RT, threshold=threshold)
    horse_lf = utils.multi_match(frame, HORSE_TEMPLATE_LF, threshold=threshold)
    horse_rt = utils.multi_match(frame, HORSE_TEMPLATE_RT, threshold=threshold)
    
    mons = bot_lf or bot_rt or horse_lf or horse_rt
    player = utils.multi_match(frame, REAL_PLAYER_TEMPLATE, threshold=threshold)
    if len(player) > 0:
        player_pos = player[0]
        print(f' -  Player detected at {player_pos}')
    else:
        print(' -  player not detected')
        return
    if len(mons) == 0:
        print(' -  No monsters detected')
        return

    next_mon_dir = find_next_monster(mons, player_pos)

    print(f' -  Next monster at player + {next_mon_dir}')

    # print(CLEAR_LINE * 2, end='')

    attact_monster(next_mon_dir)

def summon():
    # TODO
    summon_pos = utils.multi_match(cap.frame, SUMMON_TEMPLATE, threshold=threshold)
    if len(summon_pos) == 0:
        print(' -  No summon detected')
        return
    summon_pos = summon_pos[0]
    print(f' -  summon detected at {summon_pos}')
    monster_pos = (cap.window['left'] + summon_pos[0], cap.window['top'] + summon_pos[1]+ 43)
    skill_pos = (cap.window['left'] + summon_pos[0] + 70, cap.window['top'] + summon_pos[1] + 43)
    click(monster_pos)
    press('f5', 4)
    time.sleep(0.1)
    click(skill_pos)
    press('f7', 2)
    time.sleep(0.1)
    click(monster_pos)


def out():
    reset_keys(['left', 'right'])

    last_pos = None
    # again if it fails
    while True:
        npc_pos = utils.multi_match(cap.frame, npc, threshold=threshold)
        while len(npc_pos) == 0 and config.enabled:
            print(' -  finding npc...(out)')
            npc_pos = utils.multi_match(cap.frame, npc, threshold=threshold)
            time.sleep(0.1)
        
        if last_pos is None:
            last_pos = npc_pos[0]
        
        if npc_pos[0] != last_pos:
            break
        
        if not config.enabled:
            return

        print(f' -  npc detected at {npc_pos}')
        time.sleep(0.2)
        
        npc_pos = (npc_pos[0][0] + cap.window['left'], npc_pos[0][1] + cap.window['top'] + 10)
        click(npc_pos)
        time.sleep(0.5)
        press('enter', 1)
        time.sleep(0.2)



    

def attact_monster(direction_dist):
    """Attack the slime considering direction_dist."""

    too_far = 300
    facing = config.real_player_facing
    press(DEFAULT_CONFIG['Pick up'], 1)
    if direction_dist > too_far:
        key_down('right')
    elif direction_dist < -too_far:
        key_down('left')
    elif direction_dist > 0:
        reset_keys(['left', 'right'])
        if facing and facing != 'left':
            key_down('right')
            time.sleep(1)
            key_up('right')
            facing = 'right'
        press(attact, 2)
    else:
        reset_keys(['left', 'right'])
        if facing and facing != 'right':
            key_down('left')
            time.sleep(1)
            key_up('left')
            facing = 'left'
        press(attact, 2)
    time.sleep(0.01)

def find_next_monster(mons, player_pos):
    """Find the next slime to attack."""

    sweet_spot = 5

    px, _ = player_pos
    
    # retunr the closest slime's distance and direction to the player's +- sweet_spot
    closest_len = 9999
    closest_mon = None
    for mon in mons:
        sx, _ = mon
        if min(abs(sx - (px + sweet_spot)), abs(sx - (px + sweet_spot))) < closest_len:
            closest_mon = mon
            closest_len = min(abs(sx - (px + sweet_spot)), abs(sx - (px + sweet_spot)))

    # print(f' -  Closest slime at {closest_mon}')
    # print(f' -  Player at {player_pos}')
    return closest_mon[0] - player_pos[0]

def adding_ability(sec = 3):
    ABILITY = cv2.imread('assets/ability_adding/ability.png', 0)
    ability = utils.multi_match(cap.frame, ABILITY, threshold=0.99)
    if not ability:
        press(DEFAULT_CONFIG['Ability'], 1)
    time.sleep(sec)
    press(DEFAULT_CONFIG['Ability'], 1)

def switch_alt():
    global is_alt

    reset_keys(['left', 'right'])
    cap.switch_hwnd()
    time.sleep(0.1)
    left = cap.window['left']
    top = cap.window['top']
    if is_alt:
        is_alt = False
        click((left + 50, top + 40))
        time.sleep(0.05)
        click((left + 50, top + 40))
        time.sleep(0.02)
        click((left + 50, top + 40))
    else:
        is_alt = True
        click((left + 70, top + 766))
        time.sleep(0.05)
        click((left + 70, top + 766))
        time.sleep(0.02)
        click((left + 70, top + 766))

    
