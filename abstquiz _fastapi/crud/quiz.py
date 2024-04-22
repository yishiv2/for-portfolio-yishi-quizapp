import os
from typing import List

from fastapi import HTTPException
from google.cloud.firestore import CollectionReference, DocumentReference

from logger_config import logger
from services.image_processing import ImageProcessor, WebPTransformer


def create_quiz(collection: CollectionReference, quiz_data: dict, quiz_set_title: str) -> DocumentReference:
    """
    Args:
        collection (CollectionReference): Firestoreのコレクション参照
        quiz_data (dict): クイズデータ
        image_url (str): 画像URL
        quiz_set_title (str): クイズセットのタイトル
    """
    try:
        bucket_name = os.environ.get('STORAGE_BUCKET_NAME')
        destination_blob_name = f"{quiz_set_title}/{quiz_data['answer']}"

        # cloud storageに追加
        # uploaded_iamge_url = upload_image_to_storage(quiz_data["image"], bucket_name, destination_blob_name)
        image_processor = ImageProcessor(f'{bucket_name}', WebPTransformer())

        uploaded_iamge_url = image_processor.upload_image_to_storage(
            quiz_data["image"], destination_blob_name)
        quiz_data['image'] = uploaded_iamge_url  # 画像URLを更新

        # クイズデータをdbに追加
        try:
            # addメソッドからドキュメント参照と書き込み結果をアンパック
            _, doc_ref = collection.add(quiz_data)
        except Exception as e:
            # クイズデータの追加に失敗した場合、画像を削除
            image_processor.delete_blob(destination_blob_name)
            logger.error(f"Failed to create new quiz: {str(e)}", exc_info=True)

        return doc_ref

    except Exception as e:
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


def fetch_quizzes_by_set_id(collection, quiz_set_id):
    try:
        query = collection.where("quiz_set_id", "==", quiz_set_id)
        results = query.stream()
        quizzes = []
        for doc in results:
            quiz = get_and_validate_quiz(doc.reference)
            quizzes.append(quiz)
        return quizzes
    except Exception as e:
        logger.error(f"Failed to fetch quizzes for quiz_set_id {
                     quiz_set_id}: {str(e)}", exc_info=True)
        raise


def fetch_all_quizzes(collection: CollectionReference) -> List[dict]:
    try:
        results = collection.stream()
        quizzes = []
        for doc in results:
            quiz = get_and_validate_quiz(doc.reference)
            quizzes.append(quiz)
        return quizzes
    except Exception as e:
        logger.error(f"Failed to fetch all quizzes: {str(e)}", exc_info=True)
        raise


def fetch_quiz_detail(collection: CollectionReference, quiz_id) -> dict:
    try:
        doc_ref = collection.document(quiz_id)
        return get_and_validate_quiz(doc_ref)
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
        return get_and_validate_quiz(doc_ref)
    except Exception as e:
        logger.error(f"Failed to update quiz details for quiz_id {
                     quiz_id}: {str(e)}", exc_info=True)
        raise


def delete_quiz_item(collection: CollectionReference, quiz_id) -> None:
    try:
        collection.document(quiz_id).delete()
    except Exception as e:
        raise


# ドキュメント参照からクイズデータを取得し整形する、存在しない場合はエラーを返す
def get_and_validate_quiz(doc_ref: DocumentReference) -> dict:
    quiz_doc = doc_ref.get()
    if not quiz_doc.exists:
        raise HTTPException(
            status_code=404, detail="Failed to retrieve the created quiz")
    quiz = quiz_doc.to_dict()
    quiz['id'] = quiz_doc.id  # ドキュメントIDを追加
    return quiz
