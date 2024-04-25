from datetime import datetime, timedelta, timezone
import importlib
import os

from openai import OpenAI
from google.cloud import storage
from google.cloud import secretmanager
from google.oauth2 import service_account
from openai import OpenAI


class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)


class SignedURLGenerator:
    @classmethod
    def generate_signed_url(cls, bucket_name, destination_blob_name, expiration_time):
        # Secret Managerからサービスアカウントキーを取得
        credentials_json = cls.get_secret()

        # 文字列から直接認証情報を作成
        credentials = service_account.Credentials.from_service_account_info(
            credentials_json)

        # ストレージクライアントを初期化
        storage_client = storage.Client(credentials=credentials)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # 有効期限を設定
        expiration = datetime.now(timezone.utc) + \
            timedelta(hours=expiration_time)

        # 署名付きURLを生成
        signed_url = blob.generate_signed_url(expiration=expiration)
        return signed_url

    @classmethod
    def get_secret(cls):
        # Secret Managerクライアントの初期化
        client = secretmanager.SecretManagerServiceClient()

        project_id = os.environ.get("PROJECT_ID")
        secretmanager_locate = f"projects/{
            project_id}/secrets/key/versions/latest"

        # Secret Managerから秘密情報を取得
        response = client.access_secret_version(
            request={"name": secretmanager_locate})
        secret_string = response.payload.data.decode("UTF-8")

        # JSON文字列をPythonの辞書に変換
        return eval(secret_string)


def get_class_by_name(module_name, class_name):
    # モジュールをロード
    module = importlib.import_module(module_name)

    # クラスを取得し、返す
    return getattr(module, class_name)
