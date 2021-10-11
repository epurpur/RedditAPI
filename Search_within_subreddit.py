"""
The following script searches the Charlottesville subreddit (r/Charlottesville)

The first several lines set up Authentication. The 'Passwords' module is not a part of the github repo and a user must
create their own reddit client_id and secret_key. To set this up I recommend the following link and youtube video: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

Once authentication is set up, the code searches for new posts in the Charlottesville subreddit. The response is a lot of JSON data but in there is all information about the post. 
From there it makes a list of each post's id and makes a request for each post using that ID. 
The final output is formatted JSON of the title of the post followed by the text of each comment. 

Reddit API documentation: https://www.reddit.com/dev/api/

"""




import requests
import pandas as pd
import Passwords


#### SET UP AUTHENTICATION
CLIENT_ID = Passwords.client_id()
SECRET_KEY= Passwords.secret_key()


auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
        'grant_type': 'password',
        'username': 'epurpur',
        'password': Passwords.password()
        }

#identify version of API
headers = {'User-Agent': 'MyAPI/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                   auth=auth,
                   data=data,
                   headers=headers)

TOKEN = res.json()['access_token']

headers['Authorization'] = f'bearer {TOKEN}'

print(requests.get('https://oauth.reddit.com/api/v1/me', headers=headers))




#### GET NEW POSTS FROM SUBREDDIT WITH SEARCH TERM 'food'

#restrict_sr is required or else results are not limited to search term
res = requests.get('https://oauth.reddit.com/r/Charlottesville/search.json?q=food&restrict_sr=on',
                   headers=headers,
                   params={'limit': '5'})    # top 5 posts

#make dataframe from results
df = pd.DataFrame()

for post in res.json()['data']['children']:
    df = df.append({'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'post_id': post['data']['id']
                }, ignore_index=True)
    
post_ids = df['post_id'].tolist()           # makes list of post ids



#### LOOP THROUGH POSTS TO GET COMMENTS
for post in post_ids:
    res = requests.get(f'https://oauth.reddit.com/r/Charlottesville/comments/{post}', headers=headers)
    
    data = res.json()
    
    print()    
    print('***NEXT POST***')
    
    #post content
    print(data[0]['data']['children'][0]['data']['title'])
    print(data[0]['data']['children'][0]['data']['selftext'])

    #post comments
    for comment in data[1]['data']['children']:
        print('COMMENT---')
        print(comment['data']['body'])
        
    
    print()
