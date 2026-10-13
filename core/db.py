"""
============================================================
DocuMind AI v2
Database Module
============================================================
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import List, Optional

from core.config import DATABASE_PATH
from core.logger import logger


class Database:
    """
    SQLite Database Manager
    """

    def __init__(self):

        self.db_path = DATABASE_PATH

        self.initialize()

    @contextmanager
    def connect(self):

        conn = sqlite3.connect(self.db_path)

        conn.row_factory = sqlite3.Row

        try:

            yield conn

            conn.commit()

        except Exception:

            conn.rollback()

            raise

        finally:

            conn.close()

    def initialize(self):

        with self.connect() as conn:

            cursor = conn.cursor()

            # ----------------------------
            # Users
            # ----------------------------

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE NOT NULL,

                email TEXT UNIQUE NOT NULL,

                password TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """)

            # ----------------------------
            # Documents
            # ----------------------------

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                filename TEXT,

                file_hash TEXT,

                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(user_id)
                REFERENCES users(id)

            )
            """)

            # ----------------------------
            # Chat History
            # ----------------------------

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                document_name TEXT,

                role TEXT,

                message TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """)

            logger.info("Database initialized successfully")

    # ==========================================================
    # USER METHODS
    # ==========================================================

    def create_user(
        self,
        username: str,
        email: str,
        password: str
    ) -> bool:

        try:

            with self.connect() as conn:

                conn.execute(
                    """
                    INSERT INTO users(
                        username,
                        email,
                        password
                    )
                    VALUES(?,?,?)
                    """,
                    (
                        username,
                        email,
                        password
                    )
                )

            return True

        except sqlite3.IntegrityError:

            return False

    def get_user(
        self,
        email: str
    ) -> Optional[sqlite3.Row]:

        with self.connect() as conn:

            return conn.execute(

                """
                SELECT *
                FROM users
                WHERE email=?
                """,

                (email,)

            ).fetchone()

    # ==========================================================
    # DOCUMENT METHODS
    # ==========================================================

    def save_document(

        self,

        user_id,

        filename,

        file_hash

    ):

        with self.connect() as conn:

            conn.execute(

                """
                INSERT INTO documents(

                    user_id,

                    filename,

                    file_hash

                )

                VALUES(?,?,?)

                """,

                (

                    user_id,

                    filename,

                    file_hash

                )

            )

    def get_documents(

        self,

        user_id

    ) -> List[sqlite3.Row]:

        with self.connect() as conn:

            return conn.execute(

                """
                SELECT *

                FROM documents

                WHERE user_id=?

                ORDER BY uploaded_at DESC
                """,

                (user_id,)

            ).fetchall()

    def delete_document(

        self,

        user_id,

        filename

    ):

        with self.connect() as conn:

            conn.execute(

                """
                DELETE

                FROM documents

                WHERE user_id=?

                AND filename=?

                """,

                (

                    user_id,

                    filename

                )

            )

    # ==========================================================
    # CHAT METHODS
    # ==========================================================

    def save_chat(

        self,

        user_id,

        document_name,

        role,

        message

    ):

        with self.connect() as conn:

            conn.execute(

                """
                INSERT INTO chat_history(

                    user_id,

                    document_name,

                    role,

                    message

                )

                VALUES(?,?,?,?)

                """,

                (

                    user_id,

                    document_name,

                    role,

                    message

                )

            )

    def get_chat(

        self,

        user_id,

        document_name

    ) -> List[sqlite3.Row]:

        with self.connect() as conn:

            return conn.execute(

                """
                SELECT *

                FROM chat_history

                WHERE user_id=?

                AND document_name=?

                ORDER BY id
                """,

                (

                    user_id,

                    document_name

                )

            ).fetchall()

    def clear_chat(

        self,

        user_id,

        document_name

    ):

        with self.connect() as conn:

            conn.execute(

                """
                DELETE

                FROM chat_history

                WHERE user_id=?

                AND document_name=?

                """,

                (

                    user_id,

                    document_name

                )

            )

    def user_exists(self, email: str) -> bool:

        with self.connect() as conn:

            result = conn.execute(
            """
            SELECT 1
            FROM users
            WHERE email=?
            """,
            (email,)
        ).fetchone()

        return result is not None
db = Database()