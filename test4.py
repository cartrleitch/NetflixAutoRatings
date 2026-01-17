import pyautogui
import time
import NetflixAutoRatings as ar

f = open("title.episode.tsv", "r")

episde_dict = {}

for line in f:
    split_line = line.split("\t")
    episode_id = split_line[0]
    parent_id = split_line[1]
    season_num = split_line[2]
    episode_num = split_line[3]

    episde_dict[episode_id] = [parent_id, season_num, episode_num]
print("Episode Dictionary Made!")

while True:
    episode_id_input = input("Enter Episode ID (or 'exit' to quit): ")
    if episode_id_input.lower() == 'exit':
        break
    if episode_id_input in episde_dict:
        parent_id, season_num, episode_num = episde_dict[episode_id_input]
        rating = ar.get_rating_by_episode_id(episode_id_input)
        print(f"Episode ID: {episode_id_input}")
        print(f"Parent ID: {parent_id}")
        print(f"Season Number: {season_num}")
        print(f"Episode Number: {episode_num}")
        print(f"Average Rating: {rating}\n")
    else:
        print("Episode ID not found in the dataset.\n")
f.close()