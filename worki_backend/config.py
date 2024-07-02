import os

DB = os.environ.get("DB")
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = os.environ.get("JWT_EXPIRE_MINUTES")
