from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from pathlib import Path

config = Config(str(Path(__file__).resolve().parents[3]) + '\.env')
oauth = OAuth(config)

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
