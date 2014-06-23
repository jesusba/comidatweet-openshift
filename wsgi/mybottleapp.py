# -*- coding: utf-8 -*-

import bottle
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


@bottle.get('/')
def index():
    get_request_token()
    authorize_url = AUTHENTICATE_URL + TOKENS["request_token"]
    return bottle.template('index.tpl', authorize_url=authorize_url)

@bottle.get('/buscar')
def get_verifier():
    TOKENS["verifier"] = bottle.request.query.oauth_verifier
    get_access_token(TOKENS)
    return bottle.template('buscar.tpl')


@bottle.route('/resultado1', method='POST')
def tweet_search():
    def get_verifier():
        TOKENS["verifier"] = bottle.request.query.oauth_verifier
        get_access_token(TOKENS)
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key="access_token",
                   resource_owner_secret="access_token_secret")

    texto = bottle.request.forms.get("nombre")
    texto2 = texto.replace(' ','%20')
    
    r = requests.get("http://search.twitter.com/search.json", params={"q":texto2, "lang":"es", "result_type":"recent", "count":"10"}auth=oauth)
    dicc= json.loads(r.text)['query']
    contenido = json.loads(r.text)['results'][0]['text']
    avatar = json.loads(r.text)['results'][0]['profile_image_url']
    autor = json.loads(r.text)['results'][0]['from_user']
    fecha = json.loads(r.text)['results'][0]['created_at']
   
    return bottle.template('resultado1', contenido=contenido, autor=autor, fecha=fecha, avatar=avatar)


import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'], 
    'app-root/runtime/repo/wsgi/views/')) 

application=bottle.default_app()
