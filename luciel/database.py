from tinydb import TinyDB
from settings.config import settings

database = TinyDB(settings.DATABASE_PATH)

