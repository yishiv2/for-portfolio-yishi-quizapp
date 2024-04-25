import os
from google.oauth2 import service_account
from google.cloud import secretmanager
from abc import ABC, abstractmethod
from services.common import OpenAIClient
from logger_config import logger


class AbstractPromptGenerator(ABC):
    def __init__(self, openai_client):
        self.client = openai_client.client

    @abstractmethod
    def generate_prompt_from_title(self, title):
        pass


class PromptGenerator(AbstractPromptGenerator):
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_prompt_from_title(self, title):
        """問題タイトルに基づいて詳細な画像プロンプトを生成します。"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "次の指示に従って、指定された抽象的概念を強調して視覚した画像を生成するためのプロンプトを生成してください。プロンプトは、概念の深い意味や感情的な影響を視覚的に強調して表現するのに適している必要があります。"},
                    {"role": "user", "content": f"抽象的概念 '{title}' を強調して視覚した画像を生成できるような画像プロンプトを生成してください。このプロンプトは次の要素を含むものとします：\n"
                     "1. 第一印象：画像を見た人が'{title}'を直接的に想起できること。\n"
                     "2. '{title}'の本質：概念が象徴するものや、その影響が及ぼす環境。\n"
                     "3. 登場するオブジェクトや象徴：概念を表すメタフォリックなオブジェクトやキャラクター。\n"
                     "4. 情感や雰囲気：概念が引き起こす感情やムードを強調する要素。\n"
                     "5. 色と光の使用：概念の感情的または象徴的な意味を強化するための色彩や照明。\n"
                     "6. 形状や質感を強調：視覚化された概念の形状や質感。\n"

                     "このプロンプトは200文字から1000文字の範囲で、具体的で視覚的に豊かな説明を含むものにしてください。"}
                ],
                max_tokens=1000
            )
            # モデルの完了から望ましい内容と考えられる最後のメッセージを取得する
            messages = response.choices[0].message
            return messages.content
        except Exception as e:
            logger.error(
                f"Error occurred while generate_prompt_from_title: {e}")
            # 画像プロンプトがないと画像が生成できないためエラーにする
            raise


class MoeKyaraPromptGenerator(AbstractPromptGenerator):
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_prompt_from_title(self, title):
        """問題タイトルに基づいて萌えキャラ風な画像プロンプトを生成します。"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "指定された抽象的概念を萌えキャラで擬人化したかわいい画像を生成するためのプロンプトを生成してください。プロンプトは、概念の感情的な影響を視覚的に強調して表現するのに適している必要があります。"
                    },
                    {
                        "role": "user",
                        "content": f"抽象的概念 '{title}' を萌えキャラで擬人化し、「萌え」を強調したかわいい画像を生成できるようなプロンプトを生成してください。このプロンプトは次の要素を含むものとします：\n"
                        "1. 第一印象：画像を見た人が'{title}'を直接的に想起できる、かわいくて魅力的なキャラクターデザイン。\n"
                        "2. '{title}'の本質：概念が象徴するものや、その影響が及ぼす環境を表すキャラクターの特徴やアクセサリー。\n"
                        "3. 登場するオブジェクトや象徴：概念を表すメタフォリックなオブジェクトやキャラクターの小道具。\n"
                        "4. 情感や雰囲気：概念が引き起こす感情やムードを強調する表情や背景の雰囲気。\n"
                        "5. 色と光の使用：概念の感情的または象徴的な意味を強化するための鮮やかな色彩や柔らかい照明。\n"
                        "6. 形状や質感を強調：キャラクターの服装やアクセサリーのディテールによる視覚的な強調。\n"
                        "このプロンプトは200文字から1000文字の範囲で、具体的で視覚的に豊かな説明を含むものにしてください。"
                    }
                ],
                max_tokens=1000
            )
            # モデルの完了から望ましい内容と考えられる最後のメッセージを取得する
            messages = response.choices[0].message
            return messages.content
        except Exception as e:
            logger.error(
                f"Error occurred while generate_prompt_from_title: {e}")
            # 画像プロンプトがないと画像が生成できないためエラーにする
            raise


