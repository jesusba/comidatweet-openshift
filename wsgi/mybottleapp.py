# -*- encoding: utf-8 -*-

from bottle import default_app, get, post, template, request, static_file, response
import requests
import json
from requests_oauthlib import OAuth1
from urlparse import parse_qs

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHENTICATE_URL = "https://api.twitter.com/oauth/authenticate?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "QBYFweXAQsit2LhGT66UJQSOg"
CONSUMER_SECRET = "5ERrCsaiIevDDFxItsHHHgqr8UX5wFJHNPr1RG3p7NMzqdP8mj"
TOKENS = {}

def get_request_token():
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
    )
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    TOKENS["request_token"] = credentials.get('oauth_token')[0]
    TOKENS["request_token_secret"] = credentials.get('oauth_token_secret')[0]
    
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
    return bottle.template('index.tpl', authorize_url=authorize_url)

@get('/buscar')
def get_verifier():
    TOKENS["verifier"] = bottle.request.query.oauth_verifier
    get_access_token(TOKENS)
    return bottle.template('buscar.tpl')

@route('/resultado', method='POST')
def search_tweets():
    def get_verifier():
        TOKENS["verifier"] = bottle.request.query.oauth_verifier
        get_access_token(TOKENS)
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=TOKENS["access_token"],
                   resource_owner_secret=TOKENS["access_token_secret"])

    texto = request.forms.get("nombre")
    url = "https://api.twitter.com/1.1/search/tweets.json"
    texto2 = texto.replace(' ','%20')
    r = requests.get(url=url,params={"q":texto2, "lang":"es", "result_type":"recent", "count":"10"},auth=oauth)

	#listacontenido = []
	#listaavatar = []
	#listaautor = []
	#listafecha = []

	#for textop in texto:
		#dicc = json.loads(r.text)
		#contenido = dicc['statuses']['text']
		#listacontenido.append(contenido)
		#avatar = dicc['statuses']['user']['profile_image_url']
		#listaavatar.append(avatar)
		#autor = dicc['statuses']['user']['name']
		#listaautor.append(autor)
		#fecha = dicc['statuses']['created_at']
		#listafecha.append(fecha)
	#mapa = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
	
	#obtener=requests.get(url=mapa,params={'origin':origin,
	
    return r.text
		#textop = texto, palabra=listapalabra, contenido=listacontenido, autor=listaautor, avatar=listaavatar, fecha=listafecha)

#def tweet_search1():
    #textoubi = request.forms.get("nombre1")
    #oauth = OAuth1(CONSUMER_KEY,
                   #client_secret=CONSUMER_SECRET,
                   #resource_owner_key="access_token",
                   #resource_owner_secret="access_token_secret")                   

	#url = "https://api.twitter.com/1.1/search/tweets.json"

    #texto2ubi = textoubi.replace(' ','%20')
	#r = requests.get(url=url,params={"q":texto2ubi, "lang":"es", "geocode":"39.737583,-4.2851364,1176137mi", "result_type":"mixed", "count":"10"},auth=oauth)
    
    #return r.text    
    
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
