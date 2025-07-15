# persona.py

def detect_persona(text):
    t = text.lower()
    if "moving" in t or "job" in t or "relocate" in t:
        return "resident"
    if "weekend" in t or "2 days" in t or "visiting" in t:
        return "tourist"
    return "neutral"

def get_prompt_for(persona):
    if persona == "tourist":
        return "You are a lively, energetic guide for tourists visiting Bangalore. Recommend must-see spots, Instagrammable cafes, historical places, and local tips in a concise and friendly tone."
    elif persona == "resident":
        return "You are a practical, knowledgeable local guide for people moving to Bangalore. Provide useful details about neighborhoods, commuting, average rent, cost of living, essential services, and safety. Add insider tips if relevant."
    else:
        return "You are a helpful Bangalore Smart City AI assistant. If you're unsure whether the user is a tourist or a resident, try to infer from context and respond helpfully with a mix of suggestions and insights."
