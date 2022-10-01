import requests
def exists(id):
    url = f"https://www.youtube.com/oembed?format=json&url=http://www.youtube.com/watch?v={id}"
    if(requests.get(url).status_code==404):
        return False
    return True