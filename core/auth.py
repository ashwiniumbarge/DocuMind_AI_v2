"""
============================================================
DocuMind AI v2
Authentication Module
============================================================
"""

import re
import bcrypt

from core.db import db
from core.logger import logger


class AuthManager:
    """
    Authentication Manager
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        """

        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify password against hash.
        """

        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        """

        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password: str):
        """
        Password policy:
        - Minimum 8 characters
        - One uppercase
        - One lowercase
        - One digit
        """

        if len(password) < 8:
            return False, "Password must contain at least 8 characters."

        if not re.search(r"[A-Z]", password):
            return False, "Password must contain an uppercase letter."

        if not re.search(r"[a-z]", password):
            return False, "Password must contain a lowercase letter."

        if not re.search(r"\d", password):
            return False, "Password must contain a digit."

        return True, "Valid password."

    def register(self, username, email, password):
        """
        Register a new user.
        """

        if not self.validate_email(email):
            return False, "Invalid email format."

        valid, message = self.validate_password(password)

        if not valid:
            return False, message

        hashed_password = self.hash_password(password)

        success = db.create_user(
            username,
            email,
            hashed_password
        )

        if not success:
            return False, "User already exists."

        logger.info(f"New user registered: {email}")

        return True, "Registration successful."

    def login(self, email, password):
        """
        Login existing user.
        """

        user = db.get_user(email)

        if user is None:
            return False, "User not found."

        if not self.verify_password(
            password,
            user["password"]
        ):
            return False, "Incorrect password."

        logger.info(f"User logged in: {email}")

        return True, dict(user)


auth = AuthManager()