# 🎬 AI Content Digester

> An AI agent that researches, transcribes and summarizes YouTube content — built to learn AI Engineering from the ground up.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![LangGraph](https://img.shields.io/badge/LangGraph-agent-orange)
![MCP](https://img.shields.io/badge/MCP-tools-purple)

---

## 🧠 What is this?

**AI Content Digester** is a fully functional AI agent that takes a topic or question, searches YouTube for relevant videos, fetches their transcripts, and returns a structured summary — all through natural language.

Built as a hands-on AI Engineering learning project, it covers the full stack of modern LLM application development:
- **LangGraph** — stateful agent orchestration with ReAct pattern
- **MCP (Model Context Protocol)** — modular, composable tool exposure
- **Ollama** — local LLM inference (no cloud costs)
- **LangChain** — LLM abstraction and tool binding

---

## 🔍 Problem

In the world of AI Engineering, professionals face:
- Information overload from blogs, papers, GitHub, and documentation
- Time-consuming research across scattered sources
- A rapidly evolving stack with new models and tools released monthly

**AI Content Digester** solves this by collecting, summarizing, and organizing AI content into clear, concise, and up-to-date knowledge digests.

---

## ✨ Features

- 🔍 **YouTube search** via YouTube Data API v3
- 📄 **Transcript extraction** from YouTube videos
- 🤖 **AI summarization** powered by a local LLM via Ollama
- 🔗 **MCP Tools** — modular tools exposed via FastMCP server
- 🔄 **LangGraph ReAct agent** — stateful loop with conditional branching
- 📋 **Structured output** — titles, key takeaways, published dates
- 🗂️ **Separation of concerns** — clean modular architecture

---

## 🏗️ Architecture

```
User Input (topic/question)
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                      LangGraph Agent                        │
│                                                             │
│   [START]                                                   │
│      │                                                      │
│      ▼                                                      │
│  [assistant] ◄──────────────────┐                          │
│  llm.invoke(messages)           │                          │
│      │                          │                          │
│      ▼                          │                          │
│  tools_condition?               │                          │
│      │                          │                          │
│  ┌───┴───────────┐              │                          │
│  │               │              │                          │
│  ▼               ▼              │                          │
│ [tools]        [END]            │                          │
│ execute         final      ─────┘                          │
│ tool call       answer                                      │
└─────────────────────────────────────────────────────────────┘
        │                  │
        ▼                  ▼
┌───────────────┐  ┌───────────────────┐
│  MCP Server   │  │     Ollama        │
│  (server.py)  │  │  (local LLM)      │
│               │  │                   │
│ search_youtube│  │  llama3.2 / etc   │
│ transcript    │  └───────────────────┘
└───────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Agent Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM | [Ollama](https://ollama.com) (local — e.g. `llama3.2:3b`) |
| LLM Abstraction | [LangChain](https://github.com/langchain-ai/langchain) |
| Agent Tools Protocol | [MCP](https://modelcontextprotocol.io) via [FastMCP](https://github.com/jlowin/fastmcp) |
| MCP ↔ LangChain Bridge | [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters) |
| YouTube Search | YouTube Data API v3 |
| Transcript Fetching | `youtube-transcript-api` |
| Env Management | `python-dotenv` + `requirements.txt` |

---

## 📁 Project Structure

```
ai-content-digest/
├── app/
│   ├── agent.py                     ← LangGraph ReAct agent
│   ├── core/
│   │   ├── search/
│   │   │   └── youtube_search.py    ← YouTube Data API v3 search
│   │   └── sources/
│   │       └── youtube.py           ← Transcript extraction
│   ├── mcp_server/
│   │   └── server.py                ← FastMCP server (tool definitions)
│   ├── models/
│   │   └── schemas.py               ← Pydantic request/response models
│   └── prompts/
│       └── system_prompt.md         ← Agent system prompt
├── tests/
├── .env.example                     ← Environment variables template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔧 MCP Tools

The agent exposes 2 composable tools via the MCP server:

| Tool | Description |
|---|---|
| `search_youtube_tool(query, max_results)` | Searches YouTube, returns list of videos with metadata |
| `transcript_youtube_tool(url)` | Fetches and returns the transcript of a YouTube video |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) installed and running locally
- A YouTube Data API v3 key ([get one here](https://console.cloud.google.com/))

### 1. Clone the repo

```bash
git clone https://github.com/varandas-bruno/ai-content-digest.git
cd ai-content-digest
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### 4. Pull an Ollama model

```bash
ollama pull llama3.2:3b
```

### 5. Run the agent

```bash
python -m app.agent
```

You will be prompted:
```
What content do you want to search on Youtube? I will summarize it!
> ai engineering
```

---

## 💡 How it works

1. **User inputs** a topic (e.g. "ai engineering")
2. The **LangGraph agent** starts the ReAct loop
3. The **assistant node** (LLM) decides to call `search_youtube_tool`
4. The **MCP server** executes the search and returns video metadata
5. The **assistant node** decides to call `transcript_youtube_tool` for each video
6. The **MCP server** fetches transcripts
7. The **LLM synthesizes** all transcripts into a structured summary
8. The agent reaches **END** and returns the final answer

---

## 🗺️ Roadmap

- [x] YouTube search module
- [x] Transcript extraction module
- [x] MCP server with FastMCP
- [x] LangGraph ReAct agent loop
- [x] System prompt separation
- [x] Structured output guidelines
- [ ] Structured output with Pydantic (`with_structured_output`)
- [ ] Evaluation suite (faithfulness, relevance scoring)
- [ ] End-to-end tests

---

## 🗺️ Roadmap

- [x] YouTube search module
- [x] Transcript extraction module
- [x] MCP tool definitions
- [x] LangGraph agent loop
- [ ] End-to-end tests

---

## 🤝 Contributing

This is a personal learning project in AI Engineering, but feedback and ideas are welcome. Feel free to open an issue.

---

## 📄 License

MIT © Bruno Varandas
