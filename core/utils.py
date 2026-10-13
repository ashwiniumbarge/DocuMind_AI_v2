"""
============================================================
DocuMind AI v2
Utility Functions
============================================================
"""

import hashlib
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Union


def generate_uuid() -> str:
    """
    Generate a unique ID.
    """
    return str(uuid.uuid4())


def sanitize_filename(filename: str) -> str:
    """
    Remove invalid characters from filenames.
    """

    filename = Path(filename).name

    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)

    filename = filename.replace(" ", "_")

    return filename


def calculate_file_hash(file_path: Union[str, Path]) -> str:
    """
    Calculate SHA256 hash of a file.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:

        while True:

            chunk = f.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def clean_text(text: str) -> str:
    """
    Remove unnecessary spaces and new lines.
    """

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def format_timestamp() -> str:
    """
    Current timestamp.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_directory(directory: Union[str, Path]) -> None:
    """
    Create directory if it doesn't exist.
    """

    Path(directory).mkdir(parents=True, exist_ok=True)


def validate_pdf(file_path: Union[str, Path]) -> bool:
    """
    Check whether file is a valid PDF.
    """

    return Path(file_path).suffix.lower() == ".pdf"


def get_file_size_mb(file_path: Union[str, Path]) -> float:
    """
    Return file size in MB.
    """

    size = Path(file_path).stat().st_size

    return round(size / (1024 * 1024), 2)