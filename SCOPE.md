

# Limitations and Future Scope

## Current Limitations

### 1. Data Coverage
- Scraped data is limited to ~5–10 restaurants only.
- No mechanism for **periodic or real-time updates** of restaurant data yet.

### 2. Model Choices
- **Gemini 2.0 Flash** (free tier) is used for answering queries but is a closed-source model.
- Open-source HuggingFace models could not be reliably adopted due to quality issues.

### 3. Scalability
- No **caching mechanism** (e.g., Redis) to reduce repeated retrieval time.
- Scraping process is **sequential** and can be **time-consuming** for large datasets.
- No background processing like **Celery** or **threading** for parallel tasks.

### 4. User Experience
- **Basic Streamlit app** with minimal styling.
- **No login/authentication** for user personalization.
- **No file uploads** (e.g., allowing restaurants to submit their own menus for ingestion).

### 5. Conversation Handling
- **Single-turn conversations** only.
- No **multi-turn memory** to maintain longer discussions.
- No **personalized recommendations** based on chat history yet.

---

## Future Enhancements

### 1. Expand Toolset (Multi-Tool Agent)
- Add multiple "tools" beyond simple web search fallback.
- Examples: 
  - Price Comparison APIs
  - Reviews Aggregators
  - Restaurant Menu Fetchers
- Implement **MCP (Multi-Cloud Processing)** Servers to fetch external service data dynamically.

### 2. Scalability Improvements
- Introduce **background workers** (using **Celery** + **Redis**) for:
  - Scraping multiple restaurant sites simultaneously.
  - Preloading frequently asked queries.
- Enable **batch scraping** pipelines with retry logic and failure handling.

### 3. Frontend and User Experience
- Build a **richer frontend** with:
  - Images of dishes, real-time menu cards, maps integration.
  - Responsive design and mobile-friendliness.
- Add **authentication/login** features for:
  - Saving past queries.
  - Personalized restaurant suggestions.

### 4. Advanced RAG Enhancements
- Move from standard RAG to **Advanced Multi-Stage RAG**:
  - Use query expansion and multi-hop retrievals.
  - Reranking retrieved chunks using a **cross-encoder** model before sending to LLM.

### 5. Conversational Memory
- Implement **memory buffers** for user sessions:
  - Track previous interactions.
  - Personalize responses based on past chats (multi-turn memory).

### 6. Continuous Learning
- Implement **continuous learning** from user feedback:
  - Allow users to rate answers.
  - Fine-tune models periodically based on real user conversations.

---

### 🌟 Long-Term Vision
> Evolve the project into a **full-stack Intelligent Restaurant Assistant** that not only answers queries but also suggests curated experiences, tracks dietary preferences, and learns user tastes over time.


![ChatGPT Image Apr 27, 2025, 10_31_52 AM](https://github.com/user-attachments/assets/15365d48-6a6d-41a1-b1f3-db4ad7831908)


