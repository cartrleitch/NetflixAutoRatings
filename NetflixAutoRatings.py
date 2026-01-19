import sys
import os
import DatasetCache as cache
import ShowRatingToast as t

episode_title = "I'm Luffy! The Man Who Will Become the Pirate King!"

ratings_dict, episodes_dict, series_dict, movies_dict = cache.load_cache()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_rating_by_episode_id(episode_id):
    return ratings_dict.get(episode_id, "Rating not found.")
     
def get_rating_by_title(title):
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

        if episode_title.lower() == primary_title.lower():
            print(title_id, primary_title)
            target_title_id = title_id
            break

    print("Retrieving average rating...")
    print (target_title_id)

    return get_rating_by_episode_id(target_title_id)
     
#print(f'Average rating for desired episode: {get_rating_by_title(episode_title)}')

def get_rating_by_episode(target_parent_id, target_episode_num):
    episode_id = episodes_dict.get((target_parent_id.lower(), str(target_episode_num)), "Episode ID not found.")
    print(episode_id)
    if episode_id == "Episode ID not found.":
        return "Episode ID not found."
    return ratings_dict.get(episode_id, "Rating not found.")
print(f'Average rating for desired episode: {get_rating_by_episode("tt11737520", "1")}')  # One Piece 

def get_series_id_by_title(series_title):
    # Use cached series_dict for instant lookup
    matches = series_dict.get(series_title.lower(), [])
    series_title = series_title.upper()
    
    if not matches:
        print(f'Series "{series_title}" not found in cache.')
        return ""
    
    # Handle one series with title
    if len(matches) == 1:
        series_id = matches[0][0]
        print(f'Series id: {series_id} for title "{series_title}" found.')
        return series_id
    
    filtered_matches = []
    for series in matches:
        series_id = series[0]
        series_year = series[1]
        rating = float(ratings_dict.get(series_id, 0))
        print (f'Checking series id: {series_id} year: {series_year} rating: {rating}')
        if rating == 0.0 or series_year == "0":
            print (f'Removing series id: {series_id} year: {series_year} rating: {rating}')
        else:
            filtered_matches.append(series)
    
    matches = filtered_matches

    if len(matches) == 1:
        series_id = matches[0][0]
        rating = ratings_dict.get(series_id, "Rating not found.")
        print(f'Series id: {series_id} for title "{series_title}" found with rating {rating}.')
        return series_id 

    # Handle multiple series with same title
    t.show_rating_toast(f'Multiple series found for title "{series_title}".\nPlease select the correct one in the console.', -2, duration=4000)
    print(f'Found {len(matches)} series with title "{series_title}":')
    match_selection = 1
    match_dict = {}

    print("Matches:")
    for series_id, year in matches:
        rating = float(ratings_dict.get(series_id, 0))
        match_dict[match_selection] = (series_id)
        print(f'{match_selection}: {series_title} ({year}): Rating {rating}')
        match_selection += 1

    try:
        match_user_choice = int(input("Type the number of the correct series: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        match_user_choice = int(input("Type the number of the correct series: "))
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
    target_series_id = match_dict.get(match_user_choice, "")

    return (target_series_id)
    
#print(get_series_id_by_title("One Piece")) # One Piece

def get_movie_rating_by_title(movie_title):
    matches = movies_dict.get(movie_title.lower(), [])
    print(matches)
    movie_title = movie_title.upper()

    if not matches:
        print(f'Movie "{movie_title}" not found in cache.')
        return None
    
    # Handle one movie with title
    if len(matches) == 1:
        movie_id = matches[0][0]
        rating = ratings_dict.get(movie_id, "Rating not found.")
        print(f'Movie id: {movie_id} for title "{movie_title}" found with rating {rating}.')
        return rating
    
    # Remove movies with no rating or year
    filtered_matches = []
    for movie in matches:
        movie_id = movie[0]
        movie_year = movie[1]
        rating = float(ratings_dict.get(movie_id, 0))
        print (f'Checking movie id: {movie_id} year: {movie_year} rating: {rating}')
        if rating == 0.0 or movie_year == "0":
            print (f'Removing movie id: {movie_id} year: {movie_year} rating: {rating}')
        else:
            filtered_matches.append(movie)
    
    matches = filtered_matches

    if len(matches) == 1:
        movie_id = matches[0][0]
        rating = ratings_dict.get(movie_id, "Rating not found.")
        print(f'Movie id: {movie_id} for title "{movie_title}" found with rating {rating}.')
        return rating
                   
    # Handle multiple movies with same title
    t.show_rating_toast(f'Multiple movies found for title "{movie_title}".\nPlease select the correct one in the console.', -2, duration=4000)
    print(f'Found {len(matches)} movies with title "{movie_title}":')
    match_selection = 1
    match_dict = {}

    print("Matches:")
    for movie in matches:
        movie_id = movie[0]
        movie_year = movie[1]
        rating = float(ratings_dict.get(movie_id, 0))
        match_dict[match_selection] = (movie_id)
        print(f'{match_selection}: {movie_title} ({movie_year}): Rating {rating}')
        match_selection += 1

    try:
        match_user_choice = int(input("Type the number of the correct movie: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        match_user_choice = int(input("Type the number of the correct movie: "))
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error."
    target_movie_id = match_dict.get(match_user_choice, "")
    rating = ratings_dict.get(target_movie_id, "Rating not found.")

    return rating

# print(get_movie_rating_by_title("ee aa")) # Inception
#print(ratings_dict.get("tt1375666", "Rating not found."))  # Inception