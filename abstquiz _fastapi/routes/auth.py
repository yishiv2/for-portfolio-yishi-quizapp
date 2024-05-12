from database import get_firestore_collection
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from crud import auth as auth_cruds
from schemas.auth import UserCreate, UserResponse, Token
from const import QUIZ_USER_COLLCTION_NAME

router = APIRouter(prefix="/auth", tags=["Auth"])

FormDependency = Annotated[OAuth2PasswordRequestForm, Depends()]


# @router.post(
#     "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
# )
# def create_user(user_create: UserCreate,
#                 collection: any = Depends(get_firestore_collection(QUIZ_USER_COLLCTION_NAME))):
#     user_data = auth_cruds.create_user(collection, user_create)
#     print(user_data)
#     return UserResponse(displayname=user_data["displayname"], username=user_data["username"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(form_data: FormDependency, collection: any = Depends(get_firestore_collection(QUIZ_USER_COLLCTION_NAME))):
    user = auth_cruds.authenticate_user(
        collection, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")

    token = auth_cruds.create_access_token(
        user["username"], user["displayname"], timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}
