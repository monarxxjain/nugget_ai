# Project Architecture



### 1. Data Scraping
- **Initial Idea:** I explored over 20+ individual restaurant [websites](./scripts/legal_sites_to_scrape_robots.py) that allowed scraping.
- **Problem Faced:** These websites lacked complete, detailed, and structured information. Scraping them using query selectors also proved unscalable and brittle.
- **Final Approach:**  
  Instead, I decided to scrape **Zomato's restaurant listings**, where data about restaurants and dishes is highly detailed and structured.
- **Note:** Although Zomato's `robots.txt` blocks scraping, I obtained written permission for this assignment (see [ASSUMPTIONS.md](./ASSUMPTIONS.md)).
- **Reference:**  
  [`/scrapers/scrape.py`](./scrapers/scrape.py)

---

### 2. Preprocessing / Normalization
- **Goal:** Clean and normalize the raw scraped data into a consistent format.
- **Tasks Done:**
  - Extracted relevant fields (menu items, prices, dietary features, timings, etc.).
  - Converted all prices into Indian Rupees (INR) by fetching real-time currency exchange rates.
  - Standardized the format across all restaurant entries.
- **Reference:**  
  [`/knowledge_base/preprocess.py`](./knowledge_base/preprocess.py)

---

### 3. Embedding Generation
- **Initial Approach:**  
  Tried using Google's `gemini-embedding-exp-03-07` model via API ([link](https://ai.google.dev/gemini-api/docs/models#gemini-embedding)).

- **Problem Faced:**  
  - Severe rate limits even after batching.
  - Unreliable for bulk processing in free tier.

- **Final Approach:**  
  - Switched to **Hugging Face’s BAAI/bge-m3** open-source model.
  - Ran locally to avoid rate limits and control the embedding generation process.

- **Reference:**  
  [`/kb/build_index.py`](./kb/build_index.py)

---

### 4. Retrieval-Augmented Generation (RAG)

- **UI Setup:**  
  Launched a simple **Streamlit** web app for interacting with the chatbot.

- **How RAG Works in this Project:**
  1. **Initial Query Expansion:**  
     User query is first refined through the LLM to make it semantically stronger and better suited for retrieval.
  2. **Vector Search:**  
     The improved query is embedded and used to retrieve top relevant chunks from the knowledge base.
  3. **Final LLM Call:**  
     The original user query, along with retrieved context chunks, is sent to the LLM to generate the final response.

- **Enhancement Over Basic RAG:**  
  Unlike basic RAG (which directly retrieves and answers), this two-stage retrieval improves both recall and final answer quality.

- **Reference:**  
  `/chatbot/retriever.py`, `/chatbot/generator.py`, `/chatbot/chatbot_ui.py`

---

## Folder Structure

```plaintext
/root
│
├── Makefile                # Setup and run commands
├── pyproject.toml          # Python dependencies
│
├── /scrapers
│   └── scrape.py           # Web scraping logic
│
├── /data
│   ├── /raw_json           # (Optional) Raw unprocessed data
│   └── /processed_json     # Final structured data for chatbot
│
├── /knowledge_base (kb)
│   ├── build_index.py      # Embedding creation from processed data
│   └── preprocess.py       # Data normalization and cleaning
│
├── /chatbot
│   ├── generator.py        # Response generation logic
│   ├── retriever.py        # Retrieval logic
│   ├── tools.py            # Fallback options like external search (if no result found)
│   └── chatbot_ui.py       # Streamlit App (Frontend)
│
└── README.md               # Main documentation
