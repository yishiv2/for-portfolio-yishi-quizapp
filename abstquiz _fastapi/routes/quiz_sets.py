from datetime import datetime, timezone
import os
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pytz import timezone
from google.cloud import firestore

from schemas.quiz_sets import QuizSetResponse, QuizSetResponse, QuizSetCreateRequest
from database import get_firestore_collection, get_firestore_client
from logger_config import logger
from crud.quiz_set import fetch_quiz_sets, add_quiz_set, delete_quiz_set
from const import QUIZZES_COLLCTION_NAME, QUIZ_SETS_COLLCTION_NAME
from services.quiz_generate import QuizGeneratorFacade
from crud.quiz import create_quiz


router = APIRouter(prefix="/quizsets", tags=["QuizSets"])


# @router.post("", response_model=QuizSetResponse)
# async def create_quiz_set(
#     quiz_set_data: QuizSetCreateRequest,
#     db: firestore.Client = Depends(get_firestore_client),
#     quiz_sets_collection: any = Depends(get_firestore_collection(QUIZ_SETS_COLLCTION_NAME)),
#     quizzes_collection: any = Depends(get_firestore_collection(QUIZZES_COLLCTION_NAME))
# ):
#     try:
#         jst = timezone('Asia/Tokyo')
#         current_time = datetime.now(jst)
#         quiz_set_info = {
#             "title": quiz_set_data.title,
#             "category": quiz_set_data.category,
#             "tag": quiz_set_data.tag,
#             "creater": quiz_set_data.user_id,
#             "updater": quiz_set_data.user_id,
#             "created_at": current_time,
#             "updated_at": current_time,
#         }
#         transaction = db.transaction()
#         quiz_set_id = add_quiz_set_and_quizzes(transaction, quiz_sets_collection, quizzes_collection, quiz_set_info, quiz_set_data.quizzes)

#         return QuizSetResponse(id=quiz_set_id, **quiz_set_info)
#     except Exception as e:
#         logger.error(f"Failed to create quiz set: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail="Failed to create quiz set")


@router.post("", response_model=QuizSetResponse)
async def create_quiz_set(
    quiz_set_data: QuizSetCreateRequest,
    quiz_title_list: List[str] = [],
    db: firestore.Client = Depends(get_firestore_client),
    quiz_sets_collection: any = Depends(
        get_firestore_collection(QUIZ_SETS_COLLCTION_NAME)),
    quizzes_collection: any = Depends(
        get_firestore_collection(QUIZZES_COLLCTION_NAME)),
    # current_user: dict = Depends(get_current_user)
    current_user: str = "1"  # 未実装のため、仮の値を設定
):
    try:
        jst = timezone('Asia/Tokyo')
        current_time = datetime.now(jst)

        # クイズセット情報を作成する
        quiz_set_info = {
            "title": quiz_set_data.title,
            "category": quiz_set_data.category,
            "tag": quiz_set_data.tag,
            "creater": current_user,
            "updater": current_user,
            "created_at": current_time,
            "updated_at": current_time,
        }
        quiz_set_id = add_quiz_set(quiz_sets_collection, quiz_set_info)

        failed_quiz_title_list = []  # 生成に失敗したクイズタイトルのリスト
        api_key = os.environ.get('OPENAI_API_KEY')
        quiz_generator = QuizGeneratorFacade(api_key)

        # openaiを使用してクイズを生成する
        for quiz_title in quiz_title_list:
            try:
                quiz_details = quiz_generator.generate_complete_quiz(
                    quiz_title)
                quiz_details.update({
                    "quiz_set_id": quiz_set_id,
                    "created_at": current_time,
                    "updated_at": current_time,
                    "creater": current_user,
                    "updater": current_user
                })
                create_quiz(quizzes_collection, quiz_details,
                            quiz_set_data.title)
                logger.info(f"created quiz({quiz_title})")
            except Exception as e:
                logger.error(f"Failed to create quiz({quiz_title}): {
                             str(e)}", exc_info=True)
                failed_quiz_title_list.append(quiz_title)

        if len(failed_quiz_title_list) == len(quiz_title_list):
            # クイズの生成に全て失敗した場合、クイズセットを削除(ロールバック)
            logger.error("Failed to create all quizzes. Deleting quiz set...")
            delete_quiz_set(quiz_sets_collection, quiz_set_id)

        return QuizSetResponse(id=quiz_set_id, **quiz_set_info)
    except Exception as e:
        logger.error(f"Failed to create quiz set: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to create quiz set")


@router.get("", response_model=List[QuizSetResponse])
async def get_quiz_sets(
    collection: any = Depends(
        get_firestore_collection(QUIZ_SETS_COLLCTION_NAME)),
    category: Optional[str] = None,
    tag: Optional[str] = None,
    start: Optional[str] = None,
    limit: int = Query(default=10, ge=1, le=100)
):
    try:
        items = fetch_quiz_sets(collection, category, tag, start, limit)
        return [QuizSetResponse(**item) for item in items]
    except HTTPException as e:
        logger.error(f"HTTP error occurred: {e.detail}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred while fetching quiz sets.")
    except Exception as e:
        # 予期せぬエラーのログを記録
        logger.error(f"Unexpected error occurred: {str(e)}", exc_info=True)
        # クライアントには汎用的なエラーメッセージを返す
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred while fetching quiz sets.")
