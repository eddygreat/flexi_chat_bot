import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key
if not os.getenv("GOOGLE_API_KEY"):
    print("Error: GOOGLE_API_KEY not found in environment variables. Please create a .env file.")
    sys.exit(1)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage

# --- Configuration ---
MODEL_NAME = "gemini-2.0-flash"

# --- simple in-memory session store ---
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Returns the chat message history for a given session ID.
    In a production environment, this should retrieve history from a persistent database
    (e.g., Redis, PostgreSQL) instead of an in-memory dictionary.
    """
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# --- Chatbot Definition ---

# 1. Initialize LLM
llm = ChatGoogleGenerativeAI(model=MODEL_NAME)

# 2. Define Prompt Template
# Includes system instruction, chat history placeholder, and user input
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful Technical Assistant for Engineering and AI projects."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

# 3. Create Chain
# Prompt -> LLM -> String Output
chain = prompt | llm | StrOutputParser()

# 4. Add Message History
# Wraps the chain to manage history automatically based on session_id
listening_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# --- Verification / Testing ---
def run_test_suite():
    print("--- Starting Chatbot Test Suite (Gemini) ---")
    session_id = "test_session_123"
    print(f"Session ID: {session_id}")

    test_queries = [
        # 1. Introduction
        "Hi, I'm Alice. I am a Senior DevOps Engineer.",
        
        # 2. Technical Question
        "What are the key benefits of using Docker for microservices?",
        
        # 3. Follow-up (requires context)
        "Can you give me a command to list all running containers?",
        
        # 4. Recall (requires memory of step 1)
        "Based on my profession to help me optimize a CI/CD pipeline, what tool would you recommend mostly?",
        
        # 5. Summary
        "Please summarize what we have discussed so far."
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n[Turn {i}] User: {query}")
        config = {"configurable": {"session_id": session_id}}
        
        # Stream response for better UX in console, or just invoke
        # valid runnables with history support invoke/stream
        try:
            response = listening_chain.invoke(
                {"input": query},
                config=config
            )
            print(f"[Turn {i}] Bot: {response}")
        except Exception as e:
            print(f"Error during invocation: {e}")

    print("\n--- Test Suite Completed ---")

if __name__ == "__main__":
    run_test_suite()
