"""import ctypes

# 定義所需的 Windows API
user32 = ctypes.WinDLL('user32', use_last_error=True)

# 獲取當前線程的輸入法句柄
hkl = user32.GetKeyboardLayout(0)

# 輸出輸入法句柄
print(hkl)

# 如果需要更具體的信息，比如輸入法的語言代碼，可以進一步處理 hkl
lang_id = hkl & 0xffff
print(f'Language ID: {lang_id:#04x}')

if lang_id == 0x0404:
    print(1)
    user32.LoadKeyboardLayoutW("00000409", 1)"""

# 可以將語言 ID 轉換為具體的語言代碼，比如英文是 0x0409，中文是 0x0804 等

# import win32api
# import win32con
# # import win32gui
# import ctypes

# def get_keyboard_layout():
#     # hwnd = win32gui.GetForegroundWindow()
#     user32 = ctypes.WinDLL('user32', use_last_error=True)
#     hwnd = user32.GetForegroundWindow()
#     thread_id = win32api.GetWindowThreadProcessId(hwnd)[0]
#     print(thread_id)
#     keyboard_layout = win32api.GetKeyboardLayout(thread_id)
#     return keyboard_layout

# layout = get_keyboard_layout()
# print(hex(layout))


# import win32api
# import win32process
# import win32gui

# def get_keyboard_layout():
#     hwnd = win32gui.GetForegroundWindow()
#     thread_id = win32process.GetWindowThreadProcessId(hwnd)[0]
#     # thread_id = win32gui.GetWindowThreadProcessId(hwnd)[0]  # 修改這一行
#     keyboard_layout = win32api.GetKeyboardLayout(thread_id)
#     return keyboard_layout

# layout = get_keyboard_layout()
# print(hex(layout))



# import ctypes

# # Load the User32 DLL
# user32 = ctypes.WinDLL('user32', use_last_error=True)

# # The layout code, e.g., '00000409' for English (US)
# layout = '00000409'
# layout = '0x409'

# # Load the keyboard layout
# result = user32.LoadKeyboardLayoutW(layout, 1)

# if result == 0:
#     raise ctypes.WinError(ctypes.get_last_error())

# print(f'Keyboard layout changed to {layout} for this process.')

import win32api

# Function to change the keyboard layout
def change_keyboard_layout():
    # Load the keyboard layout
    # result = user32.LoadKeyboardLayoutW(layout, 1)
    # from src.common.vkeys import press, key_down, key_up
    import pydirectinput as p_in
    import time

    def get_keyboard_layouts_windows():
        # Get the list of installed keyboard layouts
        layouts = win32api.GetKeyboardLayoutList()
        layout_ids = [hex(layout & 0xFFFF) for layout in layouts]
        return layout_ids

    layouts = get_keyboard_layouts_windows()

    # print(len(layouts))
    if len(layouts) == 1:
        print('Only one keyboard layout installed. So does not change the layout.')
        return
    current_layout = get_current_keyboard_layout()
    
    
# Get and print the current layout
    if current_layout == '0x409':
        print(f'Current keyboard layout: {current_layout} (English US)')
        return
    elif current_layout == '0x404':
        print(f'Current keyboard layout: {current_layout} (Chinese)')
        print(f'changing to English US')
        # window + space
        time.sleep(2)
        # key_down('win')
        # time.sleep(0.1)
        # press('space', 1)
        # time.sleep(0.1)
        # key_up('win')
        
        p_in.keyDown('winleft')
        time.sleep(0.3)
        p_in.press('space')
        time.sleep(0.3)
        p_in.keyUp('winleft')
        return
    print(f'Keyboard layout attempted to change to English US.')

# Function to get the current keyboard layout
def get_current_keyboard_layout():
    # Get the current thread ID
    
    import ctypes

    # Load the User32 DLL
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    thread_id = win32api.GetCurrentThreadId()
    # Get the keyboard layout for the thread
    layout = user32.GetKeyboardLayout(thread_id)
    return hex(layout & 0xFFFF)

# Change to a specific layout (e.g., '00000409' for English US)
change_keyboard_layout()
