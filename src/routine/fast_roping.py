# 如果同時按上與跳，即執行重複動作，如放開就取消

from src.common.vkeys import press, click, key_down, key_up
from src.common.utils_game import reset_keys

import keyboard as kb
import time

def perform_repeated_action():
    """執行重複動作的函數"""
    press('right', 1, down_time=0.08, up_time=0.02)
    press('left', 1, down_time=0.08, up_time=0.02)

def _main():
    """主要的監聽迴圈"""
    while True:
        
        if kb.is_pressed('up') and kb.is_pressed('space'):
            perform_repeated_action()
        else:
            # 如果放開任一按鍵，暫停動作
            time.sleep(0.01)
