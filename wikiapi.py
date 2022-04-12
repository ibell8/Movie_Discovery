import requests


def get_urls(names):
    link = []
    for name in names:
        url = (
            "https://en.wikipedia.org/w/api.php?action=query&titles="
            + name
            + "&prop=extracts|pageimages|info&pithumbsize=400&inprop=url&redirects=&format=json&origin=*"
        )
        response = requests.get(url)
        # I got the idea of this if statement from: https://realpython.com/python-requests/
        if response.status_code == 200:
            response_json = response.json()
            docs = response_json
            # prettydoc= json.dumps(docs, indent=4, sort_keys=True) 'import json' to use
            newdoc = docs["query"]["pages"]
            numvalue = list(newdoc.keys())[0]
            link.append((newdoc[numvalue]["fullurl"]))
    return link
