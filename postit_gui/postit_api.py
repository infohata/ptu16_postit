import requests
import json
import config


class Post:
    id = 0
    title = '--UNTITLED--'
    body = ''
    image = ''
    created_at = None
    username = ''

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
        return None
    else:
        if response.status_code == 200 or response.status_code == 400:
            result = json.loads(response.text)
            return result
        else:
            print(response.text)
            return None


def server_get(path) -> list:
    url = f'{config.SERVER_URL}/{path}/'
    headers = config.HEADERS
    try:
        response = requests.request("GET", url, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
    except Exception as e:
        print(e)
        return None
    else:
        return json.loads(response.text)

def get_posts() -> list[Post]:
    posts_list = server_get('posts')
    posts = []
    for post_dict in posts_list:
        posts.append(Post(**post_dict))
    return posts
