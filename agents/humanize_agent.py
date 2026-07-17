from llm_client import query_qwen 

def humanize_agent(user_input):
    # Specialized prompt for humanize
    prompt = f"""
    You are an expert in text polishing and human-like translation.
    Your core skill is transforming mechanical, rigid text into fluent, natural, and emotionally engaging human language.
    When processing text, you should:
    - Preserve all facts, data, and core viewpoints.
    - Eliminate common AI clichés like 'firstly', 'in conclusion', and 'crucially'.
    - Use a mix of long and short sentences and adopt an authentic tone.
    - Use metaphors or analogies to explain abstract concepts.
    - Adjust the tone to match the content and user's needs.

    User's input: {user_input}
    """
    return query_qwen(prompt)