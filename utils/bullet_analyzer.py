import re
import language_tool_python

tool = language_tool_python.LanguageTool("en-US")


def extract_bullets(text):
    """
    Extract bullet points from resume text.
    Handles:
    - -
    - •
    - *
    - ▪
    - 1. 2. 3.
    - a) b)
    - Lines starting with uppercase action verbs
    """

    bullets = []

    lines = text.split("\n")

    bullet_pattern = re.compile(
        r"""^\s*(
            [-•*▪]\s+ |          # dash, dot, star bullets
            \d+\.\s+ |           # numbered bullets
            [a-zA-Z]\)\s+        # a) b) format
        )""",
        re.VERBOSE
    )

    for line in lines:
        clean_line = line.strip()

        if len(clean_line) < 5:
            continue

        if bullet_pattern.match(clean_line):
            bullets.append(clean_line)
        else:
            # Smart fallback: detect achievement-style sentence
            if re.search(r"\b(improved|developed|built|implemented|designed|created|optimized|achieved|increased|reduced)\b", clean_line.lower()):
                bullets.append(clean_line)

    return bullets

def weak_bullets(bullets):
    weak_verbs = ["worked", "helped", "did", "made", "responsible"]

    weak_list = []

    for bullet in bullets:
        score = 0

        # weak verbs
        if any(verb in bullet.lower() for verb in weak_verbs):
            score += 1

        # no numbers
        if not re.search(r"\d", bullet):
            score += 1

        # short bullet
        if len(bullet.split()) < 8:
            score += 1

        if score >= 1:
            weak_list.append(bullet)

    return weak_list


def fallback_bullets(bullets):
    # If weak bullets less than 2,
    # pick longest bullets for optimization suggestions
    sorted_bullets = sorted(bullets, key=lambda x: len(x), reverse=True)
    return sorted_bullets[:2]