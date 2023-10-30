import PySimpleGUI as sg
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

def get_posts():
    posts_list = server_get('posts')
    posts = []
    for post_dict in posts_list:
        posts.append(Post(**post_dict))
    return posts

def handle_post_selection(window:sg.Window, post: Post):
    window['-POST-TITLE-'].update(post.title)
    window['-POST-BODY-'].update(post.body)
    window['-POST-OWNER-'].update(post.username)
    window['-POST-CREATED-'].update(post.created_at)

def main_window() -> None:
    post_list_layout = sg.Column(
        [
            [sg.Listbox(get_posts() or [], key='-POSTS-', size=(20, 10), enable_events=True)],
        ]
    )
    post_detail_layout = sg.Column(
        [
            [sg.Text(text='', key='-POST-TITLE-', size=(50, 1), font=(None, 20)),],
            [sg.Text(text='', key='-POST-BODY-', size=(80, 8)),],
            [sg.Text(text='', key='-POST-OWNER-', size=(40, 1)),
             sg.Text(text='', key='-POST-CREATED-', size=(40, 1)),],
        ]
    )
    layout = [
        [post_list_layout, post_detail_layout]
    ]
    window = sg.Window('Postit', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-POSTS-':
            handle_post_selection(window, values['-POSTS-'][0])

main_window()
