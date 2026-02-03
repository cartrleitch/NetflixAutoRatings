import pyautogui
import time
import sys
import os
import logging
import NetflixAutoRatings as ar
import ExtractTitle as et
import ShowRatingToast as t
from MyLogger import logger

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
is_4k = screen_x >= 3840

episodes_watched = 0
skipped_intros = 0
skipped_recaps = 0

current_episode_number = ""
current_episode_rating = 0.0
cached_series_title = ""
cached_movie_title = ""
cached_movie_rating = 0.0
in_hover_area = False

watched_statistics = {}

series_id = ""

logger.info(f"Screen size: {screen_size}")
logger.info("Automatically skipping intro and selecting next episode on Netflix!")

def move_center():
    p.moveTo(int(screen_x/2), int(screen_y/2), 0)

def locate_button(button_name, confidence=0.8):
    """Locate a button image on screen based on resolution"""
    suffix = '4k125percent' if is_4k else '100percent'
    return p.locateCenterOnScreen(resource_path(f'{button_name}{suffix}.png'), confidence=confidence)

def handle_movie_rating(fscr_movie_title, maximized_movie_title):
    global cached_movie_title, cached_movie_rating
    movie_title = fscr_movie_title

    # Check if movie title is cached
    if cached_movie_title.lower() == movie_title.lower() and cached_movie_rating != 0.0:
        logger.debug(f"Using cached movie rating for '{movie_title}'")
        return ("Movie", str(cached_movie_rating), "\\N")
    
    movie_rating = ar.get_movie_rating_by_title(movie_title)
    # If still None, try in maximized but not fullscreened
    if movie_rating is None:
        logger.warning("Could not extract title tuple. Probably not fullscreen. Trying maximized but not fullscreened.")
        movie_title = maximized_movie_title
        # Check cache again with new title
        if cached_movie_title.lower() == movie_title.lower() and cached_movie_rating != 0.0:
            logger.debug(f"Using cached movie rating for '{movie_title}'")
            return ("Movie", str(cached_movie_rating), "\\N")    
        movie_rating = ar.get_movie_rating_by_title(movie_title)

    # Cache the movie data
    cached_movie_title = movie_title.upper()
    cached_movie_rating = movie_rating if movie_rating else 0.0
    return ("Movie", str(movie_rating), "\\N")

def get_episode_rating_and_number():
    global cached_series_title, series_id, cached_movie_title, cached_movie_rating
    title_tuple = ("None", "None", "None", "None")  # (episode_number, episode_rating, title_text, series_title)

    # Extract title region text, try different regions if needed
    fscr_title_tuple = et.get_text_from_title_region()
    title_tuple = fscr_title_tuple
    logger.debug(f"Extracted title tuple: {fscr_title_tuple}")

    # If no episode number found, try different region
    if fscr_title_tuple[1] == "None" or fscr_title_tuple[1] == "":
        logger.warning("Could not extract title tuple. Probably not fullscreen. Trying maximized but not fullscreened.")
        title_tuple = et.get_text_from_title_region(y=0.87)

        # If still no episode number found, probably a movie. Search movie title only in movie dataset
        if title_tuple[1] == "None" or title_tuple[1] == "":
            logger.info("Could not find episode number. Probably a movie. Searching for title only.")
            logger.debug(f"Extracted movie data: {fscr_title_tuple}")
            return handle_movie_rating(fscr_title_tuple[2].strip("\n "), title_tuple[2].strip("\n "))

    # If this session has a saved series title, and it is the same as the current series, use that ID; if not, look it up
    current_series_title = title_tuple[3]
    # If we don't have a cached series title yet, get it
    if cached_series_title == "":
        logger.info(f"First time seeing series: {current_series_title}")
        cached_series_title = title_tuple[3].upper()
        series_id = ar.get_series_id_by_title(current_series_title)
    # Get series ID by series title if different from cached
    elif cached_series_title == current_series_title.upper():
        logger.debug(f"Using cached series ID '{series_id}' for title: {current_series_title}")
    else:
        logger.info(f"Series changed from '{cached_series_title}' to '{current_series_title}'")
        cached_series_title = current_series_title.upper()
        series_id = ar.get_series_id_by_title(current_series_title)

    # Get episode rating by series ID and episode number
    episode_num = title_tuple[1]
    episode_title = title_tuple[0] 
    logger.debug(f"Getting rating for Series ID: {series_id}, Episode Number: {episode_num}, Episode Title: {episode_title}")
    episode_rating, season_num = ar.get_rating_by_episode(series_id, episode_num, episode_title)

    return (episode_num, episode_rating, season_num)

