from os import path
from requests_xml import XMLSession
import requests
import lxml
import sys


#  Collects links and episode title from url, creates list of dictionaries
def get_episode_data(url, num_episodes):
    episodes = []
    try:
        num_episodes = int(num_episodes)
        if num_of_episodes < 1:
            print('Please enter a number greater than 0')
            sys.exit(1)
    except ValueError:
        print('Please enter a number of episodes to download')
        sys.exit(1)
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
        print('Enter Valid URL')
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

# Test Code
num_of_episodes = 1

# Valid Podcast Feed Link
podcast_url = 'http://feeds.everythingisalive.com/everythingisalive'

# Good URL but not podcast feed
# podcast_url = 'http://www.google.com'

# Invalid URL
# podcast_url = 'hello'

podcast_url2 = 'http://feeds.feedburner.com/mbmbam'

data = get_episode_data(podcast_url, num_of_episodes)
data2 = get_episode_data(podcast_url2, num_of_episodes)


library = download_podcast_library(data)


'''
Still need to separate num_episodes from get episode data function
function is doing too much
'''

def get_num_episodes(num)
