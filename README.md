Automatically displays the IMDb rating for the episode of a Netflix show currently being watched.
Requires title.basics.tsv, title.episode.tsv, and title.ratings.tsv from https://datasets.imdbws.com/
MUST have Netflix at 100% scale.
Needs Tesseract installed for OCR.
Right now, the only issue is that program requires parent tconst ID (series ID) to find ratings by episode number. Hard-coded to One Piece for now :)

Todo:
Multi-season series cannot select rating by episode number, because it also needs the season number. Enable searching by title (where title and parentTconst are correct)
Make it work for movies
Handle user manually change the episode. Reset the stored episode number and rating if this happens. 
Series lookup issue: series can have same name like One Piece and One Piece
Finish speeding up other aspects of program (use series dictionary once the above issue is figured out, and find a faster way to search epsidoe ID by primary title)
Make sure the pickled cache of dictionaries works in the executable.