# Main loop
try: 
    while True:
        mouse_in_hover = p.position().x > screen_x*0.8 and p.position().x < screen_x and p.position().y < screen_y*0.18 and p.position().y > 0 
        
        if mouse_in_hover and not in_hover_area:
            # Always extract to check if series changed
            logger.debug("Extracting episode number and rating for hover toast...")
            current_episode_number, current_episode_rating, current_episode_season = get_episode_rating_and_number()
            try:
                if current_episode_number == "Movie":
                    t.show_rating_toast("Movie", float(current_episode_rating), 0)
                    watched_statistics[cached_movie_title] = (cached_movie_title, cached_movie_rating, "Movie")
                    logger.debug("Displayed movie toast")

                else:
                    logger.debug(f"Current episode season: {current_episode_season}")
                    if current_episode_season != "\\N":
                        t.show_rating_toast(f"S{current_episode_season}E{current_episode_number}", float(current_episode_rating), 0)
                        watched_statistics[cached_series_title] = (cached_series_title, current_episode_rating, f"S{current_episode_season}E{current_episode_number}")
                        logger.debug("Displayed episode toast")

                    else:
                        t.show_rating_toast(f"Episode {current_episode_number}", float(current_episode_rating), 0)
                        watched_statistics[cached_series_title] = (cached_series_title, current_episode_rating, f"E{current_episode_number}")
                        logger.debug("Displayed episode toast")

                in_hover_area = True
                logger.debug("Displayed toast")
            except Exception as e:
                logger.error(f"Could not display rating toast due to error: {e}")
        elif not mouse_in_hover and in_hover_area:
            logger.debug("Closing toast")
            t.close_rating_toast()
            in_hover_area = False
            # Clear cached episode data when leaving hover area to force fresh check next time
            current_episode_number = ""
            current_episode_rating = 0.0
        
        # Update toast window if it exists
        t.update_toast()

        # Select next episode button
        try:
            next_episode_button_location = locate_button('next_episode', confidence=0.6)
            logger.info(f"Found next episode button at: {next_episode_button_location}")
            p.leftClick(next_episode_button_location)
            move_center()
            current_episode_number = "" 
            current_episode_rating = 0.0
        except p.ImageNotFoundException:
            pass

        # Select skip intro button
        try:
            skip_intro_button_location = locate_button('skip_intro')
            logger.info(f"Found skip intro button at: {skip_intro_button_location}")
            p.leftClick(skip_intro_button_location)
            move_center()
            skipped_intros += 1
            logger.info(f"Intros skipped: {skipped_intros}")
            time.sleep(1.25)

            # Extract title and show rating toast
            current_episode_number, current_episode_rating, current_episode_season = get_episode_rating_and_number()
            logger.info(f"Episode Rating: {current_episode_rating}")
            watched_statistics[cached_series_title] = (cached_series_title, current_episode_rating, f"S{current_episode_season}E{current_episode_number}" if current_episode_season != "\\N" else f"E{current_episode_number}")

            try:
                if current_episode_season != "\\N":
                    t.show_rating_toast(f"S{current_episode_season}E{current_episode_number}", float(current_episode_rating), duration=4000)
                else:
                    t.show_rating_toast(f"Episode {current_episode_number}", float(current_episode_rating), duration=4000)
            except (ValueError, Exception) as e:
                logger.error(f"Could not display rating toast: {e}")
                try:
                    t.show_rating_toast("", -1, duration=4000)
                except Exception as e2:
                    logger.error(f"Error showing error toast: {e2}")
        except p.ImageNotFoundException:
            pass

        # Skip recap button
        try:
            skip_recap_button_location = locate_button('skip_recap')
            logger.info(f"Found skip recap button at: {skip_recap_button_location}")
            p.leftClick(skip_recap_button_location)
            move_center()
            skipped_recaps += 1
            logger.info(f"Recaps skipped: {skipped_recaps}")
            time.sleep(1)
        except p.ImageNotFoundException:
            pass

        time.sleep(0.5)
except KeyboardInterrupt:
    logger.info("Exiting Netflix Autoplay Auto Ratings script.")
except Exception as e:
    logger.error(f"Program Ended Unexpectedly: {e}")
finally:
    try:
        t.close_rating_toast()
    except Exception as e:
        logger.error(f"Error closing rating toast: {e}")

    # Print session statistics
    session_statistics = f"\n{'='*50}\nSESSION STATISTICS - {time.strftime("%m-%d-%Y %H:%M:%S", time.localtime())}\n{'='*50}\nEpisodes watched: {skipped_intros}\nRecaps skipped: {skipped_recaps}"

    if watched_statistics:
        session_statistics += f"\nWatched:"
        for value in watched_statistics.values():
            session_statistics += f"\n   {value[0]} - {value[2]}: Rating {value[1]}"
        avg_rating = sum(float(rating) for _, rating, _ in watched_statistics.values()) / len(watched_statistics)
        session_statistics += f"\n\nAverage Rating of Watched Episodes: {avg_rating:.1f}"
    session_statistics += f"\n{'='*50}\n"
    print(session_statistics)

    with open("Netflix_Session_Statistics.txt", "a", encoding="utf-8") as stats_file:
        stats_file.write(session_statistics)
        
    logger.info("Session statistics saved to Netflix_Session_Statistics.txt")
    
    os._exit(0)