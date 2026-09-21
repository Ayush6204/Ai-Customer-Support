import re


def clean_text(text: str) -> str:
    """
    Clean extracted document text.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n") #Different operating systems may store “new line” differently:Windows: "\r\n" Old Mac: "\r"Linux/macOS: "\n"

    # Remove broken null characters
    text = text.replace("\x00", " ") #Sometimes extracted document text contains broken invisible characters called null characters. This replaces them with spaces.

    # Remove excessive spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)  #Removes repeated spaces and tabs. This changes multiple spaces or tabs into a single space.

    # Remove too many blank lines
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        clean_line = line.strip()

        if clean_line:
            cleaned_lines.append(clean_line)

    cleaned_text = "\n".join(cleaned_lines)

    # Normalize multiple spaces again
    cleaned_text = re.sub(r" +", " ", cleaned_text)

    return cleaned_text.strip()