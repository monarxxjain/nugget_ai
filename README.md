## Project: Nugget AI - Restaurant Data Scraper & RAG-based Chatbot


https://github.com/user-attachments/assets/aab71d73-149a-4683-b41f-c86923d85be9


### Overview
This project combines web scraping and Retrieval-Augmented Generation (RAG) to build a chatbot that can answer natural language questions about restaurants, menus, features, dietary options, and more.

![Screenshot 2025-04-27 104834](https://github.com/user-attachments/assets/0f8c588e-30b4-413b-9ccc-f4f066eb998e)
---

### Features
- Scrapes restaurant data (menu items, prices, features, timings) from Zomato.
- Preprocesses and stores structured knowledge.
- Embedding generation using **BAAI/bge-m3** model.
- LLM responses generated using **Gemini 2.0 Flash** model.
- Simple Streamlit-based chatbot UI.

---

### Setup Instructions

#### 1. Clone the Repository
```bash
git clone https://github.com/monarxxjain/nugget_ai.git
cd nugget_ai
```

#### 2. Install Python Dependencies
```bash
uv sync
```

#### 3. Install `make` (if not already installed)
- Mac/Linux: `brew install make`
- Windows (use WSL or install manually)

---

### Commands

#### Run Setup (Scrape + Preprocess + Build Knowledge Base)
```bash
make setup
```

#### Start Chatbot UI
```bash
make chat_ui
```

> **Note:** If `make` doesn't work, you can directly run the uvicorn commands inside the `Makefile` under `setup` and `chat_ui`.

## Manual Run (If Make is Unavailable)

```bash
# Step 1: Scrape
uv run scrapers/scrape.py

# Step 2: Preprocess Data
uv run python preprocessing/json_preprocesser.py

# Step 3: Generate Embeddings
uv run kb/build_index.py

# Step 4: Launch Chatbot
uv run streamlit run chatbot/chatbot_ui.py
```


### Project Structure
(see [ARCHITECHTURE.md](./ARCHITECHTURE.md))


### Notes
- Scraped from Zomato with written permission to bypass robots.txt.
- Used Gemini 2.0 Flash model for better response quality.
- Data is saved after scraping and preprocessing in `/data/processed_json`.




