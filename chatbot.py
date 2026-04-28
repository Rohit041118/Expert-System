"""
chatbot.py
==========
Chatbot Conversation State Machine for the Fashion Expert System.
Manages the multi-step Q&A flow and accumulates user facts.
"""

# ─────────────────────────────────────────────────────────────────────────────
# CONVERSATION STEPS
# ─────────────────────────────────────────────────────────────────────────────

STEPS = [
    {
        "key": "gender",
        "question": "👋 Welcome to the <strong>Fashion AI Stylist</strong>! I'm here to recommend the perfect outfit for you.<br><br>Let's start — <strong>what is your gender?</strong>",
        "options": ["Male", "Female"],
        "hint": "Pick one to continue",
    },
    {
        "key": "occasion",
        "question": "Great choice! 👗 Now, <strong>what is the occasion</strong> you're dressing for?",
        "options": ["Party", "Office", "Casual", "Wedding"],
        "hint": "Select your occasion",
    },
    {
        "key": "weather",
        "question": "Perfect! 🌤️ What's the <strong>weather like</strong> where you'll be?",
        "options": ["Hot", "Cold", "Rainy"],
        "hint": "Select current weather",
    },
    {
        "key": "style",
        "question": "Nice! ✨ What <strong>style do you prefer</strong>?",
        "options": ["Formal", "Trendy", "Casual", "Sporty", "Classic"],
        "hint": "Pick your vibe",
    },
    {
        "key": "color",
        "question": "Almost done! 🎨 What <strong>color tone do you prefer</strong> in your outfits?",
        "options": ["Dark", "Light", "Bright", "Neutral"],
        "hint": "Choose your color preference",
    },
]

VALID_ANSWERS = {
    "gender":  ["male", "female"],
    "occasion": ["party", "office", "casual", "wedding"],
    "weather":  ["hot", "cold", "rainy"],
    "style":    ["formal", "trendy", "casual", "sporty", "classic"],
    "color":    ["dark", "light", "bright", "neutral"],
}

STEP_KEYS = [s["key"] for s in STEPS]


# ─────────────────────────────────────────────────────────────────────────────
# CHATBOT SESSION
# ─────────────────────────────────────────────────────────────────────────────

class ChatbotSession:
    """
    Manages a single user's conversation state.
    Stored in Flask's server-side session dict.
    """

    @staticmethod
    def initial_state():
        return {
            "step": 0,           # Current step index in STEPS
            "facts": {},         # Accumulated user answers
            "done": False,       # Whether conversation is complete
        }

    @staticmethod
    def get_current_question(state):
        """Return the question dict for the current step."""
        idx = state["step"]
        if idx < len(STEPS):
            return STEPS[idx]
        return None

    @staticmethod
    def process_answer(state, user_input: str):
        """
        Validate and record the user's answer for the current step.
        Returns (updated_state, error_message_or_None).
        """
        idx = state["step"]
        if idx >= len(STEPS):
            return state, "Conversation already complete."

        step = STEPS[idx]
        key = step["key"]
        answer = user_input.strip().lower()

        # Validate against allowed options
        if answer not in VALID_ANSWERS[key]:
            options_str = " / ".join(VALID_ANSWERS[key])
            return state, (
                f"❌ I didn't catch that. Please choose one of: "
                f"<strong>{options_str}</strong>"
            )

        # Record fact
        state["facts"][key] = answer
        state["step"] += 1

        if state["step"] >= len(STEPS):
            state["done"] = True

        return state, None

    @staticmethod
    def get_next_question(state):
        """
        Return the next question dict, or None if conversation is done.
        """
        idx = state["step"]
        if idx < len(STEPS):
            return STEPS[idx]
        return None

    @staticmethod
    def get_progress(state):
        """Returns progress as (current_step, total_steps)."""
        return state["step"], len(STEPS)
