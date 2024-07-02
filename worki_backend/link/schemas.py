from pydantic import BaseModel
from user.schemas import User
from typing import List


class CreateLink(BaseModel):
    link: str


class GetListLink(CreateLink):
    id: int


class UploadLink(GetListLink):
    pass


class Link(UploadLink):
    owner: User


class GetListLinkWithUser(BaseModel):
    owner: User
    links: List[GetListLink]
