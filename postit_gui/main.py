import PySimpleGUI as sg
import postit_api as api

api_token = None
username = ''

def login_window(main_window: sg.Window) -> (str, str|None):
    api_token = None
    layout = [
        [sg.Text('Username:', size=(10, 1)), 
         sg.Input('', size=(10, 1), key='-USERNAME-'),],
        [sg.Text('Password:', size=(10, 1)),
         sg.Input('', size=(10, 1), key='-PASSWORD-', password_char='*'),],
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
                sg.popup_ok('Login Successful')
                break
            else:
                reasons = []
                for name, value in result.items():
                    reasons.append(f" - {name}: {value[0]}.")
                reason = '\n'.join(reasons)
                sg.popup_error(f'Error: login failed. Try again. \nReason:\n{reason}')
    main_window.un_hide()
    if not api_token:
        window['-USERNAME-'].update('')
    return values['-USERNAME-'], api_token


def handle_post_selection(window:sg.Window, post: api.Post):
    window['-POST-TITLE-'].update(post.title)
    window['-POST-BODY-'].update(post.body)
    window['-POST-OWNER-'].update(post.username)
    window['-POST-CREATED-'].update(post.created_at)

def main_window(api_token: str | None) -> None:
    post_list_layout = sg.Column(
        [
            [sg.Listbox(api.get_posts() or [], key='-POSTS-', size=(20, 10), enable_events=True)],
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
        [sg.Button('Login', key='-LOG-IN-OUT-'), 
         sg.Text('', key='-USERNAME-'),],
        [post_list_layout, post_detail_layout],
    ]
    window = sg.Window('Postit', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-LOG-IN-OUT-':
            if api_token:
                api_token = None
                username = ''
                window['-LOG-IN-OUT-'].update('Login')
                window['-USERNAME-'].update('')
            else:
                username, api_token = login_window(window)
                if api_token:
                    window['-USERNAME-'].update(username)
                    window['-LOG-IN-OUT-'].update('Logout')
        if event == '-POSTS-':
            handle_post_selection(window, values['-POSTS-'][0])

main_window(api_token)
