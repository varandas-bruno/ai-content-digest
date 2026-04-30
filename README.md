# 🎬 AI Content Digest

> An AI agent that researches, transcribes and summarizes YouTube content.

![Status](https://img.shields.io/badge/status-WIP-yellow)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🧠 What is this?

**AI Content Digest** is an AI agent that takes a topic or question, searches YouTube for relevant videos, fetches their transcripts, and returns a structured summary — all through natural language.

---

## ✨ Features

- 🔍 **YouTube search** via YouTube Data API v3
- 📄 **Transcript extraction** from YouTube videos
- 🤖 **AI summarization** powered by a local LLM via Ollama
- 🔗 **MCP Tools** — modular, composable agent tools
- 🔄 **LangGraph orchestration** — stateful agent loop with conditional branching

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────┐
│               LangGraph Agent               │
│                                             │
│  ┌───────────────┐    ┌───────────────┐     │
│  │ search_youtube│───▶│ get_transcript│     │
│  └───────────────┘    └──────┬────────┘     │
│                              │              │
│                     ┌────────▼──────────┐   │
│                     │ summarize_content │   │
│                     └────────┬──────────┘   │
│                              │              │
│                     Response to User        │
└─────────────────────────────────────────────┘
                    │
                 Ollama
              (local LLM)
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Agent Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM | [Ollama](https://ollama.com) (local, e.g. `llama3`, `mistral`) |
| Agent Tools | MCP (Model Context Protocol) |
| YouTube Search | YouTube Data API v3 |
| Transcript Fetching | `youtube-transcript-api` |
| Env management | `pip` + `requirements.txt` |

---

## 📁 Project Structure

```
AI-CONTENT-DIGEST/
├── app/
│   ├── agent.py                    ← LangGraph agent loop
│   ├── core/
│   │   ├── search/
│   │   │   └── youtube_search.py   ✅ YouTube search
│   │   └── sources/
│   │       └── youtube.py          ✅ Transcript fetch + digest
│   ├── tools/
│   │   └── definitions.py          ⬜ MCP tool definitions (WIP)
│   ├── mcp/
│   │   └── server.py               ⬜ MCP server (WIP)
│   ├── models/
│   ├── prompts/
│   └── routes/
├── tests/
├── .env
├── requirements.txt
└── README.md
```

---

## 🔧 Agent Tools (MCP)

The agent exposes 3 composable tools:

| Tool | Description |
|---|---|
| `search_youtube(query, max_results)` | Searches YouTube, returns a list of videos |
| `get_video_transcript(url)` | Fetches the full transcript of a video |
| `summarize_content(text, focus)` | Calls the local LLM to generate a summary |

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) installed and running locally
- A YouTube Data API v3 key

### 2. Clone the repo

```bash
git clone https://github.com/your-username/ai-content-digest.git
cd ai-content-digest
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file at the root:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### 5. Pull an Ollama model

```bash
ollama pull llama3
```

### 6. Run the agent

```bash
python app/agent.py
```

---

## 🗺️ Roadmap

- [x] YouTube search module
- [x] Transcript extraction module
- [ ] MCP tool definitions
- [ ] LangGraph agent loop
- [ ] End-to-end tests
- [ ] CLI interface

---

## 🤝 Contributing

This is a personal learning project in AI Engineering, but feedback and ideas are welcome. Feel free to open an issue.

---

## 📄 License

MIT © [Your Name]
