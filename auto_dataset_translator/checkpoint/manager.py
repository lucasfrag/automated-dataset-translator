import sqlite3
import threading


class CheckpointManager:

    def __init__(self, db_path="checkpoint.db"):

        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )

        self.lock = threading.Lock()

        self._create_table()

    def _create_table(self):

        with self.lock:

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    dataset TEXT,
                    column TEXT,
                    row_index INTEGER,
                    PRIMARY KEY (dataset, column, row_index)
                )
            """)

            self.conn.commit()

    def is_done(self, dataset, column, row_index):

        with self.lock:

            cursor = self.conn.execute(
                """
                SELECT 1 FROM checkpoints
                WHERE dataset=? AND column=? AND row_index=?
                """,
                (dataset, column, row_index)
            )

            return cursor.fetchone() is not None

    def mark_done(self, dataset, column, row_index):

        with self.lock:

            self.conn.execute(
                """
                INSERT OR REPLACE INTO checkpoints
                (dataset, column, row_index)
                VALUES (?, ?, ?)
                """,
                (dataset, column, row_index)
            )

            self.conn.commit()