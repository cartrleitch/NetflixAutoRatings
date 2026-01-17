Automatically displays the IMDb rating for the episode of a Netflix show currently being watched.
Requires title.basics.tsv, title.episode.tsv, and title.ratings.tsv from https://datasets.imdbws.com/
MUST have Netflix at 100% scale.
Needs Tesseract installed for OCR.
Right now, the only issue is that program requires parent tconst ID (series ID) to find ratings by episode number. Hard-coded to One Piece for now :)

Todo:
Enable use for any show on Netflix (maybe have user enter show title on startup, then find that title in title.basics.tsv where its id is also a parent id in title.episode.tsv.). Otherwise, do this but instead of user entering it, find the show based on the title somehow (whether the series name is in the title, or you can find the series by the title).
Store selected show persistently, reference on startup. 
Have startup script that can be run to change focused show.
OR
Extract series title from title of episode.
Make it work for movies
