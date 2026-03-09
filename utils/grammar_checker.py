import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def grammar_check(text):

    matches = tool.check(text)

    errors = []

    for match in matches[:10]:  # limit to first 10 errors
        errors.append({
            "error": text[match.offset: match.offset + match.errorLength],
            "message": match.message,
            "suggestions": match.replacements[:3]
        })

    return errors