Automatically displays the IMDb rating for the episode of a Netflix show currently being watched.
Requires title.basics.tsv, title.episode.tsv, and title.ratings.tsv from https://datasets.imdbws.com/
MUST have Netflix at 100% scale.
Needs Tesseract installed for OCR.
Right now, the only issue is that program requires parent tconst ID (series ID) to find ratings by episode number. Hard-coded to One Piece for now :)

Todo:
Clean it up
Package it in nice executable
Improve flexibility across different displays and scenarios
Enhance error handling and edge cases (so it works even if it is weird)
List episodes watched during a viewing session.
