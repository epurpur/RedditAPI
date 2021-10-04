

import requests
import pandas as pd

subreddit = 'Charlottesville'
limit = 100
timeframe = 'month'
listing = 'top'

def get_reddit(subreddit, listing, limit, timeframe):
    '''Make HTTP request to Reddit API. No API key needed'''
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url)
    except:
        print('An error occurred')
    return request.json()

reddit_data = get_reddit(subreddit, listing, limit, timeframe)

def get_post_titles(reddit_data):
    '''Get a list of post titles'''
    posts = []
    
    for post in reddit_data['data']['children']:
        title = post['data']['title']
        posts.append(title)
    
    return posts
    
posts = get_post_titles(reddit_data)

def get_results(reddit_data):
    '''Create a dictionary showing title, URL, score, and number of comments'''
    
    resultsDict = {}
    
    for post in reddit_data['data']['children']:
        resultsDict[post['data']['title']] = {'url':post['data']['url'], 'score':post['data']['score'], 'comments': post['data']['num_comments']}
    
    df = pd.DataFrame.from_dict(resultsDict, orient='index')
    return df

df = get_results(reddit_data)



####
#I NEED AN ID FOR EACH POST
####

#### 
# Can I insert a search string into my results?