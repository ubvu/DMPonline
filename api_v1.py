import requests
from config import CLIENT_SECRET, EMAIL


DMP_ONLINE_URL = 'https://dmponline.vu.nl/api/v1'

DEFAULT_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Accept': 'application/json'
}


def retrieve_auth_token():
    payload = {
        'grant_type': 'authorization_code',
        'email': EMAIL,
        'code': CLIENT_SECRET
    }
    target = f'{DMP_ONLINE_URL}/authenticate'
    resp = requests.post(target, json=payload, headers=DEFAULT_HEADERS)

    token = None
    if resp.status_code == 200:
        response = resp.json()
        token = response['access_token']
        print('fetched token')
    else:
        print('could not fetch token')
    return token


def retrieve_plan(token, id):
    target = f'{DMP_ONLINE_URL}/plans/{id}'
    headers = DEFAULT_HEADERS.copy()
    headers['Authorization'] = f'Bearer {token}'
    resp = requests.get(target, headers = headers)
    
    data = None
    if resp.status_code == 200:
        data = resp.json()['items']
    else:
        print('api error')
    
    return data


def retrieve_plans(ids: list):
    token = retrieve_auth_token()
    for id in ids:
        yield retrieve_plan(token, id)
