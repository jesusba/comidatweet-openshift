from bottle import get, post, template, run, request, route, default_app
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHENTICATE_URL = "https://api.twitter.com/oauth/authenticate?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "dfy0QjVcTRWQ4ATV4tbOkJCw0"
CONSUMER_SECRET = "lYG1Ywk25TVt8jDzJ52AkNTXZouvbUiXiY8riFOvitQQvhCbWT"
TOKENS = {}

#Definiendo funciones para autenticacion en Twitter

#Acceso a la API mediante parametros del cliente
def get_request_token():
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
    )
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    TOKENS["request_token"] = credentials.get('oauth_token')[0]
    TOKENS["request_token_secret"] = credentials.get('oauth_token_secret')[0]

#Token de solicitud
def get_access_token(TOKENS):
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=TOKENS["request_token"],
                   resource_owner_secret=TOKENS["request_token_secret"],
                   verifier=TOKENS["verifier"],
    )

    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    TOKENS["access_token"] = credentials.get('oauth_token')[0]
    TOKENS["access_token_secret"] = credentials.get('oauth_token_secret')[0]

@get('/')
def index():
    get_request_token()
    authorize_url = AUTHENTICATE_URL + TOKENS["request_token"]
    return template('index.tpl', authorize_url=authorize_url)

#Twiteando
@bottle.post('/twittear')
def tweet_submit():
    def get_verifier():
        TOKENS["verifier"] = bottle.request.query.oauth_verifier
        get_access_token(TOKENS)
    texto = "Tweet enviado desde openshift"
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=TOKENS["access_token"],
                   resource_owner_secret=TOKENS["access_token_secret"])
    
    url = 'https://api.twitter.com/1.1/statuses/update.json'

    r = requests.post(url=url,
                      data={"status":texto},
                      auth=oauth)
    if r.status_code == 200:
        return "<p>Tweet enviado correctamente.</p><form><input type='button' value='VOLVER ATRÁS' name='Back2' onclick='history.back()' /></form>"
    else:
        return "<p>Problema al enviar el tweet.</p><form><input type='button' value='VOLVER ATRÁS' name='Back2' onclick='history.back()' /></form>"

import os
from bottle import TEMPLATE_PATH

TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'], 
    'app-root/runtime/repo/wsgi/views/')) 

application=bottle.default_app()