class MinimalismPromptGenerator(AbstractPromptGenerator):
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_prompt_from_title(self, title):
        """問題タイトルに基づいてミニマリズム風な画像プロンプトを生成します。"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "指定された抽象的概念を萌えキャラで擬人化したかわいい画像を生成するためのプロンプトを生成してください。プロンプトは、概念の感情的な影響を視覚的に強調して表現するのに適している必要があります。"
                    },
                    {
                        "role": "user",
                        "content": f"抽象的概念 '{title}' を萌えキャラで擬人化し、「萌え」を強調したかわいい画像を生成できるようなプロンプトを生成してください。このプロンプトは次の要素を含むものとします：\n"
                        "1. 第一印象：画像を見た人が'{title}'を直接的に想起できる、かわいくて魅力的なキャラクターデザイン。\n"
                        "2. '{title}'の本質：概念が象徴するものや、その影響が及ぼす環境を表すキャラクターの特徴やアクセサリー。\n"
                        "3. 登場するオブジェクトや象徴：概念を表すメタフォリックなオブジェクトやキャラクターの小道具。\n"
                        "4. 情感や雰囲気：概念が引き起こす感情やムードを強調する表情や背景の雰囲気。\n"
                        "5. 色と光の使用：概念の感情的または象徴的な意味を強化するための鮮やかな色彩や柔らかい照明。\n"
                        "6. 形状や質感を強調：キャラクターの服装やアクセサリーのディテールによる視覚的な強調。\n"
                        "このプロンプトは200文字から1000文字の範囲で、具体的で視覚的に豊かな説明を含むものにしてください。"
                    }
                ],
                max_tokens=1000
            )
            # モデルの完了から望ましい内容と考えられる最後のメッセージを取得する
            messages = response.choices[0].message
            return messages.content
        except Exception as e:
            logger.error(
                f"Error occurred while generate_prompt_from_title: {e}")
            # 画像プロンプトがないと画像が生成できないためエラーにする
            raise


class GradientPaintingPromptGenerator(AbstractPromptGenerator):
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_prompt_from_title(self, title):
        """問題タイトルに基づいてグラデーショナルペインティング風な画像プロンプトを生成します。"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "指定された抽象的概念を萌えキャラで擬人化したかわいい画像を生成するためのプロンプトを生成してください。プロンプトは、概念の感情的な影響を視覚的に強調して表現するのに適している必要があります。"
                    },
                    {
                        "role": "user",
                        "content": f"抽象的概念 '{title}' を萌えキャラで擬人化し、「萌え」を強調したかわいい画像を生成できるようなプロンプトを生成してください。このプロンプトは次の要素を含むものとします：\n"
                        "1. 第一印象：画像を見た人が'{title}'を直接的に想起できる、かわいくて魅力的なキャラクターデザイン。\n"
                        "2. '{title}'の本質：概念が象徴するものや、その影響が及ぼす環境を表すキャラクターの特徴やアクセサリー。\n"
                        "3. 登場するオブジェクトや象徴：概念を表すメタフォリックなオブジェクトやキャラクターの小道具。\n"
                        "4. 情感や雰囲気：概念が引き起こす感情やムードを強調する表情や背景の雰囲気。\n"
                        "5. 色と光の使用：概念の感情的または象徴的な意味を強化するための鮮やかな色彩や柔らかい照明。\n"
                        "6. 形状や質感を強調：キャラクターの服装やアクセサリーのディテールによる視覚的な強調。\n"
                        "このプロンプトは200文字から1000文字の範囲で、具体的で視覚的に豊かな説明を含むものにしてください。"
                    }
                ],
                max_tokens=1000
            )
            # モデルの完了から望ましい内容と考えられる最後のメッセージを取得する
            messages = response.choices[0].message
            return messages.content
        except Exception as e:
            logger.error(
                f"Error occurred while generate_prompt_from_title: {e}")
            # 画像プロンプトがないと画像が生成できないためエラーにする
            raise


