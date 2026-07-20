from memory.memory import SimpleMemory
from router.router import SimpleRouter
# from agents import academic_agent, humanize_agent, coding_agent, general_agent
from llm_client import query_router

def main():
    # Entry point for the AI Orchestrator.
    memory = SimpleMemory()
    router = SimpleRouter()

    print("AI Orchestrator Started (type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break

        # router
        agent_type = router.route(user_input)

        # To use diff agent
        # if agent_type == "coding":
        #     response = coding_agent.coding_agent(user_input)
        # elif agent_type == "academic":
        #     response = academic_agent.academic_agent(user_input)
        # elif agent_type == "humanize":
        #     response = humanize_agent.humanize_agent(user_input)
        # else:
        #     response = general_agent.general_agent(user_input)
        if agent_type == "coding":
            response = query_router(user_input, "coding")
        elif agent_type == "academic":
            response = query_router(user_input, "academic")
        elif agent_type == "humanize":
            response = query_router(user_input, "humanize")
        else:
            response = query_router(user_input, "general")
        
        # refresh memory
        memory.save_conversation(user_input, response)

        print(f"AI: {response}")

if __name__ == "__main__":
    main()