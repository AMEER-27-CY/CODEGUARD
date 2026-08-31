"""
Optional LLM explanation layer.
 
Only runs if ANTHROPIC_API_KEY is set in the environment. The tool
works fully without it — this layer only adds a friendlier, more
tailored explanation on top of the rule engine's built-in why/fix
text. Never sends the whole file, only the single matched line, to
minimize what leaves the machine.
"""
 
import os
 
 
def explain(finding) -> str:
    """Return a plain-language explanation for a finding.
 
    Falls back to the rule's built-in explanation if no API key is
    configured or the API call fails for any reason.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return finding.why
 
    try:
        import anthropic
 
        client = anthropic.Anthropic(api_key=api_key)
        prompt = (
            f"A code scanner flagged this line for '{finding.title}':\n"
            f"{finding.line_text}\n\n"
            f"In 2 short sentences, explain in plain language (for a "
            f"non-technical builder) why this is risky and how to fix it."
        )
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception:
        # Fail safe: never break the scan because the optional AI
        # layer had a problem (no key, no network, quota, etc).
        return finding.why
 