from kkbox_developer_sdk.auth_flow import KKBOXOAuth
from kkbox_developer_sdk.api import KKBOXAPI
import configparser
import logging
config = configparser.ConfigParser()
config.read('config.ini')

logger = logging.getLogger(__name__)

auth = KKBOXOAuth(config['KKBOX']['ID'], config['KKBOX']['SECRET'])
token = auth.fetch_access_token_by_client_credentials()
print(token.access_token)
kkboxapi = KKBOXAPI(token)
search_results = kkboxapi.search_fetcher.search('workout', types=['playlist'], terr='HK')
playlists = search_results['playlists']['data']
first = playlists[0]
print(first)

