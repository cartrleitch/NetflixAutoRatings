episode_title = input("Enter the episode title: ")

def get_rating_by_title(title):
    titles = open("title.basics.tsv", "r", encoding="utf-8")
    ratings = open("title.ratings.tsv", "r", encoding="utf-8")
    target_title_id = ""

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

    for rating_line in ratings:
        split_rating_data = rating_line.split("\t")
        rating_title_id = split_rating_data[0]
        average_rating = split_rating_data[1]

        if target_title_id == rating_title_id:
                rating_line = f"{primary_title} has an average rating of {average_rating}."
                return average_rating
     
print(get_rating_by_title(episode_title))
    
