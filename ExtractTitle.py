import pyautogui
import cv2
import numpy as np
import pytesseract
import re

p = pyautogui

p.FAILSAFE = True

p.pause = 1

def extract_episode_number(text):
    match = re.search(r'\bE(\d{1,4})\b', text)
    return int(match.group(1)) if match else None

def extract_title(text):
    title_match = re.search(r'\bE\d{1,4}\b\s*(.+)', text)
    if title_match:
        return title_match.group(1).strip()
    return text.strip()

def get_text_from_title_region(x=0.17, y=0.92, w=0.6, h=0.05):
    screen_size = p.size()
    print (f"Screen size: {screen_size}")
    screen_x = screen_size[0]
    screen_y = screen_size[1]

    title_window_x = int(screen_x * x)
    title_window_y = int(screen_y * y)
    title_window_w = int(screen_x * w)
    title_window_h = int(screen_y * h)
    print("title_window_x:", title_window_x)
    print("title_window_y:", title_window_y)
    print("title_window_w:", title_window_w)
    print("title_window_h:", title_window_h)

    try:
        screenshot = pyautogui.screenshot(region=(title_window_x, title_window_y, title_window_w, title_window_h))
        screenshot.save("netflix_title_raw.png")
        print("Screenshot saved as netflix_title_raw.png")
    except Exception as e:
        print("Error taking screenshot:", e)
        return None, None, None

    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # cv2.imshow("Post-Processed OCR Input", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
       
    custom_config = r'--psm 6 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:!?. ,\'"-'
    
    title_text = pytesseract.image_to_string(img, lang="eng", config=custom_config)

    print("Extracted Title Text:", title_text)

    episode_number = str(extract_episode_number(title_text))
    title = extract_title(title_text)
    print (f"Extracted Episode Number: |{episode_number}|")
    print (f"Extracted Title: |{title}|")
    
    return (title, episode_number, title_text)

if __name__ == "__main__":
    print(get_text_from_title_region())