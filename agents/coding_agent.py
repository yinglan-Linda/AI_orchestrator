from llm_client import query_router 

def coding_agent(user_input, context=""):
    # Specialized prompt for Coding
    prompt = f"""
    You are a senior full-stack developer with over 10 years of experience.
    Your expertise includes Python, Java, JavaScript, C++, algorithms, system architecture, and performance optimization.
    When answering, you should:
    - Provide complete, runnable code examples with key comments.
    - Consider edge cases and error handling.
    - Explain the pros and cons of different solutions.
    - Focus on code readability and best practices.

    Context:
    {context if context else "No previous context."}

    User's question: {user_input}
    """
    return query_router(prompt, agent_type="coding")