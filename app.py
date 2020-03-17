from flask import Flask, url_for
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hi there hi'

oauth = OAuth(app)

# the following local.aquiferre.com is something in /etc/hosts
# that redirect traffic to 127.0.0.1, it helps when there might
# be session storage conflict between several flask web project
# working on same machine/browser, e.g. oAuth server and client
oauth.register(
    name='o2',
    client_id='eVBfyD7yNJwJJ5coC0LZU4BB',
    client_secret='84H2UADnpGBWIXxLuorx38CvgVbM3TcNFmUeAOt5fG9AdWAN',
    access_token_url='http://local.aquiferre.com:5000/oauth/token',
    access_token_params=None,
    authorize_url='http://local.aquiferre.com:5000/oauth/authorize',
    authorize_params=None,
    api_base_url='http://local.aquiferre.com:5000/api/me',
    client_kwargs={'scope': 'profile'},
)

# o2 = oauth.create_client('o2')

@app.route('/')
def index():
    return 'hi there'

@app.route('/login')
def login():
    o2 = oauth.create_client('o2')
    redirect_uri = url_for('authorize', _external=True)
    return o2.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    o2 = oauth.create_client('o2')
    token = o2.authorize_access_token()
    resp = o2.get('me')
    profile = resp
    # do something with the token and profile
    # print(token)
    return 'the user is {} </br>And its token from auth server is {}'.format(profile.text, token)

app.run(port=7070, debug=True)
