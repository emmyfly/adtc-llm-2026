import os

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "knowledge")

def load_knowledge():
    docs = []
    for filename in os.listdir(KNOWLEDGE_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(KNOWLEDGE_DIR, filename)
            with open(path, "r") as f:
                content = f.read()
            sections = content.strip().split("\n\n")
            for section in sections:
                docs.append({"source": filename, "text": section.strip()})
    return docs

def search_knowledge(query, docs, top_k=3):
    query_words = set(query.lower().split())
    scored = []
    for doc in docs:
        doc_words = set(doc["text"].lower().split())
        overlap = len(query_words & doc_words)
        if overlap > 0:
            scored.append((overlap, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc["text"] for _, doc in scored[:top_k]]

knowledge_base = load_knowledge()

def get_context(question):
    relevant = search_knowledge(question, knowledge_base)
    if relevant:
        return "REFERENCE DATA:\n" + "\n---\n".join(relevant) + "\n\nUsing the reference data above and your own knowledge, answer the farmer's question:"
    return ""
