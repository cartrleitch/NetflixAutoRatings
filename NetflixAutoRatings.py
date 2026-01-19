import sys
import os
import DatasetCache as cache

episode_title = "I'm Luffy! The Man Who Will Become the Pirate King!"

ratings_dict, episodes_dict, series_dict = cache.load_cache()

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
    if episode_id == "Episode ID not found.":
        return "Episode ID not found."
    return ratings_dict.get(episode_id, "Rating not found.")
# print(f'Average rating for desired episode: {get_rating_by_episode("tt0388629", "601")}')  # One Piece 

def get_series_id_by_title(series_title):
    try:
        titles = open(resource_path("title.basics.tsv"), "r", encoding="utf-8")
        target_series_id = ""
    except:
        return "Error."
    next(titles)  # Skip header line

    for title_line in titles:
        split_title_data = title_line.split("\t")
        title_id = split_title_data[0]
        title_type = split_title_data[1]
        primary_title = split_title_data[2].strip("\n ")

        if series_title.lower() == primary_title.lower() and title_type == "tvSeries":
            print(f'Series id: {title_id} for title {primary_title} found.')
            target_series_id = title_id
            break

    return target_series_id