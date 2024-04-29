from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from pytz import timezone

from schemas.quiz import QuizCreateRequest, QuizResponse, QuizDetailResponse, QuizUpdateRequest
from crud.quiz import (fetch_quiz_detail, update_quiz_detail, delete_quiz_item, fetch_all_quizzes,
                       fetch_quizzes_by_set_id, create_quiz_in_db, add_ids_to_quizzes_from_results)
from database import get_firestore_collection
from logger_config import logger
from const import QUIZZES_COLLCTION_NAME


router = APIRouter(prefix="/quiz", tags=["Question"])


# 問題を作成するAPIエンドポイント
@router.post("", response_model=QuizResponse)
async def create_quiz_item(quiz_data: QuizCreateRequest, collection: any = Depends(get_firestore_collection(QUIZZES_COLLCTION_NAME))):
    try:
        jst = timezone('Asia/Tokyo')
        current_time = datetime.now(jst)
        # quiz_dataからuser_idを除外し、新しいデータセットを作成
        insert_quiz_data = quiz_data.dict(exclude={"user_id"})
        # 必要な新しいフィールドを追加
        insert_quiz_data.update({
            "creater": quiz_data.user_id,
            "updater": quiz_data.user_id,
            "created_at": current_time,
            "updated_at": current_time
        })
        # Firestoreにクイズを新規作成
        doc_ref = create_quiz_in_db(collection, insert_quiz_data)
        # Firestoreから作成されたクイズを取得し、検証
        quiz = add_ids_to_quizzes_from_results(doc_ref)
        return QuizResponse(**quiz)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to create new quiz: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to create new quiz")


# 特定の問題セットに属する問題を取得
@router.get("/{quiz_set_id}", response_model=List[QuizResponse])
async def get_quizzes_by_set(quiz_set_id: str, collection: any = Depends(get_firestore_collection(QUIZZES_COLLCTION_NAME))):
    try:
        quizzes = await fetch_quizzes_by_set_id(collection, quiz_set_id)
        if not quizzes:
            logger.error(f"No quizzes found for quiz set ID: {quiz_set_id}")
            raise HTTPException(
                status_code=404, detail="No quizzes found for this quiz set.")
        return [QuizResponse(**quiz) for quiz in quizzes]
    except HTTPException as e:
        logger.warning(f"HTTP error occurred: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# 全ての問題データを取得
@router.get("", response_model=List[QuizResponse])
async def get_all_quizzes(collection: any = Depends(get_firestore_collection(QUIZZES_COLLCTION_NAME))):
    try:
        quizzes = await fetch_all_quizzes(collection)
        if quizzes:
            return [QuizResponse(**quiz) for quiz in quizzes]
        else:
            raise HTTPException(status_code=404, detail="No quizzes found")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error occurred while fetching all quizzes: {
                     str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred while fetching quizzes")


# 問題データを取得
@router.get("/detail/{quiz_id}", response_model=QuizDetailResponse)
async def get_quiz_detail(quiz_id: str, collection: any = Depends(get_firestore_collection(QUIZZES_COLLCTION_NAME))):
    try:
        print("quiz_id", quiz_id)
        item = fetch_quiz_detail(collection, quiz_id)
        if not item:
            raise HTTPException(status_code=404, detail="Quiz not found")
        return QuizDetailResponse(**item)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 問題を更新
@router.put("/{quiz_id}", response_model=QuizResponse)
async def update_quiz_item(quiz_id: str, update_data: QuizUpdateRequest, collection: any = Depends(get_firestore_collection(QUIZZES_COLLCTION_NAME))):
    try:
        jst = timezone('Asia/Tokyo')
        current_time = datetime.now(jst)
        # quiz_dataからuser_idを除外し、新しいデータセットを作成
        update_quiz_data = update_data.dict(exclude={"user_id"})
        # 必要な新しいフィールドを追加
        update_quiz_data.update({
            "updater": update_data.user_id,
            "updated_at": current_time
        })
        updated_quiz = update_quiz_detail(
            collection, quiz_id, update_quiz_data)
        return updated_quiz
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")


@router.delete("/{quiz_id}", status_code=204)
async def delete_quiz_item_api(quiz_id: str, collection: any = Depends(get_firestore_collection(QUIZZES_COLLCTION_NAME))):
    try:
        delete_quiz_item(collection, quiz_id)
        return {"detail": "Quiz deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error occurred while deleting quiz: {
                     str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred while deleting the quiz")
