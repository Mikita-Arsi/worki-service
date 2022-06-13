from db import MainMeta


import ormar


class User(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=150)
    email = ormar.String(index=True, unique=True, nullable=False, max_length=255)
    password: str = ormar.String(max_length=200)
    prefix: str | None = ormar.String(max_length=150, nullable=True, unique=True)
    ava: str | None = ormar.String(max_length=75, nullable=True)
