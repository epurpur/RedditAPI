
import requests

CLIENT_ID='LQsgZihn7O_eQs5Y2AFTTg'
SECRET_KEY='vv61JPYoxowQ14XLSZAN80pIgRX1sg'


auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
        'grant_type': 'password',
        'username': 'epurpur',
        'password': 'battlebot'
        }

#identify version of API
headers = {'User-Agent': 'MyAPI/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                   auth=auth,
                   data=data,
                   headers=headers)

TOKEN = res.json()['access_token']

headers['Authorization'] = f'bearer {TOKEN}'



# def choose_post_by_id(url):
#     ''' Get comments from specific post'''
#     try:
#         request = requests.get(url)
#     except:
#         print('Error occurred')
    
#     return request.json()

# # data = choose_post_by_id('https://www.reddit.com/comments/pjn2v8.json')
# data = choose_post_by_id('https://www.reddit.com/r/Charlottesville/comments/py03wo.json')

