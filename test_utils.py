from core.utils import *

print(generate_uuid())

print(
    sanitize_filename(
        "My Project?.pdf"
    )
)

print(
    clean_text(
        "Hello      World\n\nPython"
    )
)

print(
    format_timestamp()
)

print(
    validate_pdf(
        "sample.pdf"
    )
)