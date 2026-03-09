import subprocess
import json


def improve_bullets(bullets):
    prompt = f"""
Improve ONLY these weak resume bullets.
Keep meaning same.
Add impact and quantification.
Return as numbered list.

Bullets:
{bullets}
"""

    process = subprocess.Popen(
        ["ollama", "run", "mistral"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output, _ = process.communicate(prompt)
    return output