# Assumptions and Special Decisions


## 1. Scraping Source
- Zomato’s `robots.txt` file does not allow automated scraping.
- However, **written permission was obtained** via email specifically for this assignment.
- (Attached in the final submission: Screenshot of the approval email as proof.)


## 2. Choice of LLM Model
- Initially tested several open-source models on Hugging Face, but they did not provide consistent or accurate answers for restaurant-related queries.
- Final Decision:
  - **Google's Gemini 2.0 Flash (Free Version)** was used for final response generation (due to better quality, speed, and availability).
  - **Note:** The Gemini model was only used at inference stage for generating answers, not during vector search.


## 3. Embedding Model and Retrieval Strategy
- **Embedding Generation:**  
  Used the **BAAI/bge-m3** model from Hugging Face locally to avoid API rate limits and ensure high-quality embeddings.
- **Vector Database:**  
  Stored embeddings in **Qdrant**, chosen for its:
  - Open-source nature
  - Scalability
  - Easy local deployment
- **Retrieval Strategy:**  
  Semantic search over stored embeddings to fetch relevant documents.


## 4. `make` Automation
- A **Makefile** was used to automate all setup, build, and run commands (e.g., scraping, preprocessing, embedding creation, running the app).
- **Note:**  
  - If `make` is not installed on the system, all commands can be run manually using `uv` (e.g., `uv pip install`, `uv python chatbot_ui.py`).


## 5. Number of Restaurants
- Scraped **5 to 10 restaurants** as per the project guidelines.
- Ensured sufficient diversity in cuisine types, price ranges, and locations.


## 6. Communication and Clarifications
- Before proceeding with scraping Zomato and other design decisions, I reached out via email to the official project contact.
- Received confirmation allowing the approach and assumptions outlined here.


 ![Screenshot 2025-04-27 100723](https://github.com/user-attachments/assets/0332c209-bbde-44c4-92d0-a053e0fc3b8f)


