from fastapi import BackgroundTasks, UploadFile, HTTPException, Request
from . import models as m


import shutil
import os


async def save_ava(
    user: m.User,
    file: UploadFile,
    back_tasks:BackgroundTasks
):
    if file.content_type.split("/")[0] == 'image':
        file_path = f'avas/{user.dict().get("id")}.png'
        back_tasks.add_task(write_ava, file_path, file)    
    else:
        raise HTTPException(status_code=418, detail="It isn't image")
    user.ava = file_path
    return await user.update()


def delete_ava(path: str) -> dict:
    try:
        os.unlink(f'{path}')
    except FileNotFoundError:
        return {'message': "You don't have an avatar"}
    return {'message': 'Successfully deleted'}


def write_ava(file_name: str, file: UploadFile):
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
