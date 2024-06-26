
import os


if os.getenv('gcp') is None:
    from dotenv import load_dotenv
    load_dotenv()

QUIZZES_COLLCTION_NAME = os.environ['QUIZZES_COLLCTION_NAME']
QUIZ_SETS_COLLCTION_NAME = os.environ['QUIZ_SETS_COLLCTION_NAME']
QUIZ_USER_COLLCTION_NAME = os.environ['QUIZ_USER_COLLCTION_NAME']
# 署名付きURLの有効期限
SIGNED_URL_EXPIRATION = 1200


# type_of_prompt_generator_dict = {1: MoeKyaraPromptGenerator,
#                                  2: MinimalismPromptGenerator,
#                                  3: GradientPaintingPromptGenerator,
#                                  4: AvantGardePromptGenerator,
#                                  5: InstallationArtPromptGenerator,
#                                  6: SurrealismPromptGenerator,
#                                  7: CubismPromptGenerator,
#                                  8: RealismPromptGenerator,
#                                  9: ImpressionismPromptGenerator,
#                                  10: LikeAbstractPaintingPromptGenerator,
#                                  11: GenrePaintingPaintingPromptGenerator}
