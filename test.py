import ctypes

# 定義所需的 Windows API
user32 = ctypes.WinDLL('user32', use_last_error=True)

# 獲取當前線程的輸入法句柄
hkl = user32.GetKeyboardLayout(0)

# 輸出輸入法句柄
print(hkl)

# 如果需要更具體的信息，比如輸入法的語言代碼，可以進一步處理 hkl
lang_id = hkl & 0xffff
print(f'Language ID: {lang_id:#04x}')

# 可以將語言 ID 轉換為具體的語言代碼，比如英文是 0x0409，中文是 0x0804 等
 