class AvantGardePromptGenerator(AbstractPromptGenerator):
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_prompt_from_title(self, title):
        """問題タイトルに基づいてアバンギャルド風な画像プロンプトを生成します。"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "指定された抽象的概念を萌えキャラで擬人化したかわいい画像を生成するためのプロンプトを生成してください。プロンプトは、概念の感情的な影響を視覚的に強調して表現するのに適している必要があります。"
                    },
                    {
                        "role": "user",
                        "content": f"抽象的概念 '{title}' を萌えキャラで擬人化し、「萌え」を強調したかわいい画像を生成できるようなプロンプトを生成してください。このプロンプトは次の要素を含むものとします：\n"
                        "1. 第一印象：画像を見た人が'{title}'を直接的に想起できる、かわいくて魅力的なキャラクターデザイン。\n"
                        "2. '{title}'の本質：概念が象徴するものや、その影響が及ぼす環境を表すキャラクターの特徴やアクセサリー。\n"
                        "3. 登場するオブジェクトや象徴：概念を表すメタフォリックなオブジェクトやキャラクターの小道具。\n"
                        "4. 情感や雰囲気：概念が引き起こす感情やムードを強調する表情や背景の雰囲気。\n"
                        "5. 色と光の使用：概念の感情的または象徴的な意味を強化するための鮮やかな色彩や柔らかい照明。\n"
                        "6. 形状や質感を強調：キャラクターの服装やアクセサリーのディテールによる視覚的な強調。\n"
                        "このプロンプトは200文字から1000文字の範囲で、具体的で視覚的に豊かな説明を含むものにしてください。"
                    }
                ],
                max_tokens=1000
            )
            # モデルの完了から望ましい内容と考えられる最後のメッセージを取得する
            messages = response.choices[0].message
            return messages.content
        except Exception as e:
            logger.error(
                f"Error occurred while generate_prompt_from_title: {e}")
            # 画像プロンプトがないと画像が生成できないためエラーにする
            raise


class InstallationArtPromptGenerator(AbstractPromptGenerator):
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_prompt_from_title(self, title):
        """問題タイトルに基づいてインスタレーションアート風な画像プロンプトを生成します。"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "指定された抽象的概念を萌えキャラで擬人化したかわいい画像を生成するためのプロンプトを生成してください。プロンプトは、概念の感情的な影響を視覚的に強調して表現するのに適している必要があります。"
                    },
                    {
                        "role": "user",
                        "content": f"抽象的概念 '{title}' を萌えキャラで擬人化し、「萌え」を強調したかわいい画像を生成できるようなプロンプトを生成してください。このプロンプトは次の要素を含むものとします：\n"
                        "1. 第一印象：画像を見た人が'{title}'を直接的に想起できる、かわいくて魅力的なキャラクターデザイン。\n"
                        "2. '{title}'の本質：概念が象徴するものや、その影響が及ぼす環境を表すキャラクターの特徴やアクセサリー。\n"
                        "3. 登場するオブジェクトや象徴：概念を表すメタフォリックなオブジェクトやキャラクターの小道具。\n"
                        "4. 情感や雰囲気：概念が引き起こす感情やムードを強調する表情や背景の雰囲気。\n"
                        "5. 色と光の使用：概念の感情的または象徴的な意味を強化するための鮮やかな色彩や柔らかい照明。\n"
                        "6. 形状や質感を強調：キャラクターの服装やアクセサリーのディテールによる視覚的な強調。\n"
                        "このプロンプトは200文字から1000文字の範囲で、具体的で視覚的に豊かな説明を含むものにしてください。"
                    }
                ],
                max_tokens=1000
            )
            # モデルの完了から望ましい内容と考えられる最後のメッセージを取得する
            messages = response.choices[0].message
            return messages.content
        except Exception as e:
            logger.error(
                f"Error occurred while generate_prompt_from_title: {e}")
            # 画像プロンプトがないと画像が生成できないためエラーにする
            raise


