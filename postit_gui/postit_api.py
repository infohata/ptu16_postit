import requests
import json
import config
from typing import Any


class Post:
    id = 0
    title = ''
    body = ''
    image = ''
    created_at = None
    username = ''
    likes_count = 0

    def __init__(self, **kwargs) -> None:
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __str__(self) -> str:
        return f"{self.title}"
    
    def __repr__(self) -> str:
        return f"{self.id}"


def login(username: str, password: str) -> str | None:
    url = f'{config.SERVER_URL}/api-token-auth/'
    headers = config.HEADERS
    data = json.dumps({
        'username': username,
        'password': password
    })
    try:
        response = requests.request("POST", url, headers=headers, data=data)
    except Exception as e:
        print('Login Error:', e)
    else:
        if response.status_code == 200 or response.status_code == 400:
            result = json.loads(response.text)
            return result
        else:
            print(response.text)


def server_get(path:str) -> list|dict|None:
    url = f'{config.SERVER_URL}/{path}/'
    headers = config.HEADERS
    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        print(e)
    else:
        if response.text:
            return json.loads(response.text)
    
def server_post(path:str, token:str, data={}, method="POST") -> (dict[str, Any], int):
    url = f'{config.SERVER_URL}/{path}/'
    headers = config.HEADERS
    headers['Authorization'] = f'Token {token}'
    json_data = json.dumps(data)
    try:
        response = requests.request(method, url, headers=headers, data=json_data)
    except Exception as e:
        print(e)
        return {}, 499
    else:
        if response.text:
            result = json.loads(response.text)
        else:
            result = None
        return result, response.status_code

def get_posts() -> list[Post]:
    posts_list = server_get('posts')
    posts = []
    for post_dict in posts_list:
        posts.append(Post(**post_dict))
    return posts

def like_post(post_id:int, token:str) -> (dict[str, int], int):
    path = f'post/{post_id}/like'
    like_dict, status = server_post(path, token)
    if status == 400:
        like_dict, status = server_post(path, token, method="DELETE")
    return like_dict, status

def new_post(token:str, **kwargs) -> (dict[str, Any], int):
    path = 'posts'
    post_dict, status = server_post(path, token, kwargs)
    return post_dict, status

def update_post(token:str, pk:int, **kwargs) -> (dict[str, Any], int):
    path = f'post/{pk}'
    post_dict, status = server_post(path, token, kwargs, "PUT")
    return post_dict, status

