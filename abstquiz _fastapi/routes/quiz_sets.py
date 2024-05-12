
from schemas.auth import DecodedToken
from typing import Annotated
import asyncio
from crud.quiz_set import check_quiz_set, update_quiz_set
from services.common import OpenAIClient
from services.quiz_set_generate import ConceptGenerator
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
from crud.quiz import create_quiz_async
from const import QUIZZES_COLLCTION_NAME, QUIZ_SETS_COLLCTION_NAME
# from crud.quiz import create_quiz
from services.quiz_generate import QuizGeneratorFacade

from services.common import get_class_by_name
from crud.auth import get_current_user


router = APIRouter(prefix="/quizsets", tags=["QuizSets"])
UserDependency = Annotated[DecodedToken, Depends(get_current_user)]


# @router.post("", response_model=QuizSetResponse)
# async def create_quiz_set(
#     user: UserDependency,
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
    user: UserDependency,
    quiz_set_data: QuizSetCreateRequest,
    quiz_title_list: List[str] = [],
    db: firestore.Client = Depends(get_firestore_client),
    quiz_sets_collection: any = Depends(
        get_firestore_collection(QUIZ_SETS_COLLCTION_NAME)),
    quizzes_collection: any = Depends(
        get_firestore_collection(QUIZZES_COLLCTION_NAME)),
    # current_user: dict = Depends(get_current_user)
    current_user: str = "1",  # 未実装のため、仮の値を設定
    prompt_type: str = "PromptGenerator"
):
    try:
        jst = timezone('Asia/Tokyo')
        current_time = datetime.now(jst)

        # 同じタイトルのクイズセットが存在するか確認
        quiz_set_id = check_quiz_set(quiz_sets_collection, quiz_set_data.title)
        if quiz_set_id:
            # すでに同じタイトルのクイズセットが存在する場合、updateを行う
            logger.info(
                f"Quiz set with the same title already exists. Updating quiz set...")

            # 更新するクイズセットの情報を作成
            quiz_set_info = {
                "title": quiz_set_data.title,
                "updater": current_user,
                "updated_at": current_time,
            }
            if quiz_set_data.tag:
                quiz_set_info.update({"tag": quiz_set_data.tag})
            if quiz_set_data.category:
                quiz_set_info.update({"category": quiz_set_data.category})

            update_quiz_set(quiz_sets_collection, quiz_set_id, quiz_set_info)

        else:
            # すでに同じタイトルのクイズセットが存在しない場合、新規作成を行う
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

        # 生成する画像のタイプを指定
        try:
            PromptGeneratorClass = get_class_by_name(
                "services.quiz_generate", prompt_type)
        except Exception as e:
            logger.error(f"Failed to get prompt_type_class by name: {
                         str(e)}", exc_info=True)
            raise HTTPException(
                status_code=400, detail="No such prompt_type_class by name")

        # 以降でクイズを作成する,openaiのレートリミットの変動を考慮してバッチ処理
        sleep_time = 30
        batch_size = 5
        batches = [quiz_title_list[i:i + batch_size]
                   for i in range(0, len(quiz_title_list), batch_size)]

        for quiz_title_list in batches:
            tasks = [fetch_and_create_quiz(quiz_title, quiz_set_id, current_time, current_user, quizzes_collection, quiz_set_info["title"])
                     for quiz_title in quiz_title_list]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            failed_quiz_title_list = [
                title for title, error in results if error]

            await asyncio.sleep(sleep_time)

        if len(failed_quiz_title_list) == len(quiz_title_list):
            logger.error("Failed to create all quizzes. Deleting quiz set...")
            await delete_quiz_set(quiz_sets_collection, quiz_set_id)

        return QuizSetResponse(id=quiz_set_id, **quiz_set_info)
    except Exception as e:
        logger.error(f"Failed to create quiz set: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to create quiz set")


async def fetch_and_create_quiz(quiz_title, quiz_set_id, current_time, current_user, quizzes_collection, quiz_set_title):
    try:
        # クイズの非同期生成
        quiz_generator_type = get_class_by_name(
            "services.quiz_generate", "PromptGenerator")
        quiz_generator = QuizGeneratorFacade(quiz_generator_type)

        quiz_details = await quiz_generator.generate_complete_quiz(quiz_title)
        quiz_details.update({
            "quiz_set_id": quiz_set_id,
            "created_at": current_time,
            "updated_at": current_time,
            "creater": current_user,
            "updater": current_user
        })
        # 非同期でFirestoreにデータを挿入
        await create_quiz_async(quizzes_collection, quiz_details, quiz_set_title)
        return quiz_title, None
    except Exception as e:
        logger.error(f"Failed to create quiz({quiz_title}): {
                     str(e)}", exc_info=True)
        return quiz_title, e


@router.get("", response_model=List[QuizSetResponse])
async def get_quiz_sets(
    user: UserDependency,
    collection: any = Depends(
        get_firestore_collection(QUIZ_SETS_COLLCTION_NAME)),
    category: Optional[str] = None,
    tag: Optional[str] = None,
    title: Optional[str] = None,
    start: Optional[str] = None,
    limit: int = Query(default=100, ge=1, le=100)

):
    try:
        items = fetch_quiz_sets(collection, category, tag, title, start, limit)
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


@router.get("/concepts", response_model=List[str])  # レスポンスの型を指定
async def get_concepts(
    user: UserDependency,
    quiz_set_title: str,
    num: int = Query(default=10, ge=1, le=100),
):
    try:
        api_key = os.environ.get('OPENAI_API_KEY')
        concepts = ConceptGenerator(OpenAIClient(
            api_key)).generate_concepts(quiz_set_title, num)
        return concepts
    except Exception as e:
        logger.error(f"Failed to generate concepts: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to generate concepts")
