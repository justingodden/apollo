import re


def rm_spaces(feature: str) -> str:
    return re.sub(r'[^0-9a-zA-Z]', '', feature)
