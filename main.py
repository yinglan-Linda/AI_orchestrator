from pathlib import Path
from dotenv import load_dotenv
# load environment variables from .env file first
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

from memory.memory import SimpleMemory
from router.router import SimpleRouter
from llm_client import query_router
from agents.coding_agent import coding_agent
from agents.academic_agent import academic_agent
from agents.humanize_agent import humanize_agent
from agents.general_agent import general_agent
from agents.reviewer import reviewer_agent

def main():
    # Entry point for the AI Orchestrator.
    memory = SimpleMemory()
    router = SimpleRouter()

    print("AI Orchestrator Started (type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break

        # router the user input to the appropriate agent
        agent_type = router.route(user_input)

        # Retrieve recent conversation relevant history for context
        relevant_history = memory.retrieve_relevant(user_input, top_k=3)
        context = ""
        if relevant_history:
            context = "\n".join([f"User: {h['user']}\nAI: {h['agent']}" for h in relevant_history])
            prompt_with_context = f"Relevant past conversation:\n{context}\n\nCurrent user: {user_input}"
        else:
            prompt_with_context = user_input

        # Call the model once and get the full response info
        result = query_router(prompt_with_context, agent_type)
        
        # Extract content, model name, and source
        response = result.get("content", "no response")

        # Run the reviewer only when the request is complex enough to justify an extra check.
        if should_review(user_input, agent_type, response):
            review_result = reviewer_agent(user_input, response, context=prompt_with_context)
            review_text = review_result.get("content", "").strip().upper()

            # If the reviewer requests a retry, regenerate the response once using the same agent.
            if review_text == "RETRY":
                if agent_type == "coding":
                    result = coding_agent(user_input, context=prompt_with_context)
                elif agent_type == "academic":
                    result = academic_agent(user_input, context=prompt_with_context)
                elif agent_type == "humanize":
                    result = humanize_agent(user_input, context=prompt_with_context)
                else:
                    result = general_agent(user_input, context=prompt_with_context)

                response = result.get("content", response)

        model_used = result.get("model", "unknown")
        source = result.get("source", "unknown")

        # Save the conversation to memory
        memory.save_conversation(user_input, response)

        # Print the result with model and source
        print(f"AI ({source}: {model_used}): {response}")

def should_review(user_input, agent_type, response):
    """
    Determine if the AI's response should be reviewed.
    """
    if agent_type in ["coding", "academic"]:
        return True

    if len(user_input.split()) > 12:
        return True

    if len(response.split()) > 100:
        return True

    return False

if __name__ == "__main__":
    main()