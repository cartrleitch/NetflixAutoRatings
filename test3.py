import pyautogui
import time
import NetflixAutoRatings as ar

p = pyautogui

time.sleep(1)
screen_size = p.size()
print (f"Screen size: {screen_size}")
screen_x = screen_size[0]
screen_y = screen_size[1]

title_window_x = int(screen_x * 0.17)
title_window_y = int(screen_y * 0.87)
title_window_w = int(screen_x * 0.6)
title_window_h = int(screen_y * 0.05)

print("title_window_x:", title_window_x)
print("title_window_y:", title_window_y)
print("title_window_w:", title_window_w)
print("title_window_h:", title_window_h)

screenshot = pyautogui.screenshot(region=(title_window_x, title_window_y, title_window_w, title_window_h))
screenshot.save("netflix_title_raw_test.png")
print("Screenshot saved as netflix_title_raw_test.png")