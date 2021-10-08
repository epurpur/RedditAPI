
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




#### GET NEW POSTS FROM SUBREDDIT

res = requests.get('https://oauth.reddit.com/r/Charlottesville/new',
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
    
post_ids = df['post_id'].tolist()



#### LOOP THROUGH POSTS TO GET COMMENTS
for post in post_ids:
    res = requests.get(f'https://oauth.reddit.com/r/Charlottesville/comments/{post}', headers=headers)
    
    data = res.json()
    
    #post content
    print(data[0]['data']['children'][0]['data']['title'])
    print(data[0]['data']['children'][0]['data']['selftext'])

    #post comments
    for comment in data[1]['data']['children']:
        print('COMMENT---')
        print(comment['data']['body'])
        
    print()    
    print('***NEXT POST***')
    print()
