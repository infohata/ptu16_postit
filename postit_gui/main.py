import PySimpleGUI as sg
import postit_api as api
import remember_me
from typing import Any

def popup_error(result: dict|None):
    reason = ''
    if type(result) == dict:
        reasons = []
        for name, value in result.items():
            reasons.append(f" - {name}: {value[0]}.")
        reason = '\n'.join(reasons)
    sg.popup_error(f'Error. Try again.\nReason:\n{reason}')

def save_post(api_token:str, post:api.Post, values:dict[str, Any]) -> (api.Post, int):
    if len(values['title']) >= 3 and len(values['body']) >= 10:
        if post.id == 0:
            post_dict, status = api.new_post(api_token, **values)
        else:
            post_dict, status = api.update_post(api_token, post.id, **values)
        if status >= 200 and status < 400:
            post = api.Post(**post_dict)
            sg.popup_auto_close('Posted. Thank you', auto_close_duration=2)            
        else:
            popup_error(post_dict)
    else:
        sg.popup_error('You must write something more')
    return post, status

def post_window(main_window:sg.Window, api_token:str, post=api.Post()) -> api.Post|None:
    status = 0
    layout = [
        [sg.Text('Title:', size=(10, 1)),
         sg.Input(post.title, size=(50, 1), key='title')],
        [sg.Text('Body:'),],
        [sg.Multiline(post.body, size=(80, 8), key='body')],
        [sg.Button('Post it', key='-CONFIRM-POST-'),
         sg.Button('Cancel', key='-CANCEL-')],
    ]
    window = sg.Window('Post on Postit', layout, finalize=True)
    main_window.hide()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '-CANCEL-':
            break
        if event == '-CONFIRM-POST-':
            post, status = save_post(api_token, post, values)
            if status >= 200 and status < 400:
                break
    main_window.un_hide()
    window.close()
    if status == 201 or hasattr(post, 'id') and post.id != 0:
        return post

def handle_new_post(window:sg.Window, api_token:str):
    new_post = post_window(window, api_token)
    update_posts(window, new_post)

def handle_edit_post(window:sg.Window, post:api.Post, api_token:str):
    updated_post = post_window(window, api_token, post)
    update_posts(window, updated_post)

def handle_delete_post(window:sg.Window, post:api.Post, api_token:str):
    confirmation = sg.popup_yes_no('Are you sure you want to delete your post?\nYou will lose all your comments and likes.', no_titlebar=True)
    if confirmation == "Yes":
        result, status = api.delete_post(api_token, post.id)
        if status == 204:
            sg.popup_auto_close('Done.', auto_close_duration=1)
        else:
            popup_error(result)
        update_posts(window)

def handle_like(window:sg.Window, post:api.Post, api_token:str):
    result, status = api.like_post(post.id, api_token)
    if status >= 200 and status < 400:
        sg.popup_auto_close('Thank you!', auto_close_duration=1)
    else:
        sg.popup_error(result[0])
    update_posts(window, post)

def login_window(main_window: sg.Window) -> (str, str|None):
    api_token = None
    layout = [
        [sg.Text('Username:', size=(10, 1)), 
         sg.Input('', size=(20, 1), key='-USERNAME-'),],
        [sg.Text('Password:', size=(10, 1)),
         sg.Input('', size=(20, 1), key='-PASSWORD-', password_char='*'),],
        [sg.Checkbox('Remember me', key='-REMEMBER-ME-', default=True),],
        [sg.Button('Log in', key='-LOGIN-'), 
         sg.Button('Cancel', key='-CANCEL-'),],
    ]
    window = sg.Window('Login to Postit', layout, finalize=True)
    main_window.hide()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '-CANCEL-':
            break
        if event == '-LOGIN-':
            result = api.login(values['-USERNAME-'], values['-PASSWORD-'])
            if result and 'token' in result:
                api_token = result['token']
                if values['-REMEMBER-ME-']:
                    remember_me.save_user(values['-USERNAME-'], api_token)
                else:
                    remember_me.forget_me()
                sg.popup_auto_close('Login Successful', auto_close_duration=1)
                break
            else:
                popup_error(result)
    if not api_token:
        main_window['-USERNAME-'].update('')
    main_window.un_hide()
    window.close()
    return values['-USERNAME-'], api_token

