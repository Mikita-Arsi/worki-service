import sqlalchemy
import databases
import ormar
from config import DB


metadata = sqlalchemy.MetaData()
db = databases.Database(DB)
engine = sqlalchemy.create_engine(DB)


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = db
