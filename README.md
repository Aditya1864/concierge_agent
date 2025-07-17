# How Persona Detection Works in this Project?
This project personalizes the assistant's behavior by detecting the user's persona: **`tourist`**, **`resident`**, or **`neutral`** (newcomer/unspecified). The detection process is fully automatic and updates dynamically during the conversation.

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

### Benefits
- Enhances user experience through targeted answers.
- Reduces irrelevant information.
- Adapts in real-time to user behavior.
- Enables use-case-specific knowledge retrieval and tool usage.

---

# RAG vs. Web Search: Decision Logic

This section explains how the Bangalore Smart Agent decides whether to use its internal **PDF knowledge base (RAG)** or perform a **live web search** using external tools like DuckDuckGo.

### Overview
The assistant uses two main sources of information:

- **RAG (Retrieval-Augmented Generation)**: Uses a vector database built from "The Ultimate Bangalore Guide.pdf".
- **Web Search Tool**: Uses DuckDuckGoTools for fresh, real-time information not covered in the PDF.

The agent dynamically chooses between them based on the nature of the user’s query.

### Decision Criteria

1. **Use RAG (PDF knowledge base)** if:
   - The query relates to static or factual information included in the PDF.
   - Example topics:
     - Landmark descriptions
     - Local food joints
     - Transportation basics
     - Neighborhood overviews
     - Cost of living details
     - Kannada phrases
     - Known infrastructure (e.g., Namma Metro lines)

2. **Use Web Search** if:
   - The query requires current, live, or dynamic data not stored in the PDF.
   - Example topics:
     - Entry timings, ticket prices, or status of landmarks
     - Real-time metro route updates or traffic conditions
     - Weather reports
     - Ongoing events, gigs, or festivals
     - Food delivery or app-based offers
     - Recent infrastructure changes or rent hikes

### Implementation Summary
- The AGNO `Agent` is first given a PDF-based `KnowledgeBase` backed by a LanceDB vector store.
- A DuckDuckGo web tool is also attached to the agent.
- During inference, the agent decides:
  - If the query matches vector-retrieved content with high relevance → use RAG.
  - If not enough relevant content is found or if freshness is crucial → use web search.

### Outcome
This design ensures:
- High-quality, grounded responses using local data.
- Real-time responsiveness for time-sensitive queries.
- Minimal hallucination due to fallback logic.
- Flexibility to serve both static and dynamic user intents effectively.

---

# Creative Features Added

### Intelligent Persona Detection via LLM
Instead of using traditional keyword-based classification, this project introduces a more robust and accurate persona detection mechanism by leveraging a language model.

### What’s New
- LLM-Based Classification  
  The agent sends the user's input to a lightweight LLM (`claude-3-haiku`) via OpenRouter to determine the user's persona — `tourist`, `resident`, or `neutral`.

- Why It’s Better Than Keyword Matching  
  Unlike basic keyword detection, which is often brittle and unreliable, the LLM understands natural language context. This enables:
  - Accurate handling of complex or ambiguous descriptions.
  - Adaptability to conversational phrasing, slang, and indirect queries.
  - Seamless persona switching mid-conversation if the user's context changes.

- Dynamic Prompt Injection  
  Once the persona is identified, a tailored system prompt is injected into the agent. This alters the assistant’s tone, content scope, and behavior to match the persona in real time.

### Result
This feature improves the assistant’s contextual understanding, personalization, and response accuracy. It allows for richer and more useful conversations compared to keyword-based approaches.

---

# Handling Conflicting Information
In this agent, conflicting or ambiguous information can arise when answers may differ between the static knowledge base (RAG) and real-time web data. To address this, the agent uses a layered and fallback-based strategy.

### Strategy Overview
1. **Source Priority Based on Query Type**
   - If the query involves timeless, factual, or structured content (e.g., neighborhood overviews, transport options, landmark descriptions), the agent prioritizes the **PDF knowledge base**.
   - If the query requires real-time or volatile data (e.g., current metro timings, event schedules, traffic status), the agent defers to **web search results**.

2. **Explicit Conflict Awareness**
   - If conflicting results are detected (for example, the guide says Cubbon Park closes at 6 PM, but the web shows 7 PM), the agent will prefer the **more recent source**, i.e., the web, and may include a clarification like:
     > "The guide lists the closing time as 6 PM, but recent online data suggests it's open till 7 PM."

3. **Transparent Justification**
   - The agent is encouraged (via system prompt) to state the source of information when a conflict is possible, so users understand which data is being relied upon.

4. **Fallback Mechanism**
   - If the knowledge base lacks information and the web search also fails or gives contradictory results, the agent:
     - Defaults to stating uncertainty,
     - May summarize both possibilities, and
     - Encourages the user to verify from official or updated sources.

### Example Scenario
**User query:** "What time does Lalbagh Botanical Garden close today?"

- **PDF response:** "Closes at 6:00 PM"
- **Web search result:** "Special summer hours until 7:30 PM"

**Agent response:**  
"Lalbagh typically closes at 6:00 PM according to the city guide, but current web results suggest it's open until 7:30 PM today. Please verify on the official website if you're visiting."

### Result
This approach balances trustworthiness and accuracy by combining the stability of offline data with the flexibility of real-time search, while always aiming for transparency when conflicts arise.









