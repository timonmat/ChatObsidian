# ChatObsidian

ChatObsidian is an Quation and Answer AI integration for a folder of markdown notes.  
Intended for Obsidian notes vault, but you could use it for any local folder of markdown files.

run locally with

```
pipenv install \
pipenv shell \
streamlit run ChatObsidian.py
```

### TODO

- [ ] vector database integration (chroma?)
- [ ] rate limiting (openAI free plan workaround)
- [ ] gpt3.5-turbo support (cost reduction)
- [ ] local embeddings model support (langchain/huggingface) (cost reduction, privacy)
