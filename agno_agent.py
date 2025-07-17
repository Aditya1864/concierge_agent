# agno_agent.py
print("✅ Script started...")


import os
from dotenv import load_dotenv
# Load your OpenRouter key and base URL from .env
load_dotenv()

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.lancedb import LanceDb
from agno.tools.duckduckgo import DuckDuckGoTools
from persona import detect_persona, get_prompt_for
from sentence_transformers import SentenceTransformer


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

# Initialize model (Gemini Flash or GPT-4.1 mini)
llm = OpenAIChat(
    id="google/gemini-flash-1.5",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Create embedder object
class SimpleEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimensions = self.model.get_sentence_embedding_dimension()

    def get_embedding(self, text: str):
        return self.model.encode(text).tolist()

embedder = SimpleEmbedder()

# Create LanceDB instance
vector_db = LanceDb(
    uri="./lancedb",
    embedder=embedder,
    table_name="bangalore_guide" 
)

# Load PDF Knowledge
kb = PDFKnowledgeBase(
    path="The Ultimate Bangalore Guide.pdf",
    vector_db=vector_db
)

# Add web search tool
tools = [DuckDuckGoTools()]



# Run chat loop
if __name__ == "__main__":
    print("🤖 Bangalore Smart City Agent is ready!\n(Type 'exit' to quit)\n")

    user_id = "intern_01"
    session_id = "banza_test_1"

    # Initial input and persona
    first_input = input("Tell me a bit about yourself or your needs (so I can personalize):\nYou: ")
    persona = detect_persona(first_input)
    prompt = get_prompt_for(persona)
    print(f"[Persona: {persona}]")

    agent = Agent(
        model=llm,
        knowledge=kb,
        tools=tools,
        num_history_runs=10,  # Adjust as needed for memory depth
        description=prompt,
        markdown=True,
    )
    agent.instructions = prompt

    # First response
    response = agent.run(first_input)
    print(f"\nAgent: {response.content}\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # Detect persona for this query
        detected_persona = detect_persona(user_input)
        if detected_persona != persona:
            persona = detected_persona
            prompt = get_prompt_for(persona)
            agent.instructions = prompt
            print(f"[Persona changed to: {persona}]")

        # The agent will automatically use chat memory (last N turns)
        response = agent.run(user_input)
        print(f"\nAgent: {response.content}\n")





         