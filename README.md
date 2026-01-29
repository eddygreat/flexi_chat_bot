# langchain-gemini-chatbot

A stateful, context-aware chatbot implemented using **LangChain** and **Google Gemini** (via `langchain-google-genai`). This project demonstrates how to manage conversation history effectively using `RunnableWithMessageHistory`.

> [!NOTE]
> **Why Gemini?**
> This project was originally designed for the **OpenAI API**. It was switched to **Google Gemini** during development due to OpenAI API quota limitations. The architecture uses LangChain's abstraction, making it trivial to switch back to OpenAI (or any other provider) by changing just the model initialization lines.

## 🚀 Features

-   **Stateful Memory**: Remembers user details and conversation context across multiple turns using session IDs.
-   **LangChain Integration**: Built on the robust LangChain framework using LCEL (LangChain Expression Language).
-   **Google Gemini Powered**: Utilizes the efficient `gemini-2.0-flash` model for high-quality responses.
-   **Secure Configuration**: Uses environment variables for API key management.
-   **Extensible Design**: Modular structure allowing for easy replacement of the memory store (currently in-memory) with persistent databases like Redis or PostgreSQL.

## 🛠️ Tech Stack

-   **Language**: Python 3.10+
-   **Framework**: [LangChain](https://python.langchain.com/)
-   **LLM Provider**: Google Generative AI (Gemini)
-   **Dependencies**:
    -   `langchain`
    -   `langchain-google-genai`
    -   `langchain-community`
    -   `python-dotenv`

## ⚙️ Installation

1.  **Clone the repository** (if applicable) or navigate to your project directory.

2.  **Install Dependencies**:
    Ensure you have Python installed, then run:

    ```bash
    pip install langchain langchain-google-genai langchain-community python-dotenv
    ```

## 🔑 Configuration

1.  **Get a Google API Key**:
    -   Visit [Google AI Studio](https://aistudio.google.com/).
    -   Create a new API key.

2.  **Set up Environment Variables**:
    -   Create a file named `.env` in the root directory.
    -   Add your API key:

    ```env
    GOOGLE_API_KEY=your_api_key_here
    ```

    > **Note**: A `.env.example` file is provided for reference.

## 🏃 Usage

Run the chatbot script directly to execute the built-in test suite:

```bash
python chatbot.py
```

### How it Works

The script executes a `run_test_suite()` function that simulates a conversation:
1.  **Turn 1**: User introduces themselves.
2.  **Turn 2**: User asks a technical question.
3.  **Turn 3**: User asks a follow-up question (context dependent).
4.  **Turn 4**: User tests the bot's memory of the introductions.
5.  **Turn 5**: User requests a summary of the chat.

The bot uses an in-memory dictionary `store` to save the history for `session_id="test_session_123"`.

## 📂 Project Structure

```
.
├── .env                # API Keys (Not committed)
├── .env.example        # Template for environment variables
├── chatbot.py          # Main bot implementation and test suite
└── README.md           # Project documentation
```

## 🔮 Future Improvements

-   **Persistent Storage**: Replace the in-memory `store` dictionary with **Redis** or **PostgreSQL** to persist sessions after the script stops.
-   **CLI Interface**: Add an interactive loop `while True:` to allow real-time typing instead of the hardcoded test suite.
-   **Dockerize**: Containerize the application for easy deployment.
