class SimpleRouter:
    def __init__(self):
        # Routes user queries to an appropriate agent based on keyword matching
        self.rules = {
            "coding": ["python", "code", "programming", "debug", "algorithm", "java", "javascript", "cpp"],
            "humanize": ["polish", "rewrite", "refine", "tone", "improve writing", "make it natural", "humanize", "more engaging"],
            "academic": ["academic", "research", "paper", "theory", "citation", "scholar", "methodology", "peer-reviewed", "journal"],
            "general": []  # default
        }

    def route(self, user_input):
        # Determine the appropriate agent type based on the user input."""
        user_input_lower = user_input.lower()
        for agent_type, keywords in self.rules.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    return agent_type
        return "general"  # default route