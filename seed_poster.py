import psycopg2
import urllib.request
import urllib.parse
import json
import os

OMDB_API_KEY = "85229378"

movies = [
    (1,  "The Shawshank Redemption", "1994"),
    (2,  "12 Angry Men",             "1957"),
    (3,  "Star Wars",                "1977"),
    (4,  "Toy Story",                "1995"),
    (5,  "The Truman Show",          "1998"),
    (6,  "Nuovo Cinema Paradiso",    "1988"),
    (7,  "Inception",                "2010"),
    (8,  "Interstellar",             "2014"),
    (9,  "Titanic",                  "1997"),
    (10, "Kung Fu Panda",            "2008"),
    (11, "The Dark Knight",          "2008"),
    (12, "Parasite",                 "2019"),
    (13, "La La Land",               "2016"),
    (14, "Whiplash",                 "2014"),
    (15, "The Matrix",               "1999"),
    (16, "Spirited Away",            "2001"),
    (17, "Joker",                    "2019"),
    (18, "Mad Max: Fury Road",       "2015"),
    (19, "The Grand Budapest Hotel", "2014"),
    (20, "Before Sunrise",           "1995"),
]

def get_poster_url(title, year):
    query = urllib.parse.urlencode({"t": title, "y": year, "apikey": OMDB_API_KEY})
    url = f"http://www.omdbapi.com/?{query}"
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
    poster = data.get("Poster")
    return poster if poster and poster != "N/A" else None

conn = psycopg2.connect(
    dbname="term_project",
    user="postgres",
    password=os.getenv("DATABASE_PASSWORD", "@100pluS"),
    host="localhost"
)
cur = conn.cursor()

for mid, title, year in movies:
    url = get_poster_url(title, year)
    if url:
        cur.execute("UPDATE movies SET poster_url = %s WHERE id = %s", (url, mid))
        print(f"[OK]   {title}")
    else:
        print(f"[MISS] {title} — no poster found")

conn.commit()
cur.close()
conn.close()
print("Done.")