class CubismPromptGenerator(AbstractPromptGenerator):
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_prompt_from_title(self, title):
        """問題タイトルに基づいてキュビズム風な画像プロンプトを生成します。"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "指定された抽象的概念を萌えキャラで擬人化したかわいい画像を生成するためのプロンプトを生成してください。プロンプトは、概念の感情的な影響を視覚的に強調して表現するのに適している必要があります。"
                    },
                    {
                        "role": "user",
                        "content": f"抽象的概念 '{title}' を萌えキャラで擬人化し、「萌え」を強調したかわいい画像を生成できるようなプロンプトを生成してください。このプロンプトは次の要素を含むものとします：\n"
                        "1. 第一印象：画像を見た人が'{title}'を直接的に想起できる、かわいくて魅力的なキャラクターデザイン。\n"
                        "2. '{title}'の本質：概念が象徴するものや、その影響が及ぼす環境を表すキャラクターの特徴やアクセサリー。\n"
                        "3. 登場するオブジェクトや象徴：概念を表すメタフォリックなオブジェクトやキャラクターの小道具。\n"
                        "4. 情感や雰囲気：概念が引き起こす感情やムードを強調する表情や背景の雰囲気。\n"
                        "5. 色と光の使用：概念の感情的または象徴的な意味を強化するための鮮やかな色彩や柔らかい照明。\n"
                        "6. 形状や質感を強調：キャラクターの服装やアクセサリーのディテールによる視覚的な強調。\n"
                        "このプロンプトは200文字から1000文字の範囲で、具体的で視覚的に豊かな説明を含むものにしてください。"
                    }
                ],
                max_tokens=1000
            )
            # モデルの完了から望ましい内容と考えられる最後のメッセージを取得する
            messages = response.choices[0].message
            return messages.content
        except Exception as e:
            logger.error(
                f"Error occurred while generate_prompt_from_title: {e}")
            # 画像プロンプトがないと画像が生成できないためエラーにする
            raise


class SurrealismPromptGenerator(AbstractPromptGenerator):
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_prompt_from_title(self, title):
        """問題タイトルに基づいてシュルレアリスム風な画像プロンプトを生成します。"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "指定された抽象的概念を萌えキャラで擬人化したかわいい画像を生成するためのプロンプトを生成してください。プロンプトは、概念の感情的な影響を視覚的に強調して表現するのに適している必要があります。"
                    },
                    {
                        "role": "user",
                        "content": f"抽象的概念 '{title}' を萌えキャラで擬人化し、「萌え」を強調したかわいい画像を生成できるようなプロンプトを生成してください。このプロンプトは次の要素を含むものとします：\n"
                        "1. 第一印象：画像を見た人が'{title}'を直接的に想起できる、かわいくて魅力的なキャラクターデザイン。\n"
                        "2. '{title}'の本質：概念が象徴するものや、その影響が及ぼす環境を表すキャラクターの特徴やアクセサリー。\n"
                        "3. 登場するオブジェクトや象徴：概念を表すメタフォリックなオブジェクトやキャラクターの小道具。\n"
                        "4. 情感や雰囲気：概念が引き起こす感情やムードを強調する表情や背景の雰囲気。\n"
                        "5. 色と光の使用：概念の感情的または象徴的な意味を強化するための鮮やかな色彩や柔らかい照明。\n"
                        "6. 形状や質感を強調：キャラクターの服装やアクセサリーのディテールによる視覚的な強調。\n"
                        "このプロンプトは200文字から1000文字の範囲で、具体的で視覚的に豊かな説明を含むものにしてください。"
                    }
                ],
                max_tokens=1000
            )
            # モデルの完了から望ましい内容と考えられる最後のメッセージを取得する
            messages = response.choices[0].message
            return messages.content
        except Exception as e:
            logger.error(
                f"Error occurred while generate_prompt_from_title: {e}")
            # 画像プロンプトがないと画像が生成できないためエラーにする
            raise


