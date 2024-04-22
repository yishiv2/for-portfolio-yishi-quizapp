from fastapi import HTTPException
from google.cloud import firestore
from google.api_core.exceptions import GoogleAPIError

from logger_config import logger

# Firestoreクライアントのグローバルインスタンス
try:
    db = firestore.Client()
    logger.info("Firestore client initialized successfully")
except GoogleAPIError as e:
    logger.error("Failed to initialize Firestore client", exc_info=True)
    db = None


# Firestoreコレクションを取得するための依存関数
def get_firestore_collection(collection_name: str) -> firestore.CollectionReference:
    def dependency():
        if db is None:
            logger.error("Firestore client is not initialized")
            raise HTTPException(
                status_code=500, detail="Internal server error: Firestore client is not available")
        try:
            collection = db.collection(collection_name)
            # logger.info(f"Accessed collection: {collection_name}")
            return collection
        except GoogleAPIError as e:
            logger.error(f"Failed to access collection {
                         collection_name}", exc_info=True)
            raise HTTPException(
                status_code=500, detail="Internal server error: could not access Firestore collection")
    return dependency


# トランザクションに使用するためのFirestoreクライアントを取得する依存関数
def get_firestore_client() -> firestore.Client:
    return db
