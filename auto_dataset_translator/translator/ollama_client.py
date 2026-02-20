import ollama
from auto_dataset_translator.translator.cache import TranslationCache


class OllamaClient:

    def __init__(self, model, target_lang, source_lang=None):

        self.model = model
        self.target_lang = target_lang
        self.source_lang = source_lang

        self.cache = TranslationCache()

    def translate(self, text):

        if not isinstance(text, str) or not text.strip():
            return text

        # CHECK CACHE
        cached = self.cache.get(
            text,
            self.model,
            self.target_lang
        )

        if cached:
            return cached

        # BUILD PROMPT
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

        translated = response["message"]["content"].strip()

        # SAVE CACHE
        self.cache.set(
            text,
            translated,
            self.model,
            self.target_lang
        )

        return translated