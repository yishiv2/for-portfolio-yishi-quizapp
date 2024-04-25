from abc import ABC, abstractmethod
from datetime import datetime
from io import BytesIO

import requests
from google.cloud import storage
from PIL import Image

from logger_config import logger


# 画像変換のための抽象クラス
class ImageTransformer(ABC):
    @abstractmethod
    def transform(self, image_data: bytes, size: tuple = None) -> BytesIO:
        """
        画像データを特定の形式に変換し、オプションでリサイズするメソッド。

        :param image_data: ダウンロードされた原始的な画像データ。
        :param size: リサイズ後の画像のサイズ (幅, 高さ)。
        :return: 変換（およびリサイズ）後の画像データが格納されたBytesIOオブジェクト。
        """
        pass


# WebP形式へ変換する具体的なクラス
class WebPTransformer(ImageTransformer):
    def transform(self, image_data: bytes, size: tuple = None) -> BytesIO:
        """
        入力された画像データをWebP形式に変換し、指定されたサイズにリサイズします。

        :param image_data: バイナリ形式の画像データ。
        :param size: リサイズする場合の新しいサイズ (幅, 高さ)。
        :return: WebP形式およびリサイズされた画像データが格納されたBytesIOオブジェクト。
        """
        image = Image.open(BytesIO(image_data))
        if size:
            image = image.resize(size, Image.ANTIALIAS)  # リサイズ処理
        output_stream = BytesIO()
        image.save(output_stream, format='WEBP')
        output_stream.seek(0)
        return output_stream


# 画像処理およびアップロードを管理するクラス
class ImageProcessor:
    def __init__(self, bucket_name: str, transformer: ImageTransformer):
        """
        ImageProcessorのコンストラクタ。

        :param bucket_name: 画像をアップロードするGoogle Cloud Storageのバケット名。
        :param transformer: 画像変換を担当するTransformerオブジェクト。
        """
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.transformer = transformer

    def upload_image_to_storage(self, image_url: str, destination_blob_name: str) -> str:
        """
        指定されたURLから画像をダウンロードし、変換後にGoogle Cloud Storageにアップロードします。

        :param image_url: ダウンロードする画像のURL。
        :param destination_blob_name: アップロード後のバケット内でのファイル名。
        :return: アップロードされた画像の公開URL。
        """
        try:
            response = requests.get(image_url)
            response.raise_for_status()

            transformed_image_stream = self.transformer.transform(
                response.content)

            destination_blob_name += datetime.now().strftime('%Y%m%d%H%M%S') + '.webp'
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_file(transformed_image_stream,
                                  content_type='image/webp')

            return destination_blob_name
        except Exception as e:
            logger.error(f"Failed to upload image to storage: {
                         str(e)}", exc_info=True)
            raise

    def delete_blob(self, blob_name):
        """
        Google Cloud Storageから特定のファイルを削除します。
        """
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()
        except Exception as e:
            logger.error(f"Failed to delete blob({blob_name}): {
                         str(e)}", exc_info=True)
            raise
