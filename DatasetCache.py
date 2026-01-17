import pickle
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def build_ratings_dict():
    """Build dictionary: {episode_id: rating}"""
    print("Building ratings dictionary from TSV...")
    ratings_dict = {}
    
    with open(resource_path("title.ratings.tsv"), "r", encoding="utf-8") as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                title_id = parts[0]
                rating = parts[1]
                ratings_dict[title_id] = rating
    
    print(f"Loaded {len(ratings_dict)} ratings")
    return ratings_dict

def build_episodes_dict():
    """Build dictionary: {(parent_id, episode_num): episode_id}"""
    print("Building episodes dictionary from TSV...")
    episodes_dict = {}
    
    with open(resource_path("title.episode.tsv"), "r", encoding="utf-8") as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 4:
                episode_id = parts[0]
                parent_id = parts[1].lower()
                episode_num = parts[3].strip()
                episodes_dict[(parent_id, episode_num)] = episode_id
    
    print(f"Loaded {len(episodes_dict)} episodes")
    return episodes_dict

def build_series_dict():
    """Build dictionary: {series_title.lower(): series_id}"""
    print("Building series dictionary from TSV...")
    series_dict = {}
    
    with open(resource_path("title.basics.tsv"), "r", encoding="utf-8") as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                title_id = parts[0]
                title_type = parts[1]
                primary_title = parts[2]
                
                if title_type == "tvSeries":
                    series_dict[primary_title.lower()] = title_id
    
    print(f"Loaded {len(series_dict)} TV series")
    return series_dict

def save_cache():
    """Build and save all dictionaries to pickle files"""
    print("\n=== Building dataset cache ===")
    
    ratings = build_ratings_dict()
    with open("cache_ratings.pkl", "wb") as f:
        pickle.dump(ratings, f)
    print("Saved cache_ratings.pkl")
    
    episodes = build_episodes_dict()
    with open("cache_episodes.pkl", "wb") as f:
        pickle.dump(episodes, f)
    print("Saved cache_episodes.pkl")
    
    series = build_series_dict()
    with open("cache_series.pkl", "wb") as f:
        pickle.dump(series, f)
    print("Saved cache_series.pkl")
    
    print("=== Cache build complete ===\n")

def load_cache():
    """Load dictionaries from pickle files, or build if they don't exist"""
    cache_files = ["cache_ratings.pkl", "cache_episodes.pkl", "cache_series.pkl"]
    
    # Check if all cache files exist
    if not all(os.path.exists(f) for f in cache_files):
        print("Cache files not found. Building cache...")
        save_cache()
    
    print("Loading cache from pickle files...")
    
    with open("cache_ratings.pkl", "rb") as f:
        ratings_dict = pickle.load(f)
    
    with open("cache_episodes.pkl", "rb") as f:
        episodes_dict = pickle.load(f)
    
    with open("cache_series.pkl", "rb") as f:
        series_dict = pickle.load(f)
    
    print(f"Cache loaded: {len(ratings_dict)} ratings, {len(episodes_dict)} episodes, {len(series_dict)} series\n")
    
    return ratings_dict, episodes_dict, series_dict

def rebuild_cache():
    """Force rebuild of cache files"""
    print("Rebuilding cache from TSV files...")
    save_cache()

if __name__ == "__main__":
    # Test: build or load cache
    ratings, episodes, series = load_cache()
    
    # Test lookups
    print("\nTesting lookups:")
    print(f"One Piece series ID: {series.get('one piece', 'Not found')}")
    print(f"Episode (tt0388629, 610): {episodes.get(('tt0388629', '610'), 'Not found')}")
    
    episode_id = episodes.get(('tt0388629', '610'), None)
    if episode_id:
        print(f"Rating for episode {episode_id}: {ratings.get(episode_id, 'Not found')}")