def handle_post_selection(window:sg.Window, post: api.Post, username='') -> api.Post:
    window['-POST-TITLE-'].update(post.title)
    window['-POST-BODY-'].update(post.body)
    window['-POST-OWNER-'].update(post.username)
    window['-POST-CREATED-'].update(post.created_at)
    window['-POST-LIKES-'].update(f'\u2665 {post.likes_count}')
    if len(username) > 0:
        window['-LIKE-POST-'].update(disabled=False)
    if len(username) > 0 and username == post.username:
        window['-EDIT-POST-'].update(disabled=False)
        window['-DELETE-POST-'].update(disabled=False)
    else:
        window['-EDIT-POST-'].update(disabled=True)
        window['-DELETE-POST-'].update(disabled=True)
    return post

def update_posts(window:sg.Window, post=None) -> api.Post|None:
    posts = api.get_posts()
    window['-POSTS-'].update(posts)
    if post != None:
        post_dict = api.server_get(f'post/{post.id}')
        if post_dict:
            selected_post = api.Post(**post_dict)
            handle_post_selection(window, selected_post)
            return selected_post

def handle_login_logout(window: sg.Window, username: str, api_token: str|None):
    if api_token:
        api_token = None
        username = ''
        window['-LOG-IN-OUT-'].update('Login')
        window['-USERNAME-'].update('')
        window['-LIKE-POST-'].update(disabled=True)
        window['-NEW-POST-'].update(disabled=True)
        window['-EDIT-POST-'].update(disabled=True)
        window['-DELETE-POST-'].update(disabled=True)
    else:
        username, api_token = login_window(window)
        if api_token:
            window['-USERNAME-'].update(username)
            window['-LOG-IN-OUT-'].update('Logout')
            window['-LIKE-POST-'].update(disabled=False)
            window['-NEW-POST-'].update(disabled=False)
    return username, api_token

def main_window(username='', api_token=None) -> None:
    if api_token != None:
        login_logout_button_name = 'Logout'
        disable_user_actions = False
    else:
        login_logout_button_name = 'Login'
        disable_user_actions = True
    post_list_layout = sg.Column(
        [
            [sg.Listbox(api.get_posts() or [], key='-POSTS-', size=(30, 10), enable_events=True)],
            [sg.Button('\u21CA', key='-REFRESH-POSTS-'),
             sg.Button('+ Add', key='-NEW-POST-', disabled=disable_user_actions), 
             sg.Button('\u270F', key='-EDIT-POST-', disabled=True),
             sg.Button('X', key='-DELETE-POST-', disabled=True)],
        ]
    )
    post_detail_layout = sg.Column(
        [
            [sg.Text(text='', key='-POST-TITLE-', size=(50, 1), font=(None, 20)),],
            [sg.Text(text='', key='-POST-BODY-', size=(80, 8)),],
            [sg.Text(text='', key='-POST-LIKES-', size=(10, 1)),
             sg.Button('\u2665', key='-LIKE-POST-', disabled=True),
             sg.Text(text='', key='-POST-OWNER-', size=(30, 1)),
             sg.Text(text='', key='-POST-CREATED-', size=(30, 1)),],
        ]
    )
    layout = [
        [sg.Button(login_logout_button_name, key='-LOG-IN-OUT-'), 
         sg.Text(username, key='-USERNAME-'),],
        [post_list_layout, post_detail_layout],
    ]
    window = sg.Window('Postit', layout)
    selected_post = None
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-LOG-IN-OUT-':
            username, api_token = handle_login_logout(window, username, api_token)
        if event == '-POSTS-':
            if values['-POSTS-'] and len(values['-POSTS-']) > 0:
                selected_post = handle_post_selection(window, values['-POSTS-'][0], username)
        if event == '-REFRESH-POSTS-':
            selected_post = update_posts(window, selected_post)
        if event == '-LIKE-POST-':
            handle_like(window, selected_post, api_token)
        if event == '-NEW-POST-':
            handle_new_post(window, api_token)
        if event == '-EDIT-POST-':
            handle_edit_post(window, selected_post, api_token)
        if event == '-DELETE-POST-':
            handle_delete_post(window, selected_post, api_token)

username, api_token = remember_me.load_user()
main_window(username, api_token)
