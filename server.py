from flask import Flask
from flask import Response
from authlib.flask.client import OAuth

app = Flask(__name__)
app.secret_key = 'ThisIsTheSecretKey'
app.debug = True

oauth = OAuth(app)

client_id='orluhS9vP2BBRh1dTGQYlHA9Mm4ZeVB6'
client_secret='iywIRFCof79pwA3ceRAdyNZZMvyLeINTmsykAHfmJO2ZGK_Rm_oVoNrnV3PjUoic'
api_base_url='https://dev-9tkz0vqw.auth0.com'
access_token_url='https://dev-9tkz0vqw.auth0.com/oauth/token'
authorize_url='https://dev-9tkz0vqw.auth0.com/authorize'

redirect_uri='https://openid-banestes-poc.herokuapp.com/callback'

auth0 = oauth.register(
    'auth0',
    client_id=client_id,
    client_secret=client_secret,
    api_base_url=api_base_url,
    access_token_url=access_token_url,
    authorize_url=authorize_url,
    client_kwargs={
        'scope': 'openid profile',
    },
)

@app.route("/")
def index():
    return "OPEN ID CONNECT AUTH0 HOMEPAGE", 200

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=redirect_uri, audience='https://dev-9tkz0vqw.auth0.com/userinfo')

@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    # session['jwt_payload'] = userinfo
    # session['profile'] = {
    #    'user_id': userinfo['sub'],
    #    'name': userinfo['name'],
    #    'picture': userinfo['picture']
    #}
    print('userinfo: {}'.format(userinfo))
    return userinfo, 200

if __name__ == "__main__":
    app.run()
