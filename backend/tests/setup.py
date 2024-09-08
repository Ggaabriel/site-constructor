from app.main import app

from .api import ClientApi

client = ClientApi(app)
