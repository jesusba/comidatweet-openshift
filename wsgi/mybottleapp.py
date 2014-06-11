import bottle
import requests
import json
from requests_oauthlib import OAuth1
from urlparse import parse_qs
from bottle import get, post, template, run, request, route, default_app, error

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHENTICATE_URL = "https://api.twitter.com/oauth/authenticate?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "QBYFweXAQsit2LhGT66UJQSOg"
CONSUMER_SECRET = "5ERrCsaiIevDDFxItsHHHgqr8UX5wFJHNPr1RG3p7NMzqdP8mj"
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

#Buscando

@error(404)
def error404(error):
	return "ERROR 404: Pagina no encontrada"

@get('/buscar')
def get_verifier():
    TOKENS["verifier"] = request.query.oauth_verifier
    get_access_token(TOKENS)
    return template('buscar.tpl')
    
@bottle.route('/buscar', method='POST')
def tweet_search():
	def get_verifier():
		TOKENS["verifier"] = bottle.request.query.oauth_verifier
        get_access_token(TOKENS)
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=TOKENS["access_token"],
                   resource_owner_secret=TOKENS["access_token_secret"])
   
    texto = request.forms.get("nombre")
    
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    
    r = requests.post(url=url,
					data={'q':texto,
							'result_type':'mixed',
							'count':'4'},
							auth=oauth)
							
    if r.status_code == 200:
        return template('resultado.tpl')
		
    else:
        return "<p>Problema al enviar la solicitud, por favor vuelva a intentarlo.</p><form><input type='button' value='VOLVER ATRAS' name='Back2' onclick='history.back()' /></form>"

import os
from bottle import TEMPLATE_PATH

ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True

if ON_OPENSHIFT:
    TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'], 
                                      'app-root/repo/wsgi/views/'))
    application=default_app()
else:
    run(host='localhost', port=8080)
