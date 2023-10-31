import pickle
import os

def load_user() -> (str, str):
    try:
        with open('.user_session', 'rb') as session_file:
            username = pickle.load(session_file)
            token = pickle.load(session_file)
    except:
        return '', None
    else:
        return username, token

def save_user(username, token) -> bool:
    try:
        with open('.user_session', 'wb') as session_file:
            pickle.dump(username, session_file)
            pickle.dump(token, session_file)
    except:
        return False
    else:
        return True

def forget_me():
    if os.path('.user_session').exists():
        try:
            os.remove('user_session')
        except:
            pass
