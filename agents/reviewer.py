from llm_client import query_router

def reviewer_agent(user_input, response, context=""):
    # Decides whether an answer should be accepted or revised
    prompt = f"""
    You are a reviewer. Decide if the answer should be accepted.

    User request:
    {user_input}

    Assistant response:
    {response}

    Context:
    {context if context else "No context."}

    Reply with only one word:
    PASS or RETRY
    """
    return query_router(prompt, agent_type="general")