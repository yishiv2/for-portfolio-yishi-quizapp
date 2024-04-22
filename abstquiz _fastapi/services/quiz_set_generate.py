class ConceptGenerator:
    def __init__(self, openai_client):
        self.client = openai_client.client

    def generate_concepts(self, base_title):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "指定されたタイトルに関連する抽象的な概念を単語リストとして10個生成してください。各概念は単語であるべきです。"},
                {"role": "user", "content": f"{
                    base_title}に関連する10個の抽象的な概念を単語のみで列挙してください。"}
            ]
        )
        concepts_text = response.choices[0].message.content.strip()
        concepts_list = [concept.strip().replace('.', '').replace(',', '')
                         for concept in concepts_text.split()]
        filtered_concepts = [
            concept for concept in concepts_list if not concept.isdigit() and concept != '']
        return filtered_concepts
