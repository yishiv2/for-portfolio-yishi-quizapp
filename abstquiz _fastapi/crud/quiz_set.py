import os
from typing import List

from fastapi import HTTPException
from google.cloud.firestore import CollectionReference, transactional, Transaction

from schemas.quiz import QuizCreateRequest
from logger_config import logger


def fetch_quiz_sets(collection: CollectionReference, category=None, tags=None, start=None, limit=10) -> list:
    try:
        query = collection

        if category:
            query = query.where('category', '==', category)
        if tags:
            for tag in tags:
                query = query.where('tag', '==', tag)
        if start:
            document = collection.document(start)
            query = query.start_after(document)

        query = query.limit(limit)
        results = query.stream()
        quizzes = [{**doc.to_dict(), 'id': doc.id} for doc in results]
        return quizzes
    except Exception as e:
        logger.error(f"Error fetching quiz sets: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching quiz sets.")


def add_quiz_set(collection: CollectionReference, quiz_set_info: dict) -> str:
    try:
        doc_ref = collection.add(quiz_set_info)
        # 追加されたドキュメントのIDを返す
        return doc_ref[1].id
    except Exception as e:
        logger.error(f"Error creating quiz sets: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An error occurred while creating quiz sets.")


def delete_quiz_set(collection: CollectionReference, quiz_set_id: str) -> None:
    try:
        doc_ref = collection.document(quiz_set_id)
        doc_ref.delete()
    except Exception as e:
        logger.error(f"Error deleting quiz set: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting quiz set.")


# @transactional
# def add_quiz_set_and_quizzes(
#     transaction: Transaction,
#     quiz_sets_collection: CollectionReference,
#     quizzes_collection: CollectionReference,
#     quiz_set_info: dict[str, any],
#     quizzes: List[QuizCreateRequest]
# ) -> str:
#     try:
#         # 新しいドキュメント参照を生成
#         quiz_set_ref = quiz_sets_collection.document()
#         # トランザクションを使って新しいクイズセットを追加
#         transaction.set(quiz_set_ref, quiz_set_info)
#         quiz_set_id = quiz_set_ref.id

#         for quiz in quizzes:
#             quiz_info = quiz.dict()
#             quiz_info.update({
#                 "quiz_set_id": quiz_set_id,
#                 "created_at": quiz_set_info['created_at'],
#                 "updated_at": quiz_set_info['updated_at'],
#                 "creater": quiz_set_info['creater'],
#                 "updater": quiz_set_info['updater']
#             })
#             # 各クイズのための新しいドキュメント参照を生成
#             quiz_doc_ref = quizzes_collection.document()
#             # トランザクションを使用してクイズを追加
#             transaction.set(quiz_doc_ref, quiz_info)

#         return quiz_set_id
#     except Exception as e:
#         logger.error(f"クイズセットとクイズの追加に失敗しました: {str(e)}", exc_info=True)
#         raise
