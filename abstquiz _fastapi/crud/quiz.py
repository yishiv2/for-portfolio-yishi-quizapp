from google.cloud.firestore_v1 import FieldFilter
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from typing import List


from fastapi import HTTPException
from google.cloud.firestore import CollectionReference, DocumentReference

from const import SIGNED_URL_EXPIRATION
from logger_config import logger
from services.image_processing import ImageProcessor, WebPTransformer
from services.common import SignedURLGenerator


# def create_quiz(collection: CollectionReference, quiz_data: dict, quiz_set_title: str) -> DocumentReference:
#     """
#     Args:
#         collection (CollectionReference): Firestoreのコレクション参照
#         quiz_data (dict): クイズデータ
#         image_url (str): 画像URL
#         quiz_set_title (str): クイズセットのタイトル
#     """
#     try:
#         bucket_name = os.environ.get('STORAGE_BUCKET_NAME')
#         destination_blob_name = f"{quiz_set_title}/{quiz_data['answer']}"

#         # cloud storageに追加
#         # uploaded_iamge_url = upload_image_to_storage(quiz_data["image"], bucket_name, destination_blob_name)
#         image_processor = ImageProcessor(f'{bucket_name}', WebPTransformer())

#         destination_blob_name = image_processor.upload_image_to_storage(
#             quiz_data["image"], destination_blob_name)

#         quiz_data['image'] = destination_blob_name  # 画像URLを更新

#         # クイズデータをdbに追加
#         try:
#             # addメソッドからドキュメント参照と書き込み結果をアンパック
#             _, doc_ref = collection.add(quiz_data)
#         except Exception as e:
#             # クイズデータの追加に失敗した場合、画像を削除
#             image_processor.delete_blob(destination_blob_name)
#             logger.error(f"Failed to create new quiz: {str(e)}", exc_info=True)

#         return doc_ref

#     except Exception as e:
#         logger.error(f"Failed to create new quiz: {str(e)}", exc_info=True)
#         raise HTTPException(
#             status_code=500, detail="Failed to create new quiz")

async def create_quiz_async(collection: CollectionReference, quiz_data: dict, quiz_set_title: str):
    try:
        bucket_name = os.environ.get('STORAGE_BUCKET_NAME')
        destination_blob_name = f"{quiz_set_title}/{quiz_data['answer']}"

        image_processor = ImageProcessor(bucket_name, WebPTransformer)

        destination_blob_name = await image_processor.upload_image_to_storage_async(
            quiz_data["image"], destination_blob_name)

        quiz_data['image'] = destination_blob_name

        # Firestoreにデータを追加
        loop = asyncio.get_running_loop()
        doc_ref = await loop.run_in_executor(
            None,
            collection.add,
            quiz_data
        )
        return doc_ref

    except Exception as e:
        await image_processor.delete_blob_async(destination_blob_name)
        logger.error(f"Failed to create new quiz: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to create new quiz")


def create_quiz_in_db(collection: CollectionReference, quiz_data: dict) -> DocumentReference:
    try:
        # クイズデータを新規作成
        # addメソッドからドキュメント参照と書き込み結果をアンパック
        _, doc_ref = collection.add(quiz_data)
        return doc_ref
    except Exception as e:
        logger.error(f"Failed to create new quiz: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to create new quiz")


# def fetch_quizzes_by_set_id(collection, quiz_set_id):
#     try:
#         query = collection.where("quiz_set_id", "==", quiz_set_id)
#         results = query.stream()
#         quizzes = []
#         for doc in results:
#             quiz = get_and_validate_quiz(doc.reference)
#             quizzes.append(quiz)
#         return quizzes
#     except Exception as e:
#         logger.error(f"Failed to fetch quizzes for quiz_set_id {
#                      quiz_set_id}: {str(e)}", exc_info=True)
#         raise


async def fetch_quizzes_by_set_id(collection, quiz_set_id):
    try:

        query = collection.where(filter=FieldFilter(
            "quiz_set_id", "==", quiz_set_id))

        results = query.stream()
        quizzes = add_ids_to_quizzes_from_results(results)
        quizzes = await update_quizzes_with_signed_urls(quizzes)
        return quizzes
    except Exception as e:
        logger.error(f"Failed to fetch quizzes for quiz_set_id {
                     quiz_set_id}: {str(e)}", exc_info=True)
        return []


