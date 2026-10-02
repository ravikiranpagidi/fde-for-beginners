"""One transparent tokenization baseline for retrieval and extractive generation."""

import re

STOP_WORDS = frozenset(
    "a an the is are was were of to for in on and or with can i my do does how "
    "what when which our we it this that be by from as me tell about".split()
)


def tokens(text: str) -> list[str]:
    return [word for word in re.findall(r"[a-z0-9]+", text.lower()) if word not in STOP_WORDS]
