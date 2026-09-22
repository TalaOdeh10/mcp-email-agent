# MCP Email Agent

An AI-powered Gmail assistant built with **Model Context Protocol (MCP)**, **Google Gemini**, and **LangChain**.

The project allows users to interact with their Gmail inbox using natural language. Instead of manually selecting tools, the AI agent understands the user's request and decides which Gmail tool to use.

For example:

> "Find my unread emails about invoices"

The agent understands the request, selects the appropriate Gmail tool, executes it through the MCP server, and returns the results in a conversational format.

---

## ✨ Features

* 🤖 AI-powered email assistant
* 🔌 Model Context Protocol (MCP) integration
* 📧 Gmail API integration
* 🔎 Search emails using natural language
* 📬 List recent emails
* 📄 Retrieve individual emails
* 🧠 Gemini-powered tool selection
* 🛠️ MCP tools exposed dynamically to the AI agent
* 🌐 FastAPI backend
* 💬 Web frontend
* 🧪 Automated tests
* 🔐 OAuth authentication with Google
* 🗂️ Conversation/memory components

---

## 🏗️ Architecture

The main architecture follows this flow:

```text
                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                           Natural Language
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │      AI Agent           │
                    │                         │
                    │ Gemini + LangChain      │
                    └────────────┬────────────┘
                                 │
                         Tool Selection
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       MCP Client        │
                    └────────────┬────────────┘
                                 │
                         MCP Protocol
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       MCP Server        │
                    │                         │
                    │      Gmail Tools        │
                    └────────────┬────────────┘
                                 │
                            Gmail API
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      Google Gmail       │
                    └─────────────────────────┘
```

### Why MCP?

Instead of tightly coupling the AI agent directly to Gmail functionality, the project separates the **AI reasoning layer** from the **tool layer**.

The MCP server exposes Gmail capabilities as tools.

The AI agent discovers these tools and decides when to use them.

This makes the system easier to extend with additional tools or services later.

---

## 🧰 MCP Tools

The MCP server currently exposes the following tools:

| Tool            | Description                  |
| --------------- | ---------------------------- |
| `hello`         | Simple MCP connectivity test |
| `list_emails`   | Retrieve recent emails       |
| `search_emails` | Search Gmail using a query   |
| `get_email`     | Retrieve a specific email    |

The AI agent can select these tools based on the user's request.

### Example

User:

```text
Find my unread emails about invoices
```

The agent interprets the request and selects:

```text
search_emails
```

with a Gmail search query such as:

```text
is:unread invoice
```

The MCP server executes the tool and returns the results to the agent.

---

## 🧠 Technologies

### AI & Agent

* Python
* Google Gemini
* LangChain
* Pydantic

### Agent Communication

* Model Context Protocol (MCP)
* MCP Client
* MCP Server
* FastMCP

### Email Integration

* Gmail API
* Google OAuth 2.0

### Backend

* FastAPI
* Uvicorn

### Frontend

* HTML
* CSS
* JavaScript

### Testing

* Pytest

---

## 📁 Project Structure

```text
mcp-email-agent/
│
├── agent/
│   ├── main.py
│   ├── memory.py
│   └── prompts.py
│
├── api/
│   └── main.py
│
├── client/
│   └── mcp_client.py
│
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
│
├── server/
│   ├── auth/
│   │   └── gmail_auth.py
│   │
│   ├── models/
│   │   └── email_models.py
│   │
│   ├── services/
│   │   └── gmail_service.py
│   │
│   ├── tools/
│   │   └── email_tools.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_confirmation.py
│   └── test_email_tools.py
│
├── .env.example
├── .gitignore
├── DECISIONS.md
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/TalaOdeh10/mcp-email-agent.git
cd mcp-email-agent
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Google Gmail API Setup

This project uses Google OAuth to access Gmail.

### 1. Create a Google Cloud project

Create or select a project in Google Cloud Console.

Enable the:

```text
Gmail API
```

### 2. Configure OAuth credentials

Create OAuth client credentials for a desktop application.

Download the credentials file and place it here:

```text
server/auth/credentials.json
```

### 3. Environment variables

Create a `.env` file based on:

```text
.env.example
```

Add the required Gemini API key and other environment variables used by the project.

> **Security:** Never commit `.env`, `credentials.json`, or `token.json` to GitHub.

These files are intentionally excluded through `.gitignore`.

---

## ▶️ Running the Agent

After completing the authentication setup:

```bash
python -m agent.main
```

The MCP client connects to the server and discovers the available tools:

```text
Connected to MCP server!

Available tools:

- hello
- list_emails
- search_emails
- get_email
```

You can then interact with the agent using natural language.

---

## 🔄 Example Interaction

```text
You: Find my unread emails about invoices

Agent is using: search_emails

Arguments:
{
    "query": "is:unread invoice"
}

Agent:
I found several unread emails related to invoices.
```

This demonstrates the complete flow:

```text
Natural Language
       ↓
Gemini
       ↓
Tool Selection
       ↓
MCP Client
       ↓
MCP Server
       ↓
Gmail API
       ↓
Email Results
       ↓
AI Response
```

---

## 🧪 Testing

Run the test suite with:

```bash
pytest
```

The repository includes tests covering email-related functionality and confirmation behavior.

---

## 🔒 Security

Sensitive authentication files are intentionally excluded from Git.

The following files should **never** be committed:

```text
.env
server/auth/credentials.json
server/auth/token.json
.venv/
```

The `.gitignore` file is configured to prevent accidental commits of these files.

---

## 🎯 Project Goals

This project was built to explore how **AI agents can interact with external systems through Model Context Protocol**.

The main learning goals were:

* Understanding MCP architecture
* Building an MCP server
* Creating an MCP client
* Exposing real-world functionality as MCP tools
* Connecting an LLM to external tools
* Implementing dynamic tool selection
* Integrating Gmail API and OAuth
* Structuring an agent-based Python application
* Separating the AI, MCP, API, and service layers

---

## 🔮 Future Improvements

Potential extensions include:

* ✉️ Draft email generation
* 📤 Send emails with confirmation
* 🏷️ Gmail label management
* 📌 Email summarization
* 🧵 Conversation/thread analysis
* 🔎 More advanced Gmail search
* 🧠 Improved conversational memory
* 🌐 Complete web-based chat interface
* 🔐 More granular tool permissions
* 📊 Email analytics

---

## 📚 What I Learned

Building this project provided hands-on experience with **AI agents, MCP, tool calling, API integration, and agent-based application architecture**.

### AI Agents

Understanding how an LLM can interpret a user's request and select an appropriate tool.

### Model Context Protocol

Learning how MCP provides a standardized way for AI applications to discover and use external tools.

### Tool Calling

Connecting natural-language requests to structured Python functions.

### API Integration

Working with the Gmail API and Google OAuth authentication.

### Software Architecture

Separating the application into distinct layers:

```text
Agent
  ↓
MCP Client
  ↓
MCP Server
  ↓
Services
  ↓
External API
```

---

## 👩‍💻 Author

**Tala Odeh**

CIS Student | Aspiring AI/ML & Agentic AI Engineer

Interested in:

* Agentic AI
* AI Agents
* Model Context Protocol
* RAG
* LLM Applications
* AI Engineering
* Intelligent Automation

---

## ⭐ Acknowledgment

This project was developed as a hands-on learning project to explore **MCP, AI agents, tool calling, and real-world API integration**.
