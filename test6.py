import pyautogui
import cv2
import numpy as np
import pytesseract
import time
import os

p = pyautogui

# Create output directory if it doesn't exist
os.makedirs("test_images", exist_ok=True)

def get_text_from_title_region(x=0.19, y=0.92, w=0.5, h=0.05, trial=0):
    screen_size = p.size()
    #print(f"\nScreen size: {screen_size}")
    screen_x = screen_size[0]
    screen_y = screen_size[1]

    title_window_x = int(screen_x * x)
    title_window_y = int(screen_y * y)
    title_window_w = int(screen_x * w)
    title_window_h = int(screen_y * h)
    # print("title_window_x:", title_window_x)
    # print("title_window_y:", title_window_y)
    # print("title_window_w:", title_window_w)
    # print("title_window_h:", title_window_h)
    # print("")   

    try:
        screenshot = pyautogui.screenshot(region=(title_window_x, title_window_y, title_window_w, title_window_h))
        screenshot.save("netflix_title_raw.png")
        print("Screenshot saved as netflix_title_raw.png")
    except Exception as e:
        print("Error taking screenshot:", e)
        return None

    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Preprocessing: Isolate white text (Netflix titles are white)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold: Keep only very bright pixels (near-white text)
    # Use 240 threshold instead of 255 to account for compression/anti-aliasing
    _, binary = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
    
    # Optional: Remove small noise with morphological operations
    kernel = np.ones((2, 2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # Save preprocessed image for inspection
    cv2.imwrite(f"test_images/netflix_title_processed_{trial}.png", binary)
    print(f"Preprocessed image saved as test_images/netflix_title_processed_{trial}.png")
    
    # Use the preprocessed binary image for OCR
    img = binary
       
    custom_config = r'--psm 6 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:!?. ,\'"-'
    
    title_text = pytesseract.image_to_string(img, lang="eng", config=custom_config)
    
    # Post-process: Replace common OCR misreads
    title_text = title_text.replace('£', 'E')  # Pound symbol often misread as E
    title_text = title_text.replace('€', 'E')  # Euro symbol often misread as E
    title_text = title_text.replace('©', 'C')  # Copyright symbol often misread as C
    title_text = title_text.replace('™', 'TM') # Trademark symbol often misread as TM

    print("Extracted Title Text:", title_text)
    return title_text

def get_text_from_title_region_no_preprocessing(x=0.19, y=0.92, w=0.5, h=0.05, trial=0):
    screen_size = p.size()
    #print(f"\nScreen size: {screen_size}")
    screen_x = screen_size[0]
    screen_y = screen_size[1]

    title_window_x = int(screen_x * x)
    title_window_y = int(screen_y * y)
    title_window_w = int(screen_x * w)
    title_window_h = int(screen_y * h)
    # print("title_window_x:", title_window_x)
    # print("title_window_y:", title_window_y)
    # print("title_window_w:", title_window_w)
    # print("title_window_h:", title_window_h)
    # print("")   

    try:
        screenshot = pyautogui.screenshot(region=(title_window_x, title_window_y, title_window_w, title_window_h))
        screenshot.save(f"test_images/netflix_title_raw_no_preprocessing_{trial}.png")
        #print(f"Screenshot saved as netflix_title_raw_no_preprocessing_{trial}.png")
    except Exception as e:
        print("Error taking screenshot:", e)
        return None

    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
       
    custom_config = r'--psm 6 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:!?. ,\'"-'
    
    title_text = pytesseract.image_to_string(img, lang="eng", config=custom_config)

    print("Extracted Title Text (No Preprocessing):", title_text)
    return title_text

if __name__ == "__main__":
    trial = 0
    while True:
        result = get_text_from_title_region(trial=trial)
        result2 = get_text_from_title_region_no_preprocessing(trial=trial)
        print(f"\nFinal result:")
        print(f"\nRaw: {result}")
        print(f"\nPre: {result2}")
        trial += 1
        time.sleep(3)