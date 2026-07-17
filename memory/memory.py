import json
import os
from datetime import datetime

class SimpleMemory:
    """Simple memory module using a JSON file to store conversation history."""
    def __init__(self, user_id="default_user"):
        self.user_id = user_id
        self.memory_file = f"memory_{user_id}.json"
        self.conversations = self._load_memory()

    def _load_memory(self):
        """Load conversations from the JSON file."""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return []

    def save_conversation(self, user_input, agent_response):
        """Save a user-agent exchange to the memory."""
        self.conversations.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": agent_response
        })
        with open(self.memory_file, 'w') as f:
            json.dump(self.conversations, f, indent=2)

    def get_recent_history(self, n=5):
        """Retrieve the last 'n' conversation records."""
        return self.conversations[-n:]