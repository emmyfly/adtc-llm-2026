import requests
import os
import re
from rag import get_context

URL = "http://localhost:8080/v1/chat/completions"

prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
with open(prompt_path, "r") as f:
    SYSTEM = f.read()

history = [{"role": "system", "content": SYSTEM}]
last_suggestions = []

def extract_suggestions(answer):
    suggestions = []
    for line in answer.split("\n"):
        match = re.match(r'>>\s*(\d+)\.\s*(.+)', line)
        if match:
            suggestions.append(match.group(2).strip())
    return suggestions

def ask(question):
    context = get_context(question)
    if context:
        enriched = context + "\n\n" + question
    else:
        enriched = question
    
    history.append({"role": "user", "content": enriched})
    
    response = requests.post(URL, json={
        "messages": history,
        "max_tokens": 256,
        "temperature": 0.7,
    })
    data = response.json()
    answer = data["choices"][0]["message"]["content"]
    
    history.append({"role": "assistant", "content": answer})
    return answer

print("=" * 50)
print("  AgriLM - Nigerian Agricultural Advisor")
print("  Offline AI · No Internet Required")
print("  Powered by Qwen2.5-3B + Nigerian Agri Knowledge Base")
print("  Type 'quit' to exit | 'clear' to reset")
print("  Type a number to select a suggested question")
print("=" * 50)

while True:
    question = input("\nFarmer: ")
    if question.lower() in ["quit", "exit", "q"]:
        print("Goodbye! Happy farming!")
        break
    if question.lower() == "clear":
        history = [{"role": "system", "content": SYSTEM}]
        last_suggestions = []
        print("Conversation cleared.")
        continue
    if not question.strip():
        continue
    
    if question.strip().isdigit() and last_suggestions:
        idx = int(question.strip()) - 1
        if 0 <= idx < len(last_suggestions):
            question = last_suggestions[idx]
            print(f"  >> {question}")
        else:
            print("Invalid selection. Ask your question directly.")
            continue
    
    answer = ask(question)
    print("\nAgriLM:", answer)
    last_suggestions = extract_suggestions(answer)
