LLM + RAG for Finance

Summary

This repository converts the notebook "LLM + RAG for Finance" into a small Python project you can run and publish to GitHub. The project demonstrates fetching market and company data, pre-processing it, creating embeddings, storing them in a Chroma vectorstore, and building a Retrieval-Augmented Generation (RAG) QA pipeline using a Hugging Face model.

Features
- Fetch stock/company quotes from Financial Modeling Prep (FMP) API
- Fetch news using NewsAPI
- Preprocess economic and news data
- Create embeddings with Hugging Face sentence transformers and LangChain
- Store vectors using Chroma (persisted directory)
- Build a RetrievalQA chain using a Hugging Face model

Tech stack
- Python (3.8+)
- pandas
- requests
- certifi
- newsapi-python
- langchain
- langchain-community
- transformers
- sentence-transformers
- chromadb
- huggingface_hub
- python-dotenv

Repository layout

- README.md            - This file
- requirements.txt     - Python dependencies
- .gitignore
- src/                 - Python package
  - config.py          - Environment and config helpers
  - data_fetch.py      - FinancialModelingPrep API helpers
  - news_fetch.py      - NewsAPI helpers
  - preprocess.py      - Preprocessing utilities
  - embeddings.py      - Build embeddings and Chroma vectorstore
  - rag.py             - Build and query a RetrievalQA chain
- scripts/
  - run_demo.py        - Minimal demo script showing the end-to-end flow

Setup

1) Create and activate a virtual environment (zsh):

   python -m venv .venv
   source .venv/bin/activate

2) Install dependencies:

   pip install -r requirements.txt

3) Create a `.env` file in the project root with the following keys:

   FMP_API_KEY=your_financialmodelingprep_api_key
   NEWSAPI_API_KEY=your_newsapi_api_key
   HUGGINGFACEHUB_API_TOKEN=your_hf_token

4) Run the demo:

   python scripts/run_demo.py

Notes

- Many of the functions return pandas DataFrames or LangChain objects. The demo script shows a short flow but you will likely adapt modules to your dataset and environment.
- For better results you may use a paid/large LLM from Hugging Face or OpenAI. The code is modular so you can swap LLMs.

License

Add a license file if you plan to publish on GitHub.
# finance_advisor
