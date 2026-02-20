import ollama


class OllamaClient:

    def __init__(self, model, target_lang, source_lang=None):

        self.model = model
        self.target_lang = target_lang
        self.source_lang = source_lang

    def translate(self, text: str):

        if not isinstance(text, str) or not text.strip():
            return text

        if self.source_lang:

            prompt = (
                f"Translate the following text from {self.source_lang} "
                f"to {self.target_lang}. Only return the translation.\n\n"
                f"{text}"
            )

        else:

            prompt = (
                f"Translate the following text to {self.target_lang}. "
                f"Only return the translation.\n\n"
                f"{text}"
            )

        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"].strip()