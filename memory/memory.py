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
    
    def retrieve_relevant(self, query, top_k=3):
        """
        according to the keyword matching, return the top_k most relevant historical records to the query.
        return model: list of dicts, each dict contains {'user': ..., 'agent': ..., 'timestamp': ...}
        """
        if not self.conversations:
            return []

        # simplified query: split by non-word characters
        import re
        query_words = set(re.findall(r'\w+', query.lower()))

        if not query_words:
            return self.get_recent_history(top_k)

        # calculate a match score for each record (the number of overlapping words with the query)
        scored = []
        for conv in self.conversations:
            user_text = conv.get('user', '')
            agent_text = conv.get('agent', '')
            combined = (user_text + ' ' + agent_text).lower()
            # calculate the number of matching words
            match_count = sum(1 for word in query_words if word in combined)
            if match_count > 0:
                scored.append((match_count, conv))

        # sort by match score in descending order and take top_k
        scored.sort(key=lambda x: x[0], reverse=True)
        top_convs = [conv for _, conv in scored[:top_k]]

        # If not enough records matched, supplement with recent records
        if len(top_convs) < top_k:
            recent = self.get_recent_history(top_k)
            # Remove duplicates
            existing = set(id(conv) for conv in top_convs)
            for conv in recent:
                if id(conv) not in existing:
                    top_convs.append(conv)
                    if len(top_convs) >= top_k:
                        break

        return top_convs