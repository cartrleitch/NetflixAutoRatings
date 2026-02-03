import pickle
import os
import sys
from MyLogger import logger

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def build_ratings_dict():
    """Build dictionary: {episode_id: rating}"""
    logger.info("Building ratings dictionary from TSV...")
    ratings_dict = {}
    
    with open(resource_path("title.ratings.tsv"), "r", encoding="utf-8") as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                title_id = parts[0]
                rating = parts[1]
                ratings_dict[title_id] = rating
    
    logger.info(f"Loaded {len(ratings_dict)} ratings")
    return ratings_dict

def build_episodes_dict():
    """Build dictionary: {(parent_id, episode_num): [episode_id, season_num]}"""
    logger.info("Building episodes dictionary from TSV...")
    episodes_dict = {}
    
    with open(resource_path("title.episode.tsv"), "r", encoding="utf-8") as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 4:
                episode_id = parts[0]
                parent_id = parts[1].lower()
                episode_num = parts[3].strip()
                season_num = parts[2].strip()
                key = (parent_id, episode_num)
                if key not in episodes_dict:
                    episodes_dict[key] = []
                episodes_dict[key].append([episode_id, season_num])
    
    logger.info(f"Loaded {len(episodes_dict)} episodes")
    return episodes_dict

def build_series_dict():
    """Build dictionary: {series_title.lower(): [(series_id, start_year), ...]}"""
    logger.info("Building series dictionary from TSV...")
    series_dict = {}
    
    with open(resource_path("title.basics.tsv"), "r", encoding="utf-8") as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 6:
                title_id = parts[0]
                title_type = parts[1]
                primary_title = parts[2]
                start_year = parts[5] if parts[5] != "\\N" else "0"
                
                if title_type == "tvSeries":
                    key = primary_title.lower()
                    if key not in series_dict:
                        series_dict[key] = []
                    series_dict[key].append((title_id, start_year))
    
    logger.info(f"Loaded {len(series_dict)} unique TV series titles")
    return series_dict

def build_movies_dict():
    """Build dictionary: {movie_title.lower(): [(movie_id, start_year), ...]}"""
    logger.info("Building movies dictionary from TSV...")
    movies_dict = {}
    
    with open(resource_path("title.basics.tsv"), "r", encoding="utf-8") as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 6:
                title_id = parts[0]
                title_type = parts[1]
                primary_title = parts[2]
                start_year = parts[5] if parts[5] != "\\N" else "0"
                
                if title_type == "movie":
                    key = primary_title.lower()
                    if key not in movies_dict:
                        movies_dict[key] = []
                    movies_dict[key].append((title_id, start_year))
    
    logger.info(f"Loaded {len(movies_dict)} unique movie titles")
    return movies_dict

def build_id_to_title_dict():
    """Build dictionary: {title_id: primary_title}"""
    logger.info("Building ID to title dictionary from TSV...")
    id_to_title_dict = {}
    
    with open(resource_path("title.basics.tsv"), "r", encoding="utf-8") as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                title_id = parts[0]
                primary_title = parts[2]
                id_to_title_dict[title_id] = primary_title
    
    logger.info(f"Loaded {len(id_to_title_dict)} title IDs")
    return id_to_title_dict

def save_cache():
    """Build and save all dictionaries to pickle files"""
    logger.info("=== Building dataset cache ===")
    
    ratings = build_ratings_dict()
    with open("cache_ratings.pkl", "wb") as f:
        pickle.dump(ratings, f)
    logger.info("Saved cache_ratings.pkl")
    
    episodes = build_episodes_dict()
    with open("cache_episodes.pkl", "wb") as f:
        pickle.dump(episodes, f)
    logger.info("Saved cache_episodes.pkl")
    
    series = build_series_dict()
    with open("cache_series.pkl", "wb") as f:
        pickle.dump(series, f)
    logger.info("Saved cache_series.pkl")
    
    movies = build_movies_dict()
    with open("cache_movies.pkl", "wb") as f:
        pickle.dump(movies, f)
    logger.info("Saved cache_movies.pkl")
    
    id_to_title = build_id_to_title_dict()
    with open("cache_id_to_title.pkl", "wb") as f:
        pickle.dump(id_to_title, f)
    logger.info("Saved cache_id_to_title.pkl")
    
    logger.info("=== Cache build complete ===")

def load_cache():
    """Load dictionaries from pickle files, or build if they don't exist"""
    cache_files = ["cache_ratings.pkl", "cache_episodes.pkl", "cache_series.pkl", "cache_movies.pkl", "cache_id_to_title.pkl"]
    
    # Check if all cache files exist
    if not all(os.path.exists(f) for f in cache_files):
        logger.info("Cache files not found. Building cache...")
        save_cache()
    
    logger.info("Loading cache from pickle files...")
    
    with open("cache_ratings.pkl", "rb") as f:
        ratings_dict = pickle.load(f)
    
    with open("cache_episodes.pkl", "rb") as f:
        episodes_dict = pickle.load(f)
    
    with open("cache_series.pkl", "rb") as f:
        series_dict = pickle.load(f)
    
    with open("cache_movies.pkl", "rb") as f:
        movies_dict = pickle.load(f)
    
    with open("cache_id_to_title.pkl", "rb") as f:
        id_to_title_dict = pickle.load(f)
    return ratings_dict, episodes_dict, series_dict, movies_dict, id_to_title_dict

def rebuild_cache():
    """Force rebuild of cache files"""
    logger.info("Rebuilding cache from TSV files...")
    save_cache()

if __name__ == "__main__":
    # Test: build or load cache
    rebuild_cache()
    ratings, episodes, series, movies, id_to_title = load_cache()
    
    # Test lookups
    print("\nTesting lookups:")
    print(f"One Piece series ID: {series.get('one piece', 'Not found')}")
    print(f"Episode (tt0388629, 610): {episodes.get(('tt0388629', '610'), 'Not found')}")
    print(f"Rating for tt0388629: {ratings.get('tt0388629', 'Not found')}")
    print(f"Movie Inception ID: {movies.get('inception', 'Not found')}")
    print(f"Title for tt2081647: {id_to_title.get('tt2081647', 'Not found')}")
    
    # episode_ids = episodes.get(('tt0388629', '610'), None)
    # if episode_ids:
    #     print(f"Found {len(episode_ids)} episode(s):")
    #     for ep_id in episode_ids:
    #         rating = ratings.get(ep_id, 'Not found')
    #         print(f"  Episode {ep_id}: Rating {rating}")
