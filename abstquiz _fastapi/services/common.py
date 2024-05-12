import asyncio
from datetime import datetime, timedelta, timezone
import importlib
import json
import os
import urllib.parse

from openai import OpenAI
from google.auth.transport.requests import Request
from google.cloud import storage
from google.cloud import secretmanager
from google.oauth2 import service_account
from openai import OpenAI

from logger_config import logger


class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)


class CredentialManager:
    @staticmethod
    def get_secret(secret_id, project_id):
        """ Google Cloud Secret Manager からシークレットを取得 """
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode('UTF-8')

    @staticmethod
    def get_credentials(secret_id, project_id):
        """ シークレットからサービスアカウントの認証情報を生成 """
        secret_data = CredentialManager.get_secret(secret_id, project_id)
        service_account_info = json.loads(secret_data)
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=['https://www.googleapis.com/auth/cloud-platform'])
        if not credentials.valid:
            credentials.refresh(Request())
        return credentials


class SignedURLGenerator:
    @classmethod
    async def async_generate_signed_url(cls, bucket_name, object_name, expiration_seconds, SignedURL_credentials):
        # ストレージクライアントをセットアップ
        storage_client = storage.Client(
            project=os.getenv('PROJECT_ID'), credentials=SignedURL_credentials)
        # storage_client = storage.Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(object_name)

        # 有効期限を設定
        expiration = datetime.now(timezone.utc) + \
            timedelta(seconds=expiration_seconds)

        # 署名付きURLを生成するための関数をラップし、非同期で実行
        loop = asyncio.get_running_loop()
        signed_url = await loop.run_in_executor(
            None,  # Noneはデフォルトのエグゼキュータを使用することを意味します
            blob.generate_signed_url,
            expiration
        )
        return signed_url


def get_class_by_name(module_name, class_name):
    # モジュールをロード
    module = importlib.import_module(module_name)

    # クラスを取得し、返す
    return getattr(module, class_name)
