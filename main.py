from memory.memory import SimpleMemory
from router.router import SimpleRouter
# from agents import academic_agent, humanize_agent, coding_agent, general_agent
from llm_client import query_router

from dotenv import load_dotenv
load_dotenv()  # load environment variables from .env file

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

        # Retrieve recent conversation history for context 
        history = memory.get_recent_history(3)
        context = ""
        if history:
            context = "\n".join([f"User: {h['user']}\nAI: {h['agent']}" for h in history])
            prompt_with_context = f"Previous conversation:\n{context}\n\nCurrent user: {user_input}"
        else:
            prompt_with_context = user_input

        # Call the model once and get the full response info
        result = query_router(prompt_with_context, agent_type)
        
        # Extract content, model name, and source
        response = result.get("content", "无响应")
        model_used = result.get("model", "unknown")
        source = result.get("source", "unknown")

        # Save the conversation to memory
        memory.save_conversation(user_input, response)

        # Print the result with model and source
        print(f"AI ({source}: {model_used}): {response}")

if __name__ == "__main__":
    main()