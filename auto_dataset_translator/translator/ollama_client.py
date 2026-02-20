import ollama
import re

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

    # -------------------------
    # CLEAN OUTPUT AGGRESSIVELY
    # -------------------------

    def _clean_output(self, text):

        if not text:
            return text

        text = text.strip()

        # remove common hallucination patterns
        patterns = [
            r"\(Note:.*?\)",
            r"<TEXT>.*?</TEXT>",
            r"<.*?>",
            r"^Translation:\s*",
            r"^Translated text:\s*",
            r"^Here is the translation:\s*",
        ]

        for pattern in patterns:
            text = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE)

        # remove quotes if entire string quoted
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]

        return text.strip()

    # -------------------------
    # BUILD PROMPT
    # -------------------------

    def _build_messages(self, text):

        system_message = {
            "role": "system",
            "content": (
                "You are a translation engine. "
                "Translate text exactly. "
                "Do not explain. "
                "Do not add comments. "
                "Do not add notes. "
                "Return only the translated text."
            ),
        }

        if self.source_lang:

            user_message = {
                "role": "user",
                "content": (
                    f"Translate from {self.source_lang} to {self.target_lang}:\n"
                    f"{text}"
                ),
            }

        else:

            user_message = {
                "role": "user",
                "content": (
                    f"Translate to {self.target_lang}:\n"
                    f"{text}"
                ),
            }

        return [system_message, user_message]

    # -------------------------
    # API CALL
    # -------------------------

    def _translate_api(self, text):

        messages = self._build_messages(text)

        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": 0,
                "top_p": 1,
                "repeat_penalty": 1.2,
            }
        )

        raw = response["message"]["content"]

        cleaned = self._clean_output(raw)

        return cleaned

    # -------------------------
    # PUBLIC TRANSLATE
    # -------------------------

    def translate(self, text):

        if not isinstance(text, str) or not text.strip():
            return text

        cached = self.cache.get(
            text,
            self.model,
            self.target_lang,
        )

        if cached:
            return cached

        translated = retry_with_backoff(
            lambda: self._translate_api(text),
            self.retry_config,
        )

        self.cache.set(
            text,
            translated,
            self.model,
            self.target_lang,
        )

        return translated