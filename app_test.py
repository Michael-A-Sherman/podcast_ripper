from podcast import download_podcast_library, get_episode_data

num_of_episodes = 1
podcast_url = 'http://feeds.everythingisalive.com/everythingisalive'
data = get_episode_data(podcast_url, num_of_episodes)
library = download_podcast_library(data)