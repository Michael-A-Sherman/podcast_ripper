from requests_xml import XMLSession
import opml
import requests
from os import path


# Parse OPML file for rss link
def get_rss_feed(opml_file):
    file = opml.parse(opml_file)
    podcast_library = []
    for data in file:
        podcast_data = {
            'rss_link': data.xmlUrl
        }
        podcast_library.append(podcast_data)
    return podcast_library


# parses rss feed for show title
def get_show_title(xmlUrl):
    show_titles = []
    session = XMLSession()
    r = session.get(xmlUrl)
    items = r.xml.xpath('//channel')
    for item in items:
        title = [item.xpath('//title', first=True).text]
        show_titles.append(title)
    return show_titles[0]


# Gets title and download link for latest episode
def get_latest_episode_title(xmlUrl):
    titles = []
    session = XMLSession()
    r = session.get(xmlUrl)
    items = r.xml.xpath('//item')
    for item in items:
        title = [item.xpath('//title', first=True).text]
        titles.append(title)
    return titles[0]


def get_latest_episode_download_url(xmlUrl):
    links = []
    session = XMLSession()
    r = session.get(xmlUrl)
    items = r.xml.xpath('//item')
    for urls in items:
        url = [urls.xpath('//enclosure', first=True).attrs['url']]
        links.append(url)
    return links[0]


# Function to convert episode title to usable filename
def convert_title(show, episode):
    show = show.replace(" ", "_")
    episode = episode.replace(" ", "_")
    safe_characters = '_'
    show = "".join(c for c in show if c.isalnum() or c in safe_characters).rstrip()
    episode = "".join(c for c in episode if c.isalnum() or c in safe_characters).rstrip()
    return show + "_" + episode + '.mp3'


# Creates podcast library in list of dicts
def create_library(rss_links):
    podcast_library = []
    for data in rss_links:
        library_data = {
            'show_title': get_show_title(data['rss_link'])[0],
            'latest_episode': convert_title(get_show_title(data['rss_link'])[0], get_latest_episode_title(data['rss_link'])[0]),
            'episode_link': get_latest_episode_download_url(data['rss_link'])[0],
        }
        podcast_library.append(library_data)
    return podcast_library


# downloads podcast episodes that do not already exist
def download_mp3(title, url):
    if path.exists(title):
        print(title + ' already exists')
    else:
        print('downloading: ' + title)
        download = requests.get(url, stream=True, allow_redirects=True)
        with open(title, 'wb') as f:
            for chunk in download.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    path.join(title)
            print('downloaded: ' + title)
    return title


# Test code

# OPML file from Overcast App
file = 'overcast.opml'

rss_urls = get_rss_feed(file)
library = create_library(rss_urls)

# for shows in library:
#     print(shows)


for shows in library:
    title = (shows['latest_episode'])
    url = (shows['episode_link'])
    download_mp3(title, url)