async def fetch_all_quizzes(collection):
    try:
        results = collection.stream()  # 全ドキュメントを取得するためのクエリ
        quizzes = add_ids_to_quizzes_from_results(results)
        quizzes = await update_quizzes_with_signed_urls(quizzes)
        return quizzes

    except Exception as e:
        logger.error(f"Failed to fetch quizzes: {str(e)}", exc_info=True)
        return []


async def fetch_quiz_detail(collection: CollectionReference, quiz_id) -> dict:
    try:
        doc_ref = collection.document(quiz_id)
        quizees = add_ids_to_quizzes_from_results([doc_ref.get()])
        return quizees[0]
    except Exception as e:
        logger.error(f"Failed to fetch quiz details for quiz_id {
                     quiz_id}: {str(e)}", exc_info=True)
        raise


# Todo 後で、更新者、更新日時を追加する様に修正
def update_quiz_detail(collection: CollectionReference, quiz_id, update_data) -> dict:
    try:
        doc_ref = collection.document(quiz_id)
        # 最初にドキュメントの存在を確認
        initial_quiz = doc_ref.get()
        if not initial_quiz.exists:
            raise ValueError("Quiz not found")
        doc_ref.update(update_data)
        # 更新されたドキュメントを取得し、整形
        return add_ids_to_quizzes_from_results([doc_ref.get()])
    except Exception as e:
        logger.error(f"Failed to update quiz details for quiz_id {
                     quiz_id}: {str(e)}", exc_info=True)
        raise


def delete_quiz_item(collection: CollectionReference, quiz_id) -> None:
    try:
        collection.document(quiz_id).delete()
    except Exception as e:
        raise


# # ドキュメント参照からクイズデータを取得し整形する、存在しない場合はエラーを返す
# def get_and_validate_quiz(doc_ref: DocumentReference) -> dict:
#     quiz_doc = doc_ref.get()
#     if not quiz_doc.exists:
#         raise HTTPException(
#             status_code=404, detail="Failed to retrieve the created quiz")
#     quiz = quiz_doc.to_dict()
#     quiz['id'] = quiz_doc.id  # ドキュメントIDを追加
#     # 署名付きURLで返す。
#     quiz["image"] = SignedURLGenerator.generate_signed_url(
#         os.environ.get('STORAGE_BUCKET_NAME'), quiz["image"], 600)
#     return quiz


# ドキュメント参照からクイズデータを取得し整形する、存在しない場合はエラーを返す

# async def get_and_validate_quiz(doc_ref):
#     loop = asyncio.get_running_loop()
#     with ThreadPoolExecutor() as pool:
#         quiz_doc = await loop.run_in_executor(pool, doc_ref.get)
#         if not quiz_doc.exists:
#             raise HTTPException(
#                 status_code=404, detail="Failed to retrieve the created quiz")
#         quiz = quiz_doc.to_dict()
#         quiz['id'] = quiz_doc.id
#         return quiz

def add_ids_to_quizzes_from_results(results):
    quizzes = []
    for doc in results:
        quiz_data = doc.to_dict()
        quiz_data['id'] = doc.id  # ドキュメントIDを追加
        quizzes.append(quiz_data)
    return quizzes


async def update_quizzes_with_signed_urls(quizzes):
    tasks = []
    for quiz in quizzes:
        if "image" in quiz:
            task = SignedURLGenerator.async_generate_signed_url(
                os.environ.get(
                    'STORAGE_BUCKET_NAME'), quiz["image"], SIGNED_URL_EXPIRATION
            )
            tasks.append(task)
        else:
            # イメージが存在しない場合は None または適当なデフォルト値を追加
            tasks.append(None)

    signed_urls = await asyncio.gather(*tasks, return_exceptions=True)

    # 署名付きURLをクイズのリストに割り当てる
    for quiz, result in zip(quizzes, signed_urls):
        if isinstance(result, Exception):
            # 例外が発生した場合、その詳細をログに出力
            logger.error(f"Error generating signed URL for {
                         quiz['image']}: {result}")
            quiz["image"] = None  # エラーがあった場合はNoneを設定
        else:
            quiz["image"] = result

    return quizzes
