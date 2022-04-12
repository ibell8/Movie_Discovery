import os
import requests
from dotenv import load_dotenv, find_dotenv


def gather_data(ids):
    """This function will gather all of the data we need
    from our tmdb api, such as, movie name, genres
    taglines and images.
    """
    names = []
    genres = []
    taglines = []
    images = []
    i = 0
    load_dotenv(find_dotenv())
    api_key = os.getenv("API_KEY")
    for single_id in ids:
        url = (
            "https://api.themoviedb.org/3/movie/"
            + single_id
            + "week?api_key="
            + api_key
            + "&language=en-US"
        )

        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            docs = response_json
            # prettydoc= json.dumps(docs, indent=4, sort_keys=True) 'import json' to use
            genres.append([])
            for genre in docs["genres"]:
                genres[i].append(genre["name"])
            i += 1
        else:
            print("Error with TMDB API")
        # Info for front end
        names.append(docs["title"])
        taglines.append(docs["tagline"])
        images.append("https://image.tmdb.org/t/p/w500" + docs["poster_path"])
    return names, genres, taglines, images
