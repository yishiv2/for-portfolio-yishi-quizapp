
from datetime import datetime, timedelta
import hashlib
import base64
import os
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from schemas.auth import UserCreate, DecodedToken
from google.cloud.firestore import AsyncCollectionReference
from fastapi import HTTPException
from google.api_core.exceptions import GoogleAPICallError

from logger_config import logger


ALGORITHM = "HS256"
SECRET_KEY = os.environ.get("JWT_KEY")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def user_serializer(user) -> dict:
    return {
        "username": user["username"],
        "email": user["email"],
    }


def create_user(users_ref: AsyncCollectionReference, user_create: UserCreate):
    salt = base64.b64encode(os.urandom(32))
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", user_create.password.encode(), salt, 1000
    ).hex()

    email = user_create.username
    # password = user_create.get("password")
    displayname = user_create.username

    # users_ref = collection
    doc_ref = users_ref.document(email)  # ドキュメントの参照を使用する

    try:
        user = doc_ref.get()
        if user.exists:
            raise HTTPException(
                status_code=400, detail='Email is already taken')

        # パスワードをハッシュ化してユーザー情報をFirestoreに設定します。
        user_data = {
            'displayname': displayname,
            'username': email,
            'passwordHash': hashed_password,
            'lastLogin': datetime.now(),
            'salt': salt.decode(),
            'settings': {
                'language': 'Japanese',
                'theme': 'dark'
            }
        }
        doc_ref.set(user_data)
        doc_ref = users_ref.document(email)  # ドキュメントの参照を使用する
        user = doc_ref.get()

        return user.to_dict()

    except GoogleAPICallError as e:
        # Firestore API呼び出し中に発生したエラーを処理します
        raise HTTPException(status_code=500, detail=str(e))


def authenticate_user(users_ref: AsyncCollectionReference, username: str, password: str):

    try:
        # メールアドレスに一致するユーザーを検索するクエリ
        query_ref = users_ref.where("username", "==", username)
        query_snapshot = query_ref.get()
        # クエリ結果が空かどうかをチェック
        if not query_snapshot:
            raise HTTPException(status_code=404, detail="User not found")

        user = query_snapshot[0].to_dict()

        hashed_password = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), user['salt'].encode(), 1000
        ).hex()

        if user['passwordHash'] != hashed_password:
            return None

        return user

    except GoogleAPICallError as e:
        # Firestore API呼び出し中に発生したエラーを処理します
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # その他の予期せぬエラー
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")


def create_access_token(email: str, displayname: str, expires_delta: timedelta):
    # expires = datetime.now() + expires_delta
    payload = {
        'exp': datetime.now() + expires_delta,
        'username': email,
        'displayname': displayname
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        displayname = payload.get("displayname")
        if username is None:
            return None
        return DecodedToken(username=username, displayname=displayname)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception as e:
        logger.error(f"Failed to validate token: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=401, detail="Could not validate credentials")