class RealismPromptGenerator(AbstractPromptGenerator):
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_prompt_from_title(self, title):
        """問題タイトルに基づいてシュルレアリスム風な画像プロンプトを生成します。"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "指定された抽象的概念を萌えキャラで擬人化したかわいい画像を生成するためのプロンプトを生成してください。プロンプトは、概念の感情的な影響を視覚的に強調して表現するのに適している必要があります。"
                    },
                    {
                        "role": "user",
                        "content": f"抽象的概念 '{title}' を萌えキャラで擬人化し、「萌え」を強調したかわいい画像を生成できるようなプロンプトを生成してください。このプロンプトは次の要素を含むものとします：\n"
                        "1. 第一印象：画像を見た人が'{title}'を直接的に想起できる、かわいくて魅力的なキャラクターデザイン。\n"
                        "2. '{title}'の本質：概念が象徴するものや、その影響が及ぼす環境を表すキャラクターの特徴やアクセサリー。\n"
                        "3. 登場するオブジェクトや象徴：概念を表すメタフォリックなオブジェクトやキャラクターの小道具。\n"
                        "4. 情感や雰囲気：概念が引き起こす感情やムードを強調する表情や背景の雰囲気。\n"
                        "5. 色と光の使用：概念の感情的または象徴的な意味を強化するための鮮やかな色彩や柔らかい照明。\n"
                        "6. 形状や質感を強調：キャラクターの服装やアクセサリーのディテールによる視覚的な強調。\n"
                        "このプロンプトは200文字から1000文字の範囲で、具体的で視覚的に豊かな説明を含むものにしてください。"
                    }
                ],
                max_tokens=1000
            )
            # モデルの完了から望ましい内容と考えられる最後のメッセージを取得する
            messages = response.choices[0].message
            return messages.content
        except Exception as e:
            logger.error(
                f"Error occurred while generate_prompt_from_title: {e}")
            # 画像プロンプトがないと画像が生成できないためエラーにする
            raise


class ImpressionismPromptGenerator(AbstractPromptGenerator):
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_prompt_from_title(self, title):
        """問題タイトルに基づいてインプレッショニズム風な画像プロンプトを生成します。"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "指定された抽象的概念を萌えキャラで擬人化したかわいい画像を生成するためのプロンプトを生成してください。プロンプトは、概念の感情的な影響を視覚的に強調して表現するのに適している必要があります。"
                    },
                    {
                        "role": "user",
                        "content": f"抽象的概念 '{title}' を萌えキャラで擬人化し、「萌え」を強調したかわいい画像を生成できるようなプロンプトを生成してください。このプロンプトは次の要素を含むものとします：\n"
                        "1. 第一印象：画像を見た人が'{title}'を直接的に想起できる、かわいくて魅力的なキャラクターデザイン。\n"
                        "2. '{title}'の本質：概念が象徴するものや、その影響が及ぼす環境を表すキャラクターの特徴やアクセサリー。\n"
                        "3. 登場するオブジェクトや象徴：概念を表すメタフォリックなオブジェクトやキャラクターの小道具。\n"
                        "4. 情感や雰囲気：概念が引き起こす感情やムードを強調する表情や背景の雰囲気。\n"
                        "5. 色と光の使用：概念の感情的または象徴的な意味を強化するための鮮やかな色彩や柔らかい照明。\n"
                        "6. 形状や質感を強調：キャラクターの服装やアクセサリーのディテールによる視覚的な強調。\n"
                        "このプロンプトは200文字から1000文字の範囲で、具体的で視覚的に豊かな説明を含むものにしてください。"
                    }
                ],
                max_tokens=1000
            )
            # モデルの完了から望ましい内容と考えられる最後のメッセージを取得する
            messages = response.choices[0].message
            return messages.content
        except Exception as e:
            logger.error(
                f"Error occurred while generate_prompt_from_title: {e}")
            # 画像プロンプトがないと画像が生成できないためエラーにする
            raise


