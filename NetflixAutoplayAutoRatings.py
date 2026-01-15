import pyautogui
import time
import NetflixAutoRatings as ar
import ExtractTitle as et
import ShowRatingToast as t

# Netflix must be 100% scale for the images to be detected properly.

p = pyautogui

p.FAILSAFE = True

p.pause = 1

screen_size = p.size()
screen_x = screen_size[0]
screen_y = screen_size[1]

title_window_x = int(screen_x * 0.05)
title_window_y = int(screen_y * 0.06)
title_window_w = int(screen_x * 0.5)
title_window_h = int(screen_y * 0.14)

next_episodes = 0
skipped_intros = 0

print(f"Screen size: {screen_size}")
print("Automatically skipping intro and selecting next episode on Netflix!")

def move_center():
    p.moveTo(int(screen_x/2), int(screen_y/2), 0)

while True:
    # Select next episode button
    try:
        next_episode_button_location = p.locateCenterOnScreen(r'next_episode100percent.png', confidence=0.5)
        print("Locating next episode: " + str(next_episode_button_location))
        p.leftClick(next_episode_button_location)
        move_center()
        next_episodes += 1
        print("Next epsiodes selected: " + str(next_episodes))
        
    except p.ImageNotFoundException:
        #print("Next episode button not on screen.")
        pass

    # Select skip intro button
    try:
        skip_intro_button_location = p.locateCenterOnScreen(r'skip_intro100percent.png', confidence=0.8)
        print("Locating skip intro: "+ str(skip_intro_button_location))
        p.leftClick(skip_intro_button_location)
        move_center()
        skipped_intros += 1
        print("Intros skipped: " + str(skipped_intros))
        time.sleep(1)
        title_tuple = et.get_text_from_title_region()
        print(title_tuple)
        episode_rating = ar.get_rating_by_episode("tt0388629", title_tuple[1])
        print(f"Episode Rating: {episode_rating}")
        t.show_rating_toast(f"Episode {title_tuple[1]}", float(episode_rating), duration=4000)

    except p.ImageNotFoundException:
        #print("Skip intro button not on screen.")
        pass
    
    time.sleep(0.5)

# One Piece parent tconst: tt0388629