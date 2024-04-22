import logging


def setup_logger():
    """ロガーの設定を行う関数"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger('QuizAppLogger')
    return logger


logger = setup_logger()
