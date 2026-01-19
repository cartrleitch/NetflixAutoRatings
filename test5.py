import pyautogui
import time
import NetflixAutoRatings as ar
import re

strip_string = ' "\'‘’“”()-_—=~`'

def extract_series_title(text):
    title_match = re.search(r'(.+)\bE\d{1,4}\b', text)
    if title_match:
        return title_match.group(1).strip(strip_string)
    return text.strip().strip(strip_string)

print(f"|{extract_series_title("\"\'one Piece E10 The Great Adventure")}|") # Example usage
print(f"|{extract_series_title("Stranger Things E3 Gay" )}|") # Example usage
print(f"|{extract_series_title("Breaking Bad E1 Pilot")}|") # Example usage
print(f"|{extract_series_title("—_ One Piece")}|") # Example usage