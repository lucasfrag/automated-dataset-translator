import ollama

from auto_dataset_translator.translator.cache import TranslationCache
from auto_dataset_translator.translator.retry import (
    retry_with_backoff,
    RetryConfig,
)


class OllamaClient:

    def __init__(
        self,
        model,
        target_lang,
        source_lang=None,
        retry_config=None,
    ):

        self.model = model
        self.target_lang = target_lang
        self.source_lang = source_lang

        self.cache = TranslationCache()

        self.retry_config = retry_config or RetryConfig()

    def _translate_api(self, text):

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

    def translate(self, text):

        if not isinstance(text, str) or not text.strip():
            return text

        # CACHE HIT
        cached = self.cache.get(
            text,
            self.model,
            self.target_lang,
        )

        if cached:
            return cached

        # RETRY LOGIC
        translated = retry_with_backoff(
            lambda: self._translate_api(text),
            self.retry_config,
        )

        # CACHE SAVE
        self.cache.set(
            text,
            translated,
            self.model,
            self.target_lang,
        )

        return translated