import pyautogui
import time
import NetflixAutoRatings as ar
import ExtractTitle as et
import ShowRatingToast as t

# Netflix must be 100% scale for the images to be detected properly on 1920x1080 or 125% on 4k.

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

episodes_watched = 0
skipped_intros = 0

current_episode_number = ""
current_episode_rating = 0.0

print(f"Screen size: {screen_size}")
print("Automatically skipping intro and selecting next episode on Netflix!")

def move_center():
    p.moveTo(int(screen_x/2), int(screen_y/2), 0)

while True:
    if p.position().x > 1550 and p.position().y < 200 and current_episode_number != "" and current_episode_rating != 0.0:
        t.show_rating_toast(f"Episode {current_episode_number}", float(current_episode_rating), duration=1000)
        print("Displayed toast")

    # Select next episode button
    try:
        if screen_x >= 3840:
            next_episode_button_location = p.locateCenterOnScreen(r'next_episode4k.png', confidence=0.6)
        else:
            next_episode_button_location = p.locateCenterOnScreen(r'next_episode100percent.png', confidence=0.6)

        print("Locating next episode: " + str(next_episode_button_location))
        
        p.leftClick(next_episode_button_location)
        move_center()
        
        episodes_watched += 1
        print("Episodes watched: " + str(episodes_watched))

        current_episode_number = "" 
        current_episode_rating = 0.0
        
    except p.ImageNotFoundException:
        #print("Next episode button not on screen.")
        pass

    # Select skip intro button
    try:
        if screen_x >= 3840:
            skip_intro_button_location = p.locateCenterOnScreen(r'skip_intro4k125percent.png', confidence=0.8)
        else:
            skip_intro_button_location = p.locateCenterOnScreen(r'skip_intro100percent.png', confidence=0.8)

        print("Locating skip intro: "+ str(skip_intro_button_location))
        p.leftClick(skip_intro_button_location)
        move_center()
        skipped_intros += 1
        print("Intros skipped: " + str(skipped_intros))
        time.sleep(1)

        # Extract title and show rating toast
        title_tuple = et.get_text_from_title_region()
        print(title_tuple)
        if title_tuple[1] == "None" or title_tuple[1] == "":
            print("Could not extract title tuple. Probably not fullscreen. Trying maximized but not fullscreened.")
            title_tuple = et.get_text_from_title_region(y=0.87)

        episode_rating = ar.get_rating_by_episode("tt0388629", title_tuple[1])
        current_episode_number = title_tuple[1]
        current_episode_rating = episode_rating

        print(f"Episode Rating: {episode_rating}")

        try:
            t.show_rating_toast(f"Episode {current_episode_number}", float(current_episode_rating), duration=4000)
        except ValueError:
            print("Could not display rating toast due to invalid rating value.")
            try:
                t.show_rating_toast("", -1, duration=4000)
                print("Displayed error toast")
            except Exception as e:
                print(f"Could not display rating toast due to error: {e}")
        except Exception as e:
            print(f"Could not display rating toast due to error: {e}")

    except p.ImageNotFoundException:
        #print("Skip intro button not on screen.")
        pass
    
    time.sleep(0.5)

# One Piece parent tconst: tt0388629