import ormar
from db import MainMeta
from user.models import User


class Link(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    link: str = ormar.String(max_length=75)
    owner: User = ormar.ForeignKey(User)
