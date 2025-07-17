## How Persona Detection Works

This project personalizes the assistant's behavior by detecting the user's persona: **`tourist`**, **`resident`**, or **`neutral`** (newcomer/unspecified). The detection process is fully automatic and updates dynamically during the conversation.

---

### Step-by-Step Explanation

1. **User Input**
   - The user is prompted to describe their needs or background.
   - Example prompt:  
     `"Tell me a bit about yourself or your needs (so I can personalize):"`

2. **LLM-Based Persona Classification**
   - The function `detect_persona(user_text)` sends the input to the `claude-3-haiku` model via the OpenRouter API.
   - A system prompt instructs the model to respond with just one word:  
     **`tourist`**, **`resident`**, or **`neutral`**.
   - The API returns this label, which is parsed and validated.

3. **Prompt Personalization**
   - The label is passed to `get_prompt_for(persona)` which returns a predefined prompt tailored for that persona.
   - This prompt is then used to configure the AGNO `Agent`, altering its tone, knowledge scope, and recommendation style.

4. **Dynamic Persona Switching**
   - Every new user query is re-evaluated.
   - If the persona classification changes mid-conversation (e.g., a tourist starts asking about Bangalore rent), the agent updates its prompt and adapts accordingly.

5. **Fallbacks and Robustness**
   - If the classification fails or gives unexpected output, the system defaults to the `neutral` persona to maintain graceful degradation.

---

### Benefits

- Enhances user experience through targeted answers.
- Reduces irrelevant information.
- Adapts in real-time to user behavior.
- Enables use-case-specific knowledge retrieval and tool usage.


