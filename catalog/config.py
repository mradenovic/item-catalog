'''Configuration data'''

GOOGLE_LOGIN_CLIENT_ID = "954232220602-me59j84hb9enrejc0nt4i3bkd7hnf42v.apps.googleusercontent.com"
GOOGLE_LOGIN_CLIENT_SECRET = "5zMs7LtC6TgNHas8AamTdmOH"

GOOGLE = {
    'consumer_key': GOOGLE_LOGIN_CLIENT_ID,
    'consumer_secret': GOOGLE_LOGIN_CLIENT_SECRET,
    'request_token_params': {
        'scope': 'email'
    },
    'base_url': 'https://www.googleapis.com/oauth2/v1/',
    'request_token_url': None,
    'access_token_method': 'POST',
    'access_token_url': 'https://accounts.google.com/o/oauth2/token',
    'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
}
