from os import path
from requests_xml import XMLSession
import requests
import lxml


def get_episode_data(url, num_episodes):
    episodes = []
    num_episodes = int(num_episodes)
    try:
        session = XMLSession()
        r = session.get(url)
        items = r.xml.xpath('//item')
        for item in items:
            episode = {
                'title': item.xpath('//title', first=True).text,
                'url': item.xpath('//enclosure', first=True).attrs['url']
            }
            episodes.append(episode)
    except requests.exceptions.MissingSchema:
        print('<h1>Enter Valid URL</h1>')
    except (lxml.etree.XMLSyntaxError):
        print('Not a valid podcast feed')
    return episodes[0:num_episodes]


# Function to convert episode title to usable filename
def convert_title(title):
    title = title.replace(" ", "_")
    safe_characters = '_'
    return "".join(c for c in title if c.isalnum() or c in safe_characters).rstrip()


# downloads podcast episodes that do not already exist
def download_podcast_library(episodes):
    filename = episodes
    for episode in episodes:
        filename = convert_title(episode["title"]) + ".mp3"
        if path.exists(filename):
            print(filename + ' already exists')
        else:
            print('downloading: ' + filename)
            download = requests.get(episode['url'], stream=True, allow_redirects=True)
            with open(filename, 'wb') as f:
                for chunk in download.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                print('downloaded: ' + filename)
    return filename
