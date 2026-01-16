import sys
import os

episode_title = "I'm Luffy! The Man Who Will Become the Pirate King!"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_rating_by_episode_id(episode_id):
    try:
        ratings = open(resource_path("title.ratings.tsv"), "r", encoding="utf-8")
    except:
        return "Error."
    next(ratings)  # Skip header line

    for rating_line in ratings:
        split_rating_data = rating_line.split("\t")
        rating_title_id = split_rating_data[0]
        average_rating = split_rating_data[1]

        if episode_id == rating_title_id:
                rating_line = f"Episode ID {episode_id} has an average rating of {average_rating}."
                return average_rating
     
    return "Rating not found."

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
    try:
        episodes = open(resource_path("title.episode.tsv"), "r", encoding="utf-8")
    except:
        return "Error."
    next(episodes) # Skip header line

    for episode_line in episodes:
        split_episode_data = episode_line.split("\t")
        episode_num = split_episode_data[3].strip()
        parent_id = split_episode_data[1].lower()
    
        if target_parent_id.lower() == parent_id and target_episode_num == episode_num:
            episode_id = split_episode_data[0]
            print(f'Episode id: {episode_id} for episode number {episode_num} found. Parent id: {parent_id}')
            return get_rating_by_episode_id(episode_id)
            
    return "Rating not found." 

# print(f'Average rating for desired episode: {get_rating_by_episode("tt0388629", "601")}')  # One Piece 