class LikeAbstractPaintingPromptGenerator(AbstractPromptGenerator):
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_prompt_from_title(self, title):
        """問題タイトルに基づいて抽象画風な画像プロンプトを生成します。"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "指定された抽象的概念を萌えキャラで擬人化したかわいい画像を生成するためのプロンプトを生成してください。プロンプトは、概念の感情的な影響を視覚的に強調して表現するのに適している必要があります。"
                    },
                    {
                        "role": "user",
                        "content": f"抽象的概念 '{title}' を萌えキャラで擬人化し、「萌え」を強調したかわいい画像を生成できるようなプロンプトを生成してください。このプロンプトは次の要素を含むものとします：\n"
                        "1. 第一印象：画像を見た人が'{title}'を直接的に想起できる、かわいくて魅力的なキャラクターデザイン。\n"
                        "2. '{title}'の本質：概念が象徴するものや、その影響が及ぼす環境を表すキャラクターの特徴やアクセサリー。\n"
                        "3. 登場するオブジェクトや象徴：概念を表すメタフォリックなオブジェクトやキャラクターの小道具。\n"
                        "4. 情感や雰囲気：概念が引き起こす感情やムードを強調する表情や背景の雰囲気。\n"
                        "5. 色と光の使用：概念の感情的または象徴的な意味を強化するための鮮やかな色彩や柔らかい照明。\n"
                        "6. 形状や質感を強調：キャラクターの服装やアクセサリーのディテールによる視覚的な強調。\n"
                        "このプロンプトは200文字から1000文字の範囲で、具体的で視覚的に豊かな説明を含むものにしてください。"
                    }
                ],
                max_tokens=1000
            )
            # モデルの完了から望ましい内容と考えられる最後のメッセージを取得する
            messages = response.choices[0].message
            return messages.content
        except Exception as e:
            logger.error(
                f"Error occurred while generate_prompt_from_title: {e}")
            # 画像プロンプトがないと画像が生成できないためエラーにする
            raise


class GenrePaintingPaintingPromptGenerator(AbstractPromptGenerator):
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_prompt_from_title(self, title):
        """問題タイトルに基づいて博物画風な画像プロンプトを生成します。"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "指定された抽象的概念を萌えキャラで擬人化したかわいい画像を生成するためのプロンプトを生成してください。プロンプトは、概念の感情的な影響を視覚的に強調して表現するのに適している必要があります。"
                    },
                    {
                        "role": "user",
                        "content": f"抽象的概念 '{title}' を萌えキャラで擬人化し、「萌え」を強調したかわいい画像を生成できるようなプロンプトを生成してください。このプロンプトは次の要素を含むものとします：\n"
                        "1. 第一印象：画像を見た人が'{title}'を直接的に想起できる、かわいくて魅力的なキャラクターデザイン。\n"
                        "2. '{title}'の本質：概念が象徴するものや、その影響が及ぼす環境を表すキャラクターの特徴やアクセサリー。\n"
                        "3. 登場するオブジェクトや象徴：概念を表すメタフォリックなオブジェクトやキャラクターの小道具。\n"
                        "4. 情感や雰囲気：概念が引き起こす感情やムードを強調する表情や背景の雰囲気。\n"
                        "5. 色と光の使用：概念の感情的または象徴的な意味を強化するための鮮やかな色彩や柔らかい照明。\n"
                        "6. 形状や質感を強調：キャラクターの服装やアクセサリーのディテールによる視覚的な強調。\n"
                        "このプロンプトは200文字から1000文字の範囲で、具体的で視覚的に豊かな説明を含むものにしてください。"
                    }
                ],
                max_tokens=1000
            )
            # モデルの完了から望ましい内容と考えられる最後のメッセージを取得する
            messages = response.choices[0].message
            return messages.content
        except Exception as e:
            logger.error(
                f"Error occurred while generate_prompt_from_title: {e}")
            # 画像プロンプトがないと画像が生成できないためエラーにする
            raise


