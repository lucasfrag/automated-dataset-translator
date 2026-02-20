import sqlite3
import hashlib
import threading


class TranslationCache:

    def __init__(self, db_path="translation_cache.db"):

        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )

        self.lock = threading.Lock()

        self._create_table()

    def _create_table(self):

        with self.lock:

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS translations (
                    hash TEXT PRIMARY KEY,
                    source_text TEXT,
                    translated_text TEXT,
                    model TEXT,
                    target_lang TEXT
                )
            """)

            self.conn.commit()

    def _hash(self, text, model, target_lang):

        key = f"{model}:{target_lang}:{text}"

        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def get(self, text, model, target_lang):

        h = self._hash(text, model, target_lang)

        with self.lock:

            cursor = self.conn.execute(
                "SELECT translated_text FROM translations WHERE hash=?",
                (h,)
            )

            row = cursor.fetchone()

        return row[0] if row else None

    def set(self, text, translated, model, target_lang):

        h = self._hash(text, model, target_lang)

        with self.lock:

            self.conn.execute(
                """
                INSERT OR REPLACE INTO translations
                (hash, source_text, translated_text, model, target_lang)
                VALUES (?, ?, ?, ?, ?)
                """,
                (h, text, translated, model, target_lang)
            )

            self.conn.commit()