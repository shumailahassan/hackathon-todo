from fastapi import APIRouter, Depends

from src.schemas.auth import UserRead
from src.models import User
from src.middleware.auth import get_current_user

router = APIRouter()




@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
