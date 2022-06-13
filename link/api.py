from fastapi import APIRouter, Depends, HTTPException, status
from user.depends import get_current_user
from user.models import User
from user import schemas as us

from . import models as m
from . import schemas as s

link_router = APIRouter(tags=['link'])


@link_router.post("/link", response_model=s.Link)
async def create_link(link: s.CreateLink, user: User = Depends(get_current_user)):
    return await m.Link.objects.create(link=link.link, owner=user)


@link_router.delete("/link")
async def delete_link(link_id: int, user: User = Depends(get_current_user)):
    link = await m.Link.objects.get_or_none(id=link_id)
    if link is not None and link.owner.id == user.id:
        await m.Link.objects.delete(id=link_id)
        return {"message": 'Successfully deleted'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found this link")


@link_router.get("/link/{link_pk}", response_model=m.Link)
async def get_link(link_pk: int):
    try:
        return await m.Link.objects.get(pk=link_pk)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found this link")


@link_router.get("/{prefix_or_id}", response_model=s.GetListLinkWithUser)
async def get_links(prefix_or_id: int | str):
    creator = 0
    if type(prefix_or_id) == str:
        creator = await m.User.objects.get_or_none(prefix=prefix_or_id)
        if creator is not None:
            user_id = creator.id
    elif creator in (0, None):
        creator = await m.User.objects.get_or_none(id=prefix_or_id)
        if creator is not None:
            user_id = prefix_or_id
    if creator in (0, None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found this user")
    return s.GetListLinkWithUser(
        owner=us.User(**creator.dict()),
        links=[
            s.GetListLink(id=i.id, link=i.link) for i in await m.Link.objects.filter(owner__id=user_id).all()
        ]
    )
