## MDCAT AI Project Structure

```
MDCAT_AI/  
│── .devcontainer/           # (Existing) Development container configs  
│── .github/                 # (Existing) GitHub workflows/settings  
│── Assets/Images/           # (Existing) Store logos and UI images  
│  
│── data/                    # 🔹 NEW: Store MDCAT book text, past papers  
│   ├── mdcat_books_text.json  
│   ├── past_papers.csv  
│   ├── formulas.pkl  
│  
│── models/                  # 🔹 NEW: Store trained models & tokenizers  
│   ├── mdcat_model.pth  
│   ├── tokenizer/  
│  
│── src/                     # 🔹 NEW: Core AI scripts  
│   ├── preprocess.py        # Data cleaning & tokenization  
│   ├── train.py             # Model training script  
│   ├── infer.py             # Model inference (Q&A)  
│  
│── positioning/             # 🔹 NEW: Handles ranking, embeddings & retrieval  
│   ├── ranker.py           # Re-rank responses based on confidence score  
│   ├── embedding_store.py  # Store/retrieve vector embeddings (FAISS, ChromaDB)  
│   ├── context_manager.py  # Ensures correct answer context  
│  
│── app/                     # 🔹 (Modify) Streamlit frontend  
│   ├── streamlit_app.py     # (Existing) Main Streamlit UI  
│   ├── utils.py             # 🔹 NEW: Helper functions  
│  
│── api/                     # 🔹 NEW: FastAPI for scalable AI serving  
│   ├── server.py            # FastAPI backend  
│  
│── .gitignore               # (Existing) Git ignore file  
│── LICENSE                  # (Existing) License file  
│── README.md                # (Existing) Documentation  
│── requirements.txt         # (Existing) Dependencies  
```

