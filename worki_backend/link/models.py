import ormar
from db import ormar_base_config
from user.models import User


class Link(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id: int = ormar.Integer(primary_key=True)
    link: str = ormar.String(max_length=75)
    owner: User = ormar.ForeignKey(User)
