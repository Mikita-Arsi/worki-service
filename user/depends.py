from fastapi import Depends, HTTPException, status
from .security import JWTBearer, decode_access_token
from .models import User


async def get_current_user(
    token: str = Depends(JWTBearer()),
) -> User:
    exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise exception
    email: str = payload.get("sub")
    if email is None:
        raise exception
    user = await User.objects.get(email=email)
    if user is None:
        return exception
    return user
    