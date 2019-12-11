import logging

from app.core.config import ELIXIR_CLIENT_ID, ELIXIR_CLIENT_SECRET, ELIXIR_METADATA_URL
from app.business.oauth_client import oauth
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi.encoders import jsonable_encoder


async def auth(request: Request):
    logging.info(request.query_params)
    token = await oauth.client.elixir.authorize_access_token(request)
    logging.info(token)
    user = await oauth.client.elixir.parse_id_token(request, token)
    request.session['token'] = token
    logging.info('Logged in User:' +  user['email'])
    jsonResponse = { 'Process' : 'Elixir_Auth'}
    jsonResponse['login_success'] = True
    jsonResponse['status'] = 200
    jsonResponse['user'] = user['email']
    jsonResponse_json = jsonable_encoder(jsonResponse)
    return JSONResponse(content=jsonResponse_json, status_code=jsonResponse['status'])


async def login(request: Request):
    redirect_uri = request.url_for('oauth_login_auth')
    return await oauth.client.elixir.authorize_redirect(request, redirect_uri)



async def auth_request(request: Request):
    if 'token' in request.session:
        token = request.session['token']
        user = await oauth.client.elixir.parse_id_token(request, token)
        if 'email' in dict(user):
            logging.info('Authorized User:' +  user['email'])
            return user
        else:
            return None
    else:
        return None
    
async def logout(request: Request):
    request.session.pop('token', None)
    jsonResponse = { 'Process' : 'Elixir_Auth'}
    jsonResponse['logout_success'] = True
    jsonResponse['status'] = 200
    jsonResponse_json = jsonable_encoder(jsonResponse)
    return JSONResponse(content=jsonResponse_json, status_code=jsonResponse['status'])