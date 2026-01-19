import pyautogui
import time
import sys
import os
import NetflixAutoRatings as ar
import ExtractTitle as et
import ShowRatingToast as t

# Netflix must be 100% scale for the images to be detected properly on 1920x1080 or 125% on 4k.

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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
skipped_recaps = 0

current_episode_number = ""
current_episode_rating = 0.0
cached_series_title = ""
cached_movie_title = ""
cached_movie_rating = 0.0
in_hover_area = False

episodes_watched_ratings = {}

series_id = ""

print(f"Screen size: {screen_size}")
print("Automatically skipping intro and selecting next episode on Netflix!")

def move_center():
    p.moveTo(int(screen_x/2), int(screen_y/2), 0)

def get_episode_rating_and_number():
    global cached_series_title, series_id, cached_movie_title, cached_movie_rating
    title_tuple = ("None", "None", "None", "None")  # (episode_number, episode_rating, title_text, series_title)

    # Extract title region text, try different regions if needed
    fscr_title_tuple = et.get_text_from_title_region()
    title_tuple = fscr_title_tuple
    print(fscr_title_tuple)

    # If no episode number found, try different region
    if fscr_title_tuple[1] == "None" or fscr_title_tuple[1] == "":
        print("\n <- Could not extract title tuple. Probably not fullscreen. Trying maximized but not fullscreened.")
        title_tuple = et.get_text_from_title_region(y=0.87)

        # If still no episode number found, probably a movie. Search movie title only in movie dataset
        if title_tuple[1] == "None" or title_tuple[1] == "":
            print("\nCould not find episode number. Probably a movie. Searching for title only.")
            movie_title = fscr_title_tuple[2].strip("\n ")
            
            # Check if movie title is cached
            if cached_movie_title == movie_title and cached_movie_rating != 0.0:
                print(f"Using cached movie rating for '{movie_title}'")
                return ("Movie", str(cached_movie_rating))
            
            movie_rating = ar.get_movie_rating_by_title(movie_title)
            # If still None, try in maximized but not fullscreened
            if movie_rating is None:
                print("\nCould not extract title tuple. Probably not fullscreen. Trying maximized but not fullscreened.")
                movie_title = title_tuple[2].strip("\n ")
                
                # Check cache again with new title
                if cached_movie_title == movie_title and cached_movie_rating != 0.0:
                    print(f"Using cached movie rating for '{movie_title}'")
                    return ("Movie", str(cached_movie_rating))
                    
                movie_rating = ar.get_movie_rating_by_title(movie_title)
            
            # Cache the movie data
            cached_movie_title = movie_title
            cached_movie_rating = movie_rating
            return ("Movie", str(movie_rating))

    # If this session has a saved series title, and it is the same as the current series, use that ID; if not, look it up
    current_series_title = title_tuple[3]
    # If we don't have a cached series title yet, get it
    if cached_series_title == "":
        cached_series_title = title_tuple[3]
        series_id = ar.get_series_id_by_title(current_series_title)

    # Get series ID by series title if different from cached
    if cached_series_title == current_series_title:
        print(f"Using cached series ID for title: {current_series_title}")
    else:
        cached_series_title = current_series_title
        series_id = ar.get_series_id_by_title(current_series_title)

    # Get episode rating by series ID and episode number
    print(series_id, title_tuple[1])
    episode_rating = ar.get_rating_by_episode(series_id, title_tuple[1])

    return (title_tuple[1], episode_rating)
try: 
    while True:
        mouse_in_hover = p.position().x > screen_x*0.8 and p.position().x < screen_x and p.position().y < screen_y*0.18 and p.position().y > 0 
        
        if mouse_in_hover and not in_hover_area:
            # Always extract to check if series changed
            print("Extracting episode number and rating for hover toast...")
            current_episode_number, current_episode_rating = get_episode_rating_and_number()
            try:
                if current_episode_number == "Movie":
                    t.show_rating_toast("Movie", float(current_episode_rating), 0)
                else:
                    t.show_rating_toast(f"Episode {current_episode_number}", float(current_episode_rating), 0)
                in_hover_area = True
                print("Displayed toast")
            except Exception as e:
                print(f"Could not display rating toast due to error: {e}")
        elif not mouse_in_hover and in_hover_area:
            print("Closing toast")
            t.close_rating_toast()
            in_hover_area = False
            # Clear cached episode data when leaving hover area to force fresh check next time
            current_episode_number = ""
            current_episode_rating = 0.0
        
        # Update toast window if it exists
        t.update_toast()

        # Select next episode button
        try:
            if screen_x >= 3840:
                next_episode_button_location = p.locateCenterOnScreen(resource_path('next_episode4k125percent.png'), confidence=0.6)
            else:
                next_episode_button_location = p.locateCenterOnScreen(resource_path('next_episode100percent.png'), confidence=0.6)

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
                skip_intro_button_location = p.locateCenterOnScreen(resource_path('skip_intro4k125percent.png'), confidence=0.8)
            else:
                skip_intro_button_location = p.locateCenterOnScreen(resource_path('skip_intro100percent.png'), confidence=0.8)

            print("Locating skip intro: "+ str(skip_intro_button_location))
            p.leftClick(skip_intro_button_location)
            move_center()
            skipped_intros += 1
            print("Intros skipped: " + str(skipped_intros))
            time.sleep(1)

            # Extract title and show rating toast
            current_episode_number, current_episode_rating = get_episode_rating_and_number()

            print(f"Episode Rating: {current_episode_rating}")
            episodes_watched_ratings[current_episode_number] = float(current_episode_rating)

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

        # Skip recap button
        try:
            if screen_x >= 3840:
                skip_recap_button_location = p.locateCenterOnScreen(resource_path('skip_recap4k125percent.png'), confidence=0.8)
            else:
                skip_recap_button_location = p.locateCenterOnScreen(resource_path('skip_recap100percent.png'), confidence=0.8)
            print("Locating skip recap: "+ str(skip_recap_button_location))
            p.leftClick(skip_recap_button_location)
            move_center()
            skipped_recaps += 1
            print("Recaps skipped: " + str(skipped_recaps))
            time.sleep(1)
        except:
            #print("Skip recap button not on screen.")
            pass

        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nExiting Netflix Autoplay Auto Ratings script.")
except Exception as e:
    print(f"\nProgram Ended Unexpectedly: {e}")
finally:
    t.close_rating_toast()

    episodes_watched_ratings_list = ""
    for episode, rating in episodes_watched_ratings.items():
        episodes_watched_ratings_list += f"\nEpisode {episode}: Rating {rating}"
        
    print(f"\nTotal episodes watched: {episodes_watched}\nTotal intros skipped: {skipped_intros}\nTotal recaps skipped: {skipped_recaps}\nEpisodes Watched Ratings: {episodes_watched_ratings_list}\nAverage Rating: {sum(episodes_watched_ratings.values())/len(episodes_watched_ratings) if episodes_watched_ratings else 0}")
# One Piece parent tconst: tt0388629