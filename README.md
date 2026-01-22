Automatically displays the IMDb rating for the episode of a Netflix show currently being watched.
Requires title.basics.tsv, title.episode.tsv, and title.ratings.tsv from https://datasets.imdbws.com/
MUST have Netflix at 100% scale on 1080p or 125% on 4k.
Needs Tesseract installed for OCR.

Todo:
Don't strip ending punctuation from extracted title, namely exclamation points.
Store session statistics persistently with date. Make sure stats are accurate. 
