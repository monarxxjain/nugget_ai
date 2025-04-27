export PYTHONPATH := .

.PHONY: init get_legal_site preprocess_data chat_ui scrape knowledge_base lint format setup

init:
	uv sync
	# uv run playwright install

get_legal_site:
	uv run scripts/legal_sites_to_scrape_robots.py

preprocess_data:
	uv run python preprocessing/json_preprocesser.py

scrape:
	uv run scrapers/scrape.py

knowledge_base:
	uv run kb/build_index.py

lint:
	uv run ruff check

format:
	uv run ruff format

setup: scrape preprocess_data knowledge_base

chat_ui:
	uv run streamlit run chatbot/chatbot_ui.py
