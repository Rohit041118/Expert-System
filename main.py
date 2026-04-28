"""
main.py
=======
Flask Application Entry Point -- Fashion Recommendation Expert System
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from flask import Flask, render_template, request, jsonify, session
from chatbot import ChatbotSession
from expert_system import get_recommendation
import uuid

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
app.secret_key = "fashion-expert-secret-2024-xK9mP"   # For session management


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_or_init_session():
    """Retrieve or initialize the chatbot state in Flask session."""
    if "chatbot" not in session:
        session["chatbot"] = ChatbotSession.initial_state()
    return session["chatbot"]


# ─────────────────────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main chat UI page."""
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    """
    Initialize or reset the session and return the first question.
    Called when the page loads or user clicks 'Start Over'.
    """
    session["chatbot"] = ChatbotSession.initial_state()
    state = session["chatbot"]

    q = ChatbotSession.get_current_question(state)
    current_step, total_steps = ChatbotSession.get_progress(state)

    return jsonify({
        "type": "question",
        "message": q["question"],
        "options": q["options"],
        "hint": q["hint"],
        "step": current_step,
        "total": total_steps,
    })


@app.route("/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint.
    Receives user's answer, processes it through the chatbot & expert system.
    Returns either the next question or the final recommendation.
    """
    data = request.get_json()
    user_message = data.get("message", "").strip()

    state = get_or_init_session()

    # If already done, ignore further messages
    if state.get("done"):
        return jsonify({"type": "done", "message": "Conversation complete. Click 'Start Over' to restart."})

    # Process the answer
    updated_state, error = ChatbotSession.process_answer(state, user_message)
    session["chatbot"] = updated_state
    session.modified = True

    if error:
        # Validation failed — re-ask with error
        q = ChatbotSession.get_current_question(updated_state)
        current_step, total_steps = ChatbotSession.get_progress(updated_state)
        return jsonify({
            "type": "error",
            "message": error,
            "options": q["options"] if q else [],
            "step": current_step,
            "total": total_steps,
        })

    # Conversation complete → run inference engine
    if updated_state["done"]:
        facts = updated_state["facts"]
        result = get_recommendation(facts)

        return jsonify({
            "type": "recommendation",
            "outfit": result["outfit"],
            "accessories": result["accessories"],
            "explanation": result["explanation"],
            "fired_rules": result["fired_rules"],
            "rule_id": result["rule_id"],
            "facts": facts,
        })

    # Next question
    next_q = ChatbotSession.get_next_question(updated_state)
    current_step, total_steps = ChatbotSession.get_progress(updated_state)

    return jsonify({
        "type": "question",
        "message": next_q["question"],
        "options": next_q["options"],
        "hint": next_q["hint"],
        "step": current_step,
        "total": total_steps,
    })


@app.route("/reset", methods=["POST"])
def reset():
    """Reset the session."""
    session.pop("chatbot", None)
    return jsonify({"status": "reset"})


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  [AI] Fashion Recommendation Expert System")
    print("  Running at: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=5000)
