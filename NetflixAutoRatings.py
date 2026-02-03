import sys
import os
import DatasetCache as cache
import ShowRatingToast as t
from MyLogger import logger

episode_title = "I'm Luffy! The Man Who Will Become the Pirate King!"

ratings_dict, episodes_dict, series_dict, movies_dict, id_to_title_dict = cache.load_cache()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_rating_by_episode_id(episode_id):
    return ratings_dict.get(episode_id, "Rating not found.")
     
def get_rating_by_title(target_title):
    try:
        titles = open(resource_path("title.basics.tsv"), "r", encoding="utf-8")
        target_title_id = ""
    except:
        return "Error."
    next(titles)  # Skip header line

    for title_line in titles:
        split_title_data = title_line.split("\t")
        title_id = split_title_data[0]
        primary_title = split_title_data[2]

        if target_title.lower() == primary_title.lower():
            logger.debug(f"Found title match: {title_id} {primary_title}")
            target_title_id = title_id
            break

    logger.debug("Retrieving average rating...")
    logger.debug(f"Target title ID: {target_title_id}")

    return get_rating_by_episode_id(target_title_id)
     
def get_rating_by_episode(target_parent_id, target_episode_num, target_title=""):
    """Find episode rating, handling multiple seasons with same episode number"""
    episode_ids = episodes_dict.get((target_parent_id.lower(), str(target_episode_num)), None)
    logger.debug(f"Episode IDs found: {episode_ids}")
    
    if not episode_ids:
        logger.warning(f"Episode {target_episode_num} not found for series {target_parent_id}")
        return ("Episode ID not found.", "\\N")
    
    # Single episode found
    if len(episode_ids) == 1:
        episode_id = episode_ids[0][0]
        season_num = episode_ids[0][1]
        logger.debug(f"Found episode ID: {episode_id}")
        rating = ratings_dict.get(episode_id, None)
        return (rating if rating else "No rating", season_num)
    
    # Multiple seasons have this episode number, try to match by title if provided
    logger.info(f"Found {len(episode_ids)} episodes with number {target_episode_num}")
    
    # If target title provided, try to match it
    if target_title:
        for episode in episode_ids:
            episode_id = episode[0]
            season_num = episode[1]
            title = id_to_title_dict.get(episode_id, "")
            logger.debug(f'Checking episode ID: {episode_id} with title: "{title}" against target title: "{target_title}"')
            if target_title.lower() in title.lower():
                logger.info(f'Matched episode title: "{title}" with target title: "{target_title}"')
                rating = ratings_dict.get(episode_id, None)
                logger.debug(f'Found rating: {rating} for episode ID: {episode_id}')
                return (rating if rating else "No rating", season_num)
    
    # No title match found, return the highest rated episode with this number
    logger.info("No title match, returning highest rated episode")
    best_rating = 0.0
    best_episode = None
    for episode in episode_ids:
        episode_id = episode[0]
        season_num = episode[1]
        rating = ratings_dict.get(episode_id, None)
        if rating and float(rating) > best_rating:
            best_rating = float(rating)
            best_episode = (rating, season_num)
    
    if best_episode:
        return best_episode
    
    # If no ratings found, return first episode's data
    return ("No rating", episode_ids[0][1])