class ImageGenerator:
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_image(self, prompt):
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                # model="dall-e-2",
                prompt=prompt,
                size="1024x1024",
                # size="512×512",
                n=1,
                quality="standard"
            )
            image_url = response.data[0].url
            image_path = prompt.split(
                '/')[-1].replace(' ', '_').lower() + ".png"
            return image_path, image_url
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            # 画像の生成に失敗した場合はエラーにする
            raise


class ExplanationGenerator:
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_text(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "次のプロンプトに基づいて詳細な説明を生成してください。"},
                    {"role": "user", "content": f"DALL-E-3で以下のプロントで画像を生成します。生成されるであろう画像の意味を400文字以上、1000文字以内の詳細な説明を,「DALL-E-3」や「生成される」、「生成された」などの単語は含まないで生成してください。: {prompt}"}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error occurred while generating text: {e}")
            return "説明文の生成に失敗しました。"


class HintGenerator:
    def __init__(self, openai_client):
        self.client = openai_client.client

    def split_response_into_list(self, response_text):
        # 分割するためのテキストを行ごとに分ける
        hint_list = response_text.split('\n')
        # 空の行を除外する
        hint_list = [line.strip() for line in hint_list if line.strip()]

        return hint_list

    def generate_hint(self, word):
        try:
            prompt = f'''
            単語当てゲーム用に、「{word}」という単語に対するヒントを4つ生成してください。ヒントはこの単語が持つ一般的な特徴や関連性に焦点を当てるものであり「{word}」という単語自体は必ず含まないものとします。以下の観点からヒントを構成してください：
            1. この単語が一般的にどのような状況や文脈で使われるか。
            2. この単語とよく関連づけられる他の概念や対象。
            3. この単語の具体的な特性や性質。
            4. この単語がどのような感情やイメージを喚起するか。
            '''
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "次のプロンプトに基づいてヒントを生成してください。"},
                    {"role": "user", "content": prompt}
                ]
            )
            return self.split_response_into_list(response.choices[0].message.content.strip())
        except Exception as e:
            logger.error(f"Error occurred while generating hint: {e}")
            return "ヒントの生成に失敗しました。"


class QuizDataFormatter:
    @staticmethod
    def format_data(base_title, description, hints, prompt, image_url):
        return {
            "image": image_url,
            "answer": base_title,
            "explanation": description,
            "hints": hints,
            "imgae_generate_prompt": prompt}


class QuizGeneratorFacade:
    def __init__(self, PromptGenerator: AbstractPromptGenerator = PromptGenerator):
        secret = QuizGeneratorFacade.get_secret()
        self.openai_client = OpenAIClient(secret)
        self.prompt_generator = PromptGenerator(self.openai_client)
        self.image_generator = ImageGenerator(self.openai_client)
        self.text_generator = ExplanationGenerator(self.openai_client)
        self.hint_generator = HintGenerator(self.openai_client)
        self.quiz_formatter = QuizDataFormatter()

    def generate_complete_quiz(self, base_title):
        """
        問題タイトルに基づいてクイズを生成します。

        """
        try:
            prompt = self.prompt_generator.generate_prompt_from_title(
                base_title)
            image_path, image_url = self.image_generator.generate_image(prompt)
            description = self.text_generator.generate_text(prompt)
            hints = self.hint_generator.generate_hint(base_title)
            return self.quiz_formatter.format_data(base_title, description, hints, prompt, image_url)
        except Exception as e:
            logger.error(f"Error occurred while generating quiz: {e}")
            return None, None

    @classmethod
    def get_secret(cls):
        # Secret Managerクライアントの初期化
        client = secretmanager.SecretManagerServiceClient()

        project_id = os.environ.get("PROJECT_ID")
        secret_name = f"projects/{project_id}/secrets/openai/versions/latest"

        # Secret Managerから秘密情報を取得
        response = client.access_secret_version(request={"name": secret_name})
        secret_value = response.payload.data.decode("UTF-8")

        # 単純な文字列データを返す
        return secret_value
