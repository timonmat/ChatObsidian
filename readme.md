# ChatObsidian

ChatObsidian is an Question and Answer AI integration for a folder of markdown notes.  
Intended for Obsidian notes vault, but you could use it for any local folder of markdown files.

run locally with

```bash
pipenv shell \
pipenv install \
export OPENAI_API_KEY=YOUR_API_KEY \
streamlit run ChatObsidian.py
```

### TODO

- [x] vector database integration (chroma)
- [x] gpt3.5-turbo support (cost reduction)
- [x] local embeddings model support (langchain/huggingface) (cost reduction, privacy)
- [ ] local LLM support (free, privacy)
- [ ] select and configure LLM on sidebar (model and prompthelper)
- [ ] pdf support
- [ ] image support
- [ ] docker support (folder mapping would suck a bit. maybe map to a default './data/obsidianvault')
- [ ] multi collection support (collection per vault folder? select which folders to index)