def get_series_id_by_title(series_title):
    # Use cached series_dict for instant lookup
    matches = series_dict.get(series_title.lower(), [])
    series_title = series_title.upper()
    
    if not matches:
        logger.warning(f'Series "{series_title}" not found in cache.')
        return ""
    
    # Handle one series with title
    if len(matches) == 1:
        series_id = matches[0][0]
        logger.info(f'Series id: {series_id} for title "{series_title}" found.')
        return series_id
    
    filtered_matches = []
    for series in matches:
        series_id = series[0]
        series_year = series[1]
        rating = float(ratings_dict.get(series_id, 0))
        logger.debug(f'Checking series id: {series_id} year: {series_year} rating: {rating}')
        if rating == 0.0 or series_year == "0":
            logger.debug(f'Removing series id: {series_id} year: {series_year} rating: {rating}')
        else:
            filtered_matches.append(series)
    
    matches = filtered_matches

    if len(matches) == 1:
        series_id = matches[0][0]
        rating = ratings_dict.get(series_id, "Rating not found.")
        logger.info(f'Series id: {series_id} for title "{series_title}" found with rating {rating}.')
        return series_id 

    # Handle multiple series with same title
    t.show_rating_toast(f'Multiple series found for title "{series_title}".\nPlease select in the popup.', -2, duration=4000)
    logger.info(f'Found {len(matches)} series with title "{series_title}":')
    
    # Build options for GUI dialog
    options = []
    for series_id, year in matches:
        rating = float(ratings_dict.get(series_id, 0))
        display_text = f"{series_title} ({year}): Rating {rating}"
        options.append((display_text, series_id))
        logger.debug(f'{series_title} ({year}): Series Rating {rating}')
    
    # Show GUI selection dialog
    target_series_id = t.show_selection_dialog(
        "Select Series",
        f'Multiple series found for "{series_title}".\nSelect the correct one:',
        options
    )
    
    if target_series_id:
        logger.info(f"User selected series ID: {target_series_id}")
        return target_series_id
    else:
        logger.info("User cancelled series selection")
        return ""
    
def get_movie_rating_by_title(movie_title):
    matches = movies_dict.get(movie_title.lower(), [])
    logger.debug(f"Movie matches: {matches}")
    movie_title = movie_title.upper()

    if not matches:
        logger.warning(f'Movie "{movie_title}" not found in cache.')
        return None
    
    # Handle one movie with title
    if len(matches) == 1:
        movie_id = matches[0][0]
        rating = ratings_dict.get(movie_id, "Rating not found.")
        logger.info(f'Movie id: {movie_id} for title "{movie_title}" found with rating {rating}.')
        return rating
    
    # Remove movies with no rating or year
    filtered_matches = []
    for movie in matches:
        movie_id = movie[0]
        movie_year = movie[1]
        rating = float(ratings_dict.get(movie_id, 0))
        logger.debug(f'Checking movie id: {movie_id} year: {movie_year} rating: {rating}')
        if rating == 0.0 or movie_year == "0":
            logger.debug(f'Removing movie id: {movie_id} year: {movie_year} rating: {rating}')
        else:
            filtered_matches.append(movie)
    
    matches = filtered_matches

    if len(matches) == 1:
        movie_id = matches[0][0]
        rating = ratings_dict.get(movie_id, "Rating not found.")
        print(f'Movie id: {movie_id} for title "{movie_title}" found with rating {rating}.')
        return rating
                   
    # Handle multiple movies with same title
    t.show_rating_toast(f'Multiple movies found for title "{movie_title}".\nPlease select in the popup.', -2, duration=4000)
    logger.info(f'Found {len(matches)} movies with title "{movie_title}":')
    
    # Build options for GUI dialog
    options = []
    for movie in matches:
        movie_id = movie[0]
        movie_year = movie[1]
        rating = float(ratings_dict.get(movie_id, 0))
        display_text = f"{movie_title} ({movie_year}): Rating {rating}"
        options.append((display_text, movie_id))
        logger.debug(f'{movie_title} ({movie_year}): Rating {rating}')
    
    # Show GUI selection dialog
    target_movie_id = t.show_selection_dialog(
        "Select Movie",
        f'Multiple movies found for "{movie_title}".\nSelect the correct one:',
        options
    )
    
    if target_movie_id:
        rating = ratings_dict.get(target_movie_id, "Rating not found.")
        logger.info(f"User selected movie ID: {target_movie_id} with rating {rating}")
        return rating
    else:
        logger.info("User cancelled movie selection")
        return None

if __name__ == "__main__":
    pass
    # print(get_rating_by_episode("tt0903747", "2", "Grilled"))
    # print(get_movie_rating_by_title("Superman")) # Inception
    # print(get_series_id_by_title("One Piece")) # One Piece
    # print(f'Average rating for desired episode: {get_rating_by_episode("tt11737520", "1")}')  # One Piece 
    # print(f'Average rating for desired episode: {get_rating_by